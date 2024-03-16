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
table_name = 'ppp_clients_table'
table = dynamodb.Table(table_name)

def lambda_handler(event, context):

    try:
        
        # Retrieve the item ID to read from the query parameters
        clientsID = event.get("params", {}).get("clientsID")
        print(clientsID)

        # If an ID is provided, read the specific item
        if clientsID:
            response = table.get_item(Key={'clientsID': clientsID})
            if 'Item' in response:
                item = response['Item']
                return {
                    'statusCode': 200,
                    'body': json.dumps({'message': 'Item retrieved successfully', 'item': item})
                }
            else:
                return {
                    'statusCode': 404,
                    'body': json.dumps({'message': 'Item not found'})
                }
        else:
            # Retrieve all items from the DynamoDB table
            response = table.scan()
            if 'Items' in response:
                items = response['Items']
                return {
                    'statusCode': 200,
                    'body': json.dumps({'message': 'Items retrieved successfully', 'items': items}, cls=JSONEncoder)
                }
            else:
                return {
                    'statusCode': 404,
                    'body': json.dumps({'message': 'No items found'})
                }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'message': 'An error occurred', 'error': str(e)})
        }
