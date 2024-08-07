import json
import boto3
import uuid

dynamodb = boto3.resource('dynamodb')
table_name = 'vdirken-books'
table = dynamodb.Table(table_name)

def lambda_handler(event, context):
    try:
        # json.loads(event).content.decode('utf-8') 
        # Don't need to json.loads(json_data) as it is already a python dict, we just need to output this dict directly.
        
        request_body = event 
        isbn = request_body['isbn']
        bookName = request_body['bookName']



        # Save form data to DynamoDB
        item = {
            'isbn': isbn,
            'bookName': bookName
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
