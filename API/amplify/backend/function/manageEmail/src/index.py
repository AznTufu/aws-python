import os
import boto3
import uuid
from boto3.dynamodb.conditions import Key
import json
import hashlib

class CustomException(Exception):
    def __init__(self, message, code):
        super().__init__(message)
        self.message = message
        self.code = code

    def to_dict(self):
        return {
            "statusCode": self.code,
            "body": self.message
        }
        
def handler(event, context):
    user_table_name = os.environ.get('STORAGE_USERS_NAME')
    dynamodb = boto3.resource('dynamodb', region_name='eu-west-1')
    table = dynamodb.Table(user_table_name)
    
    body = json.loads(event['body'])
    user_email = body.get('email')
    
    if not user_email:
        raise CustomException("Missing email in the request body", 400)

    res = table.query(
        IndexName='emails',
        KeyConditionExpression=Key('email').eq(user_email)
    )
    print(res)

    user_id = None
    hash_value = None
    
    if not res['Items']:
        user_id = str(uuid.uuid4())
        lambda_client = boto3.client('lambda', region_name='eu-west-1')
        hash_value = hashlib.sha256((user_id + user_email).encode()).hexdigest()
        
        try:
            lambda_client.invoke(
                FunctionName= os.environ.get('FUNCTION_ADDUSER_NAME'),
                InvocationType='Event',
                Payload=json.dumps({
                    'email': user_email,
                    'user_id': user_id,
                    'hash_value': hash_value
                })
            )
        except Exception as e:
            print(f"Error invoking addUser Lambda: {e}")
            raise CustomException(f"Error invoking addUser Lambda: {str(e)}", 500)
    else:
        user_id = res['Items'][0].get('id')
        hash_value = res['Items'][0].get('hash_value')
        print("User already exists")

    return {
        "statusCode": 200,
        "body": json.dumps({
            "user_id": user_id,
            "email": user_email,
            "hash_value": hash_value
        })
    }
