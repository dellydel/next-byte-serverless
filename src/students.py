import boto3
import json
import os
from src.http_response import create_response
from boto3.dynamodb.types import TypeDeserializer

dynamodb = boto3.client('dynamodb')
deserializer = TypeDeserializer()

def createStudent(student):
  table_name = os.environ.get("STUDENTS_TABLE")
  dynamodb_resource = boto3.resource('dynamodb')
  table = dynamodb_resource.Table(table_name)
  table.put_item(Item=student)
  return create_response(201, json.dumps({"message": "Student created successfully", "student": student}))

def getStudents(student_id=None, email=None):
  table_name = os.environ.get("STUDENTS_TABLE")
  
  if student_id:
    response = dynamodb.get_item(
      TableName=table_name,
      Key={'id': {'S': student_id}}
    )
    if 'Item' in response:
      student = {k: deserializer.deserialize(v) for k, v in response['Item'].items()}
      return create_response(200, json.dumps(student))
    return create_response(404, json.dumps({"message": "Student not found"}))
  
  if email:
    response = dynamodb.query(
      TableName=table_name,
      IndexName='EmailIndex',
      KeyConditionExpression='email = :email',
      ExpressionAttributeValues={':email': {'S': email}}
    )
    students = [{k: deserializer.deserialize(v) for k, v in item.items()} for item in response.get('Items', [])]
    return create_response(200, json.dumps(students))
  
  response = dynamodb.scan(TableName=table_name)
  students = [{k: deserializer.deserialize(v) for k, v in item.items()} for item in response.get('Items', [])]
  return create_response(200, json.dumps(students))
