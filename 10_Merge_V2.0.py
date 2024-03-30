import boto3
import json
from decimal import Decimal

# Custom JSON encoder to handle Decimal objects
class JSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Decimal):
            return float(obj)  # Convert Decimal to float for JSON serialization
        return json.JSONEncoder.default(self, obj)

# Create a DynamoDB resource
dynamodb = boto3.resource('dynamodb')

def lambda_handler(event, context):
    try:
        # Scan data from the 'users' table
        users_response = dynamodb.Table('users').scan()
        users_items = users_response['Items']
        print(users_items)
        print("USERS SCANNED")  # Print the retrieved items from 'users' table
    except dynamodb.meta.client.exceptions.DynamoDBError as e:
        # Handle exceptions when scanning 'users' table
        print("ERROR: Unexpected error: Could not scan 'users' table.")
        print(e)
        return {
            'statusCode': 500,
            'body': str(e)
        }

    try:
        # Scan data from the 'movies' table
        movies_response = dynamodb.Table('movies').scan()
        movies_items = movies_response['Items']
        print("MOVIES SCANNED")  # Print the retrieved items from 'movies' table
    except dynamodb.meta.client.exceptions.DynamoDBError as e:
        # Handle exceptions when scanning 'movies' table
        print("ERROR: Unexpected error: Could not scan 'movies' table.")
        print(e)
        return {
            'statusCode': 500,
            'body': str(e)
        }

    try:
        # Scan data from the 'reviews' table
        reviews_response = dynamodb.Table('reviews').scan()
        reviews_items = reviews_response['Items']
        print("REVIEWS SCANNED")  # Print the retrieved items from 'reviews' table
    except dynamodb.meta.client.exceptions.DynamoDBError as e:
        # Handle exceptions when scanning 'reviews' table
        print("ERROR: Unexpected error: Could not scan 'reviews' table.")
        print(e)
        return {
            'statusCode': 500,
            'body': str(e)
        }

    # Perform in-memory join
    joined_results = []
    for reviews_item in reviews_items:
        # Extract the movie_id and user_id from the current reviews_item
        review_movie_id = reviews_item.get('movie_id')
        review_user_id = reviews_item.get('user_id')
        print(f"WARNING: --- Review ITEM ---")
        print(f"WARNING: USER ID - {review_user_id} ")
        print(f"WARNING: MOVIE ID - {review_movie_id} ")
        print(f"WARNING: </--- Review ITEM --- >")
    
        # Skip if movie_id or user_id is None
        if review_movie_id is None or review_user_id is None:
            print("ERROR: review_movie_id or review_user_id not found in the item from 'reviews' table.")
            continue
    
        # Find user details
        user_details = None
        print(users_items)
        for user_item in users_items:
            print(user_item)
            if user_item['user_id'] == review_user_id:
                user_details = user_item
                break
        
        if user_details is None:
            print(f"ERROR: User details not found for review_user_id: {review_user_id}")
            continue
    
        # Find movie details
        movie_details = None
        for movie_item in movies_items:
            if movie_item['movie_id'] == review_movie_id:
                movie_details = movie_item
                break
        
        if movie_details is None:
            print(f"ERROR: Movie details not found for review_movie_id: {review_movie_id}")
            continue
    
        # Merge user and movie details
        joined_result = {**user_details, **movie_details}
        joined_results.append(joined_result)

    return {
        'statusCode': 200,
        'body': json.dumps({'message': 'Items retrieved successfully', 'items': joined_results}, cls=JSONEncoder)
    }
