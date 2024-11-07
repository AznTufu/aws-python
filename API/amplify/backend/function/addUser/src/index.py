import os
import boto3

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
    
    user_email = event.get('email')
    user_id = event.get('user_id')
    hash_value = event.get('hash_value')
    
    if not user_email or not user_id:
        raise CustomException("Missing user_id or email in the request body", 400)
    
    try:
        table.put_item(Item={
            'id': user_id,
            'email': user_email,
            'hash_value': hash_value
        })
        raise CustomException("User added successfully", 200)
    except Exception as e:
        raise CustomException(f"Error adding user: {str(e)}", 500)
