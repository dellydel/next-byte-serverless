from botocore.exceptions import ClientError
from src.error_handler import handle_client_error
from src.students import getStudents

def handler(event, _):
  try:
    path_params = event.get('pathParameters') or {}
    query_params = event.get('queryStringParameters') or {}
    student_id = path_params.get('id')
    email = query_params.get('email')
    return getStudents(student_id, email)
  except ClientError as err:
      handle_client_error(err)
