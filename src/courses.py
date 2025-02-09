# Description: This file contains the logic to retrieve all courses from the database.
import os
import boto3
from src.http_response import create_response
from botocore.exceptions import ClientError
from src.http_response import create_response
from src.utils.unmarshall import deserialize

dynamodb = boto3.client('dynamodb')
tableName=os.environ.get("COURSES_TABLE")

def getAllCourses():
  response = dynamodb.scan(
    TableName=tableName,
  )
  try:
      courses = deserialize(response)
      print(courses)
      return create_response(200, courses.get("Items"))
  except:
      raise ClientError("Error when attempting to retrieve courses.")
  
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
        raise ClientError(f"Error when attempting to retrieve courses: {str(e)}")