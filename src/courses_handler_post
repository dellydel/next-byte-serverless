import json
from src.http_response import create_response
from src.courses import get_courses_by_id

def handler(event, _):
    try:
        body = json.loads(event['body'])
        course_ids = body['courseIds']
        
        if not course_ids:
            return create_response(200, [])
            
        return get_courses_by_id(course_ids)
    except (KeyError, json.JSONDecodeError):
        return create_response(400, {"message": "Invalid request body"})
