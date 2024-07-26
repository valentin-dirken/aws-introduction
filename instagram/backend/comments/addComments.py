import json
import boto3

# Initialize the DynamoDB client
dynamodb_client = boto3.client('dynamodb')

# Constants
DYNAMODB_TABLE = 'vdirken-instagram'  # Replace with your actual DynamoDB table

def lambda_handler(event, context):
    try:
        # Extract the publicationID and comment from the request body
        body = json.loads(event['body'])
        publication_id = body['publicationID']
        comment_text = body['comment']

        # Update the DynamoDB item to add the new comment
        response = dynamodb_client.update_item(
            TableName=DYNAMODB_TABLE,
            Key={'publicationID': {'S': publication_id}},
            UpdateExpression="SET Comments = list_append(if_not_exists(Comments, :empty_list), :new_comment)",
            ExpressionAttributeValues={
                ':new_comment': {'L': [{'S': comment_text}]},
                ':empty_list': {'L': []}
            }
        )
        
        return {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps({'message': 'Comment added successfully'})
        }

    except Exception as e:
        print("Error: ", str(e))
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }
