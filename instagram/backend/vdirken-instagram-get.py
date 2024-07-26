import json
import boto3

# Initialize clients for DynamoDB and S3
dynamodb_client = boto3.client('dynamodb')
s3_client = boto3.client('s3')

# Constants
DYNAMODB_TABLE = 'vdirken-instagram'  # Replace with your actual DynamoDB table
S3_BUCKET_NAME = 'vdirken-instagram'  # Replace with your actual S3 bucket name

def lambda_handler(event, context):
    try:
        # Scan the DynamoDB table
        response = dynamodb_client.scan(
            TableName=DYNAMODB_TABLE
        )
        
        items = response.get('Items', [])
        
        # Transform the items to be JSON serializable
        results = []
        for item in items:
            publication_id = item['publicationID']['S']
            image_filename = item['ImageFilename']['S']
            
            # Generate a signed URL for the image
            signed_url = s3_client.generate_presigned_url(
                'get_object',
                Params={
                    'Bucket': S3_BUCKET_NAME,
                    'Key': image_filename
                },
                ExpiresIn=3600  # URL expiration time in seconds
            )
            
            results.append({
                'publicationID': publication_id,
                'caption': item['Caption']['S'],
                'location': item['Location']['S'],
                'imageFilename': image_filename,
                'timestamp': item['Timestamp']['S'],
                'imageUrl': signed_url  # Add signed URL to the result
            })
        
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
