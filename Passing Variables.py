'''
### Passing variables from AWS API Gateway to Lambda : ###

--- API Gateway ---
  GET clients/
   Create resource {clientsID}
   Add Method GET

In {clientsID} > GET > Integration Request > Edit > Mapping Templates

- Content type : application/json 

- Template body : 


{
  "body" : $input.json('$'),
  "headers": {
    #foreach($header in $input.params().header.keySet())
    "$header": "$util.escapeJavaScript($input.params().header.get($header))" #if($foreach.hasNext),#end

    #end
  },
  "method": "$context.httpMethod",
  "params": {
    #foreach($param in $input.params().path.keySet())
    "$param": "$util.escapeJavaScript($input.params().path.get($param))" #if($foreach.hasNext),#end

    #end
  },
  "query": {
    #foreach($queryParam in $input.params().querystring.keySet())
    "$queryParam": "$util.escapeJavaScript($input.params().querystring.get($queryParam))" #if($foreach.hasNext),#end

    #end
  }  
}


----

--- In the Lambda function associated : ---

'''

import json
import boto3

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
                    'body': json.dumps({'message': 'Items retrieved successfully', 'items': items})
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

