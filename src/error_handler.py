from src.http_response import create_response
import json

def handle_client_error(err):
    statusCode = err.statusCode if hasattr(err, 'statusCode') else 500
    message = err.message if hasattr(err, 'message') else 'Internal Server Error'
    return create_response(statusCode, message)   