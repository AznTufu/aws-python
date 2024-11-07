import os
import boto3
import uuid
from boto3.dynamodb.conditions import Key
import json
import hashlib

def handler(event, context):
    user_table_name = os.environ.get('STORAGE_USERS_NAME')
    dynamodb = boto3.resource('dynamodb', region_name='eu-west-1')
    table = dynamodb.Table(user_table_name)
    
    body = json.loads(event['body'])
    user_email = body.get('email')
    
    if not user_email:
        return {"statusCode": 400, "body": "Missing email in the request body"}

    res = table.query(
        IndexName='emails',
        KeyConditionExpression=Key('email').eq(user_email)
    )
    print(res)
    
    if not res['Items']:
        user_id = str(uuid.uuid4())
        hash_value = hashlib.sha256((user_id + user_email).encode()).hexdigest()
        try:
            table.put_item(Item={
                    'id': user_id,
                    'email': user_email,
                    'hash_value': hash_value
                }
            )
            print("add new user")
        except Exception as e:
            print(f"Error: {e}")
    else:
        user_id = res['Items'][0].get('id')
        hash_value = res['Items'][0].get('hash_value')
        print("user already exists")

    return {
        "statusCode": 200,
        "body": json.dumps({
            "user_id": user_id,
            "email": user_email,
            "hash_value": hash_value
        })
    }