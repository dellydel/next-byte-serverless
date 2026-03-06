from src.error_handler import handle_client_error
from botocore.exceptions import ClientError
from src.registration import getRegistrationByEmail
from src.courses import getAllCourses, get_course_by_id 

def handler(event, _):
  try:
    query_params = event.get('queryStringParameters') or {}
    if query_params.get('email'):
      return getRegistrationByEmail(query_params.get('email'))
    elif query_params.get('courseId'):
      course_id = query_params.get('courseId')
      return get_course_by_id(course_id)
    else:
      return getAllCourses()

  except ClientError as err:
      return handle_client_error(err)