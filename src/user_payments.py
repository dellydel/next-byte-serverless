import boto3.utils
from src.http_response import create_response
from botocore.exceptions import ClientError
import boto3
import os
import datetime
from src.utils.unmarshall import deserialize, convert_decimal

dynamodb = boto3.client('dynamodb')

def retrievePayments(email):
  response = dynamodb.scan(
     TableName=os.environ.get("REGISTRATIONS_TABLE"),
     FilterExpression="emailLower = :emailLower OR email = :email",
     ExpressionAttributeValues={
      ":emailLower": { "S": email.lower() },
      ":email": { "S": email },
    },
    ProjectionExpression="amount, created, course_name",
  )
  try:
    payments = deserialize(response)
    amounts = list(map(lambda obj: {
      'date': datetime.datetime.fromtimestamp(int(obj.get("created")) / 1000).strftime('%Y-%m-%d %H:%M:%S'),
      'amount': convert_decimal(obj.get("amount")),
      'name': obj.get("course_name"),
    }, payments.get("Items")))
    return create_response(200, amounts)
  except ClientError as err:
      statusCode = err.statusCode if hasattr(err, 'statusCode') else 500
      message = err.message if hasattr(err, 'message') else 'Internal Server Error'
      return create_response(statusCode, message)

  
