import boto3
import json
import os
from src.http_response import create_response

dynamodb = boto3.resource('dynamodb')

def createStudent(student):
  table = dynamodb.Table(os.environ.get("STUDENTS_TABLE"))
  table.put_item(Item=student)
  return create_response(201, json.dumps({"message": "Student created successfully", "student": student}))
