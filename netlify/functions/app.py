from app import app
from flask import Request
import json

def handler(event, context):
    """Netlify Function handler for Flask app"""
    with app.test_client() as client:
        # Convert Netlify event to Flask request
        method = event.get('httpMethod', 'GET')
        path = event.get('path', '/')
        headers = event.get('headers', {})
        body = event.get('body', '')
        
        if method == 'GET':
            response = client.get(path, headers=headers)
        elif method == 'POST':
            response = client.post(path, data=body, headers=headers)
        elif method == 'PUT':
            response = client.put(path, data=body, headers=headers)
        elif method == 'DELETE':
            response = client.delete(path, headers=headers)
        else:
            response = client.open(path, method=method, data=body, headers=headers)
        
        return {
            'statusCode': response.status_code,
            'headers': dict(response.headers),
            'body': response.get_data(as_text=True)
        }
