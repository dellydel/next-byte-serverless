# Description: This file contains the logic to retrieve all courses from the database.
import os
import boto3
import logging
from src.http_response import create_response
from botocore.exceptions import ClientError
from src.http_response import create_response
from src.utils.unmarshall import deserialize

logger = logging.getLogger()
logger.setLevel(logging.INFO) 

dynamodb = boto3.client('dynamodb')
tableName=os.environ.get("COURSES_TABLE")

def getAllCourses():
  logger.info("Starting getAllCourses function")
  response = dynamodb.scan(
    TableName=tableName,
  )
  try:
      items = response.get("Items", []) 
      logger.info(f"Successfully retrieved {len(items)} courses")
      logger.debug(f"Items: {items}")       
      deserialized_items = [deserialize(item) for item in items]
      logger.debug(f"Deserialized Items: {deserialized_items}") 
      return create_response(200, deserialized_items)
  except ClientError as e:
      logger.error(f"Error retrieving courses: {str(e)}")
      return create_response(500, f"Error retrieving courses: {str(e)}")
  
def get_courses_by_id(course_ids):
    response = dynamodb.scan(
        TableName=tableName,
    )
    try:
        courses = deserialize(response)
        registered_courses = [
            course for course in courses.get("Items", [])
            if course.get("id") in course_ids
        ]
        return create_response(200, registered_courses)
    except ClientError as e:
        return create_response(500, f"Error retrieving courses: {str(e)}")