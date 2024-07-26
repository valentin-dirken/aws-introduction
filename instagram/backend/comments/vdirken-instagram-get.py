import json
import boto3
from datetime import datetime, timedelta

# Initialize clients for DynamoDB and S3
dynamodb_client = boto3.client('dynamodb')
s3_client = boto3.client('s3')

# Constants
DYNAMODB_TABLE = 'vdirken-instagram'
S3_BUCKET_NAME = 'vdirken-instagram'
BRUSSELS_UTC_OFFSET = timedelta(hours=2)  # Brussels is UTC+2 in standard time

def lambda_handler(event, context):
    try:
        response = dynamodb_client.scan(TableName=DYNAMODB_TABLE)
        items = response.get('Items', [])

        results = []
        for item in items:
            publication_id = item['publicationID']['S']
            image_filename = item['ImageFilename']['S']

            signed_url = s3_client.generate_presigned_url(
                'get_object',
                Params={'Bucket': S3_BUCKET_NAME, 'Key': image_filename},
                ExpiresIn=3600
            )

            timestamp_str = item['Timestamp']['S']
            timestamp_utc = datetime.fromisoformat(timestamp_str.replace('Z', '+00:00'))
            timestamp_brussels = timestamp_utc + BRUSSELS_UTC_OFFSET

            # Extract comments
            comments = item.get('Comments', {}).get('L', [])
            comments_list = [c['S'] for c in comments]

            results.append({
                'publicationID': publication_id,
                'caption': item['Caption']['S'],
                'location': item['Location']['S'],
                'imageFilename': image_filename,
                'timestamp': timestamp_brussels.isoformat(),
                'imageUrl': signed_url,
                'comments': comments_list  # Include comments in the result
            })

        results.sort(key=lambda x: x['timestamp'], reverse=True)

        return {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps(results)
        }

    except Exception as e:
        print("Error: ", str(e))
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }
