from botocore.exceptions import ClientError
from src.error_handler import handle_client_error
from src.registration import createCourseRegistration, createFreeCourseRegistration
import json

def handler(event, _):
  try:
    body = json.loads(event["body"])
    if body.get("price") == "0":
      return createFreeCourseRegistration(body)
    return createCourseRegistration(body)
  except ClientError as err:
      handle_client_error(err)