import boto3
import os
import uuid
from src.http_response import create_response
from botocore.exceptions import ClientError
from src.utils.unmarshall import deserialize, convert_decimal
import datetime
import stripe

dynamodb = boto3.client('dynamodb')

def getRegistrationByEmail(email):
  response = dynamodb.scan(
     TableName=os.environ.get("REGISTRATIONS_TABLE"),
     FilterExpression="emailLower = :emailLower OR email = :email",
     ExpressionAttributeValues={
      ":emailLower": { "S": email.lower() },
      ":email": { "S": email },
    },
    ProjectionExpression="amount, created, course_name, course_id, email",
    )
  try:
    payments = deserialize(response)
    amounts = list(map(lambda obj: {
      'date': datetime.datetime.fromtimestamp(int(obj.get("created")) / 1000).strftime('%Y-%m-%d %H:%M:%S'),
      'amount': convert_decimal(obj.get("amount")),
      'name': obj.get("course_name"),
      'course_id': obj.get("course_id"),
      'email': obj.get("email"),
    }, payments.get("Items")))
    return create_response(200, amounts)
  except Exception as e:
    return create_response(500, {"message": "Error when attempting to retrieve registrations."})
  
def check_existing_registration(email, course_id):
  response = dynamodb.scan(
    TableName=os.environ.get("REGISTRATIONS_TABLE"),
    FilterExpression="emailLower = :emailLower AND course_id = :course_id",
    ExpressionAttributeValues={
      ":emailLower": {"S": email.lower()},
      ":course_id": {"S": course_id}
    }
  )
  return response.get('Count', 0) > 0

def createCourseRegistration(body):
  stripe.api_key = os.environ.get("STRIPE_SECRET")
  if body.get("type").equals("payment_intent.succeeded"):
    session = body.get("data").get("object")
    try:
      checkout_session = stripe.checkout.sessions.list({
        'payment_intent': session.get("id"),
        'expand': ["data.line_items"],
      })
      lineItems = stripe.checkout.sessions.listLineItems(
        checkout_session.data[0].id
      )
      line_item = lineItems.get("data")[0]

      if check_existing_registration(session.get("receipt_email"), line_item.price.product):
        return create_response(409, {"message": "Registration already exists for this course."})
      
      table = dynamodb.Table(os.environ.get("REGISTRATIONS_TABLE"))
      table.put_item(
        Item = {
          'id':session.get("id"),
          'amount': session.get("amount"),
          'created': session.get("created"),
          'email': session.get("receipt_email"),
          'emailLower': str(session.get("receipt_email")).lower(),
          'course_name': line_item.description,
          'price': line_item.price.unit_amount,
          'product_id': line_item.price.product
        }
      )
      return create_response(200, "Transaction recorded successfully.")
    except Exception as e:
      raise Exception("Error when recording transaction.")
    
def createFreeCourseRegistration(body):
  try:
    dynamodb_resource = boto3.resource('dynamodb')
    table = dynamodb_resource.Table(os.environ.get("REGISTRATIONS_TABLE"))

    email = body.get("email")
    course_id = body.get("course_id")
    
    if check_existing_registration(email, course_id):
      return create_response(409, {"message": "Registration already exists for this course."})
    
    table.put_item(
      Item = {
        'id': str(uuid.uuid4()),
        'amount': 0,
        'created': int(datetime.datetime.now().timestamp() * 1000),
        'email': body.get("email"),
        'emailLower': body.get("email").lower(),
        'course_name': body.get("course_name"),
        'course_id': body.get("course_id"),
        'price': 0,
      }
    )
    return create_response(200, "Transaction recorded successfully.")
  except Exception as e:
    return create_response(500, {"message": "Error when recording transaction."})
