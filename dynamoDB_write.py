import json
import boto3
import uuid

dynamodb = boto3.resource('dynamodb')
table_name = 'vdirken'
table = dynamodb.Table(table_name)

def lambda_handler(event, context):
    try:
        # json.loads(event).content.decode('utf-8') 
        # Don't need to json.loads(json_data) as it is already a python dict, we just need to output this dict directly.
        
        request_body = event 
        name = request_body['name']
        email = request_body['email']
        message = request_body['message']

        # Generate unique messageID using UUID
        message_id = str(uuid.uuid4())

        # Save form data to DynamoDB
        item = {
            'messageID': message_id,
            'name': name,
            'email': email,
            'message': message
        }
        table.put_item(Item=item)

        return {
            'statusCode': 200,
            'body': json.dumps({'message': 'Form data saved successfully'})
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'message': 'An error occurred while saving the form data: '+ str(e)})
        }
