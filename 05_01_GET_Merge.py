import boto3  # Import the boto3 library for AWS SDK
import json   # Import the json library for JSON manipulation
from decimal import Decimal  # Import Decimal class from decimal module for handling Decimal objects

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
        # Scan data from the 'veterinaires' table
        veterinaires_response = dynamodb.Table('veterinaires').scan()
        veterinaires_items = veterinaires_response['Items']
        print(veterinaires_items)  # Print the retrieved items from 'veterinaires' table
    except dynamodb.meta.client.exceptions.DynamoDBError as e:
        # Handle exceptions when scanning 'veterinaires' table
        print("ERROR: Unexpected error: Could not scan 'veterinaires' table.")
        print(e)
        return {
            'statusCode': 500,
            'body': str(e)
        }

    try:
        # Scan data from the 'hospitals' table
        hospitals_response = dynamodb.Table('hospitals').scan()
        hospitals_items = hospitals_response['Items']
        print(hospitals_items)  # Print the retrieved items from 'hospitals' table
    except dynamodb.meta.client.exceptions.DynamoDBError as e:
        # Handle exceptions when scanning 'hospitals' table
        print("ERROR: Unexpected error: Could not scan 'hospitals' table.")
        print(e)
        return {
            'statusCode': 500,
            'body': str(e)
        }

    try:
        # Scan data from the 'vets-hospitals' table
        vets_hospitals_response = dynamodb.Table('vets-hospitals').scan()
        vets_hospitals_items = vets_hospitals_response['Items']
        print(vets_hospitals_items)  # Print the retrieved items from 'vets-hospitals' table
    except dynamodb.meta.client.exceptions.DynamoDBError as e:
        # Handle exceptions when scanning 'vets-hospitals' table
        print("ERROR: Unexpected error: Could not scan 'vets-hospitals' table.")
        print(e)
        return {
            'statusCode': 500,
            'body': str(e)
        }

    # Perform in-memory join
    joined_results = []
    for vets_hospital_item in vets_hospitals_items:
        # Iterate through each item in 'vets_hospitals_items'
        # Extract the value associated with the 'vetsID' key from the current item
        vetsID = vets_hospital_item['vetsID']
        # Use .get() method to safely extract the value associated with the 'hospiID' key from the current item
        # If 'hospiID' key is not present, hospiID will be None
        hospiID = vets_hospital_item.get('hospiID')

        if hospiID is None:
            # Handle the case where hospiID is not found in the item from 'vets-hospitals' table
            print("WARNING: hospiID not found in the item from 'vets-hospitals' table.")
            continue

        # Find veterinarian details
        vet_details = next((item for item in veterinaires_items if item['vetsID'] == vetsID), None)
        if vet_details:
            vet_details.pop('vetsID')  # Remove vetsID from veterinarian details

        # Find hospital details
        hospital_details = next((item for item in hospitals_items if item.get('hospiID') == hospiID), None)
        if hospital_details:
            hospital_details.pop('hospiID')  # Remove hospiID from hospital details

        # Merge veterinarian and hospital details
        joined_result = {**vet_details, **hospital_details}
        joined_results.append(joined_result)  # Append joined result to the list

    return {
        'statusCode': 200,
        'body': json.dumps({'message': 'Items retrieved successfully', 'items': joined_results}, cls=JSONEncoder)
    }
