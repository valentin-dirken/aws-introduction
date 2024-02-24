import json
import boto3

# <Fix> when the DynamoDB field is Decimal : Object of type Decimal is not JSON serializable
from decimal import *
class JSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Decimal):
            return float(obj)
        return json.JSONEncoder.default(self, obj)
# </Fix>



dynamodb = boto3.resource('dynamodb')
table_name = 'vdirken_users'
table = dynamodb.Table(table_name)

def lambda_handler(event, context):
    
    response = table.scan()
    items = response['Items']
    return {
                    'statusCode': 200,
                    'body': json.dumps({'message': 'Items retrieved successfully', 'items': items}, cls=JSONEncoder)
            }
