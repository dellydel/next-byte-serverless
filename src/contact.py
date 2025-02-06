import boto3
import json
import os
import datetime
import uuid
from src.http_response import create_response
from time import time
dynamodb = boto3.resource('dynamodb')
sns = boto3.client('sns')

def processContactRequest (name, email, message):
  table = dynamodb.Table(os.environ.get("CONTACT_TABLE"))
  table.put_item(
      Item={
        'id': str(uuid.uuid4()),
        'name': name,
        'email': email,
        'message': message,
        'timestamp': int(time() * 1000)
      }
  )
  sendContactEmailNotification()
  return create_response(
    200,
    json.dumps({"message": "Success! Your message has been sent."} )
  )

def sendContactEmailNotification(): 
   sns.publish(
    TopicArn=os.environ.get("CONTACT_TOPIC"),
    Message="A new contact / more informtion request has been submitted",
  )

