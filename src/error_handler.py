from src.http_response import create_response
import json

def handle_client_error(err):
    statusCode = err.response['Error']['Code'] if hasattr(err, 'response') else 500
    message = err.response['Error']['Message'] if hasattr(err, 'response') else 'Internal Server Error'
    return create_response(statusCode, json.dumps({"message": message}))   