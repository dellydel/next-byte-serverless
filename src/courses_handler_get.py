from src.error_handler import handle_client_error
from botocore.exceptions import ClientError
from src.registration import getRegistrationByEmail
from src.courses import getAllCourses 

def handler(event, _):
  try:
    if not event.get('queryStringParameters') or not event.get('queryStringParameters').get('email'):
      return getAllCourses()
    else:
      email = event.get('queryStringParameters').get('email')
      return getRegistrationByEmail(email)   

  except ClientError as err:
      return handle_client_error(err)