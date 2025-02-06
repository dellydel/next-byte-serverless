from src.error_handler import handle_client_error
from botocore.exceptions import ClientError
from src.registration import getRegistrationByEmail 

def handler(event, _):
  try:
    query_params = event.get('queryStringParameters', {})
    email = query_params.get('email')
    return  getRegistrationByEmail(email)
  except ClientError as err:
      handle_client_error(err)