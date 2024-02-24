import json
import boto3

dynamodb = boto3.resource('dynamodb')
table_name = 'vdirken_users'
table = dynamodb.Table(table_name)

def lambda_handler(event, context):
    
    response = table.scan()
    items = response['Items']
    return {
                    'statusCode': 200,
                    'body': json.dumps({'message': 'Items retrieved successfully', 'items': items})
            }
    
