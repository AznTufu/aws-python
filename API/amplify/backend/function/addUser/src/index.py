import os
import boto3
import hashlib
import json

def handler(event, context):
    user_table_name = os.environ.get('STORAGE_USERS_NAME')
    dynamodb = boto3.resource('dynamodb', region_name='eu-west-1')
    table = dynamodb.Table(user_table_name)
    
    user_email = event.get('email')
    user_id = event.get('user_id')
    hash_value = event.get('hash_value')
    
    if not user_email or not user_id:
        return {
            "statusCode": 400,
            "body": "Missing user_id or email in the request body"
        }
    
    try:
        table.put_item(Item={
            'id': user_id,
            'email': user_email,
            'hash_value': hash_value
        })
        return {
            "statusCode": 200,
            "body": json.dumps({
                "message": "User added successfully"
            })
        }
    except Exception as e:
        return {
            "statusCode": 500,
            "body": f"Error adding user: {str(e)}"
        }
