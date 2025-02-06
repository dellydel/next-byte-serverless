import boto3
from src.http_response import create_response
from botocore.exceptions import ClientError
from src.utils.unmarshall import deserialize, convert_decimal

dynamodb = boto3.client('dynamodb')

def getRegistrationByEmail(email):
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
  except: 
    raise ClientError("Error when attempting to retrieve registrations.")