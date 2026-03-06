# Description: This file contains the logic to retrieve all courses from the database.
import os
import boto3
import logging
from src.http_response import create_response
from botocore.exceptions import ClientError
from src.http_response import create_response

logger = logging.getLogger()
logger.setLevel(logging.INFO) 

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(os.environ.get("COURSES_TABLE"))

def getAllCourses():
  logger.info("Starting getAllCourses function")
  try:
      response = table.scan()
      items = response.get("Items", []) 
      logger.info(f"Successfully retrieved {len(items)} courses")
      logger.debug(f"Items: {items}")       
      return create_response(200, items)
  except ClientError as e:
      logger.error(f"Error retrieving courses: {str(e)}")
      return create_response(500, f"Error retrieving courses: {str(e)}")
  
def get_course_by_id(course_id):
    try:
        response = table.get_item(Key={'id': course_id})
        if 'Item' in response:
            return create_response(200, response['Item'])
        return create_response(404, {"message": "Course not found"})
    except ClientError as e:
        return create_response(500, f"Error retrieving courses: {str(e)}")