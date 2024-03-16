import boto3
import json

# <Fix> when the DynamoDB field is Decimal : Object of type Decimal is not JSON serializable
from decimal import *
class JSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Decimal):
            return float(obj)
        return json.JSONEncoder.default(self, obj)
# </Fix>


# Création d'un client DynamoDB
dynamodb = boto3.client('dynamodb')

def lambda_handler(event, context):
    # Lecture des données depuis la table veterinaires
    try:
        veterinaires_response = dynamodb.scan(
            TableName='veterinaires'
        )
        veterinaires_items = veterinaires_response['Items']
    except dynamodb.exceptions.DynamoDBError as e:
        print("ERROR: Unexpected error: Could not scan 'veterinaires' table.")
        print(e)
        return {
            'statusCode': 500,
            'body': str(e)
        }

    # Lecture des données depuis la table hospitals
    try:
        hospitals_response = dynamodb.scan(
            TableName='hospitals'
        )
        hospitals_items = hospitals_response['Items']
    except dynamodb.exceptions.DynamoDBError as e:
        print("ERROR: Unexpected error: Could not scan 'hospitals' table.")
        print(e)
        return {
            'statusCode': 500,
            'body': str(e)
        }

    # Lecture des données depuis la table vets-hospitals
    try:
        vets_hospitals_response = dynamodb.scan(
            TableName='vets-hospitals'
        )
        vets_hospitals_items = vets_hospitals_response['Items']
        print(vets_hospitals_items)
    except dynamodb.exceptions.DynamoDBError as e:
        print("ERROR: Unexpected error: Could not scan 'vets-hospitals' table.")
        print(e)
        return {
            'statusCode': 500,
            'body': str(e)
        }

    # Réalisation de la jointure en mémoire
    joined_results = []
    for vets_hospital_item in vets_hospitals_items:
        vetsID = vets_hospital_item['vetsID']['S']
        hospiID = vets_hospital_item.get('hospiID', {}).get('S', None)

        if hospiID is None:
            print("WARNING: hospiID not found in the item from 'vets-hospitals' table.")
            continue

        # Recherche des détails du vétérinaire
        vet_details = next((item for item in veterinaires_items if item['vetsID']['S'] == vetsID), None)
        if vet_details:
            vet_details.pop('vetsID')

        # Recherche des détails de l'hôpital
        hospital_details = next((item for item in hospitals_items if item.get('hospiID', {}).get('S') == hospiID), None)
        if hospital_details:
            hospital_details.pop('hospiID')

        # Fusion des détails du vétérinaire et de l'hôpital
        joined_result = {**vet_details, **hospital_details}
        joined_results.append(joined_result)
    return {
        'statusCode': 200,
        'body': json.dumps({'message': 'Items retrieved successfully', 'items': joined_results}, cls=JSONEncoder)

    }
