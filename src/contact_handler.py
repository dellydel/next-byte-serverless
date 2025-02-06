import json 
from src.error_handler import handle_client_error
from src.contact import processContactRequest
from botocore.exceptions import ClientError

def handler(event, _):
  try:
    body = json.loads(event["body"])
    name = body.get("name")
    email = body.get("email")
    message = body.get("message")
    return processContactRequest(name, email, message)
  except ClientError as err:
      handle_client_error(err)