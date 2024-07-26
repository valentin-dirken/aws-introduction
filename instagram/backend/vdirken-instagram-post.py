import json
import boto3
import base64
import uuid
from datetime import datetime

s3_client = boto3.client('s3')
dynamodb_client = boto3.client('dynamodb')

S3_BUCKET = 'vdirken-instagram'
DYNAMODB_TABLE = 'vdirken-instagram'
def lambda_handler(event, context):
    try:
         # Log the incoming event for debugging
        print("Received event: " + json.dumps(event, indent=2))

        # Check if the event has a body key or if it directly contains the payload
        if 'body' in event:
            body = json.loads(event['body'])
        else:
            body = event
        caption = body.get('caption')
        location = body.get('location')
        image_data = body.get('image')
        image_filename = body.get('filename')

        if not all([caption, image_data, image_filename]):
            raise ValueError("Missing one or more required fields: caption, image, filename")

        # Generate a unique publication ID and a filename
        publication_id = str(uuid.uuid4())
        image_filename = f"{publication_id}_{image_filename}"

        # Decode the base64 image
        image_bytes = base64.b64decode(image_data)

        # Upload the image to S3
        s3_client.put_object(
            Bucket=S3_BUCKET,
            Key=image_filename,
            Body=image_bytes,
            ContentType='image/jpeg'  
        )

        # Store metadata in DynamoDB
        dynamodb_client.put_item(
            TableName=DYNAMODB_TABLE,
            Item={
                'publicationID': {'S': publication_id},
                'Caption': {'S': caption},
                'Location': {'S': location},
                'ImageFilename': {'S': image_filename},
                'Timestamp': {'S': datetime.utcnow().isoformat()}
            }
        )

        return {
            'statusCode': 200,
            'body': json.dumps('Upload successful!')
        }

    except Exception as e:
        print("Error: ", str(e))
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }
