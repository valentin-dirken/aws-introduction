from boto3.dynamodb.conditions import Key, Attr

# ....

# <Fix> when the DynamoDB field is Decimal : Object of type Decimal is not JSON serializable
from decimal import *
class JSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Decimal):
            return float(obj)
        return json.JSONEncoder.default(self, obj)
# </Fix>




def lambda_handler(event, context):
  # ...
  category = "chairs"
  try:
    response = table.scan(FilterExpression=Attr('furniture_type').eq(category))
    items = response['Items']
    return {
                    'statusCode': 200,
                    'body': json.dumps({'message': 'Items retrieved successfully', 'items': items}, cls=JSONEncoder)
            }
  except Exception as e:
    print(f"Error accessing DynamoDB: {str(e)}")
