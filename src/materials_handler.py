from botocore.exceptions import ClientError
from src.error_handler import handle_client_error
from src.materials import get_course_materials

def handler(event, context):
    query_params = event.get('queryStringParameters', {})
    topic = query_params.get('topic')
    try:
        return get_course_materials(topic)
    except ClientError as err:
      handle_client_error(err)

