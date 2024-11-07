from requests import HTTPError
from http import HTTPStatus
from functools import wraps
import os
import boto3

def exception_handler(func):
    @wraps(func)
    def wrapper(event, context):
        print(event)
        response = {}
        try:
            if not event['headers'].get('x-api-key'):
                raise PermissionError('x-api-key is invalid')
            res = func(event, context)
            if res:
                response['body'] = res
            response['statusCode'] = HTTPStatus.OK
        except HTTPError as e:
            response['body'] = e.response
            response['statusCode'] = e.response.status_code
        except PermissionError as e:
            response['body'] = str(e)
            response['statusCode'] = HTTPStatus.FORBIDDEN
        except Exception as e:
            response['body'] = str(e)
            response['statusCode'] = HTTPStatus.INTERNAL_SERVER_ERROR
        return response
    return wrapper

@exception_handler
def handler(event, context):
    if not event.get('httpMethod') == 'GET':
        raise ValueError('Method not allowed')
    
    user_table_name = os.environ.get('STORAGE_USERS_NAME')
    dynamodb = boto3.resource('dynamodb', region_name='eu-west-1')
    table = dynamodb.Table(user_table_name)

    user_id = event['headers']['x-api-key']
    res = table.get_item( Key= { 'id': user_id })   

    data = res.get('Item')
    print(data)
    if not data:
        raise ValueError('User not found')

    return data['email']
