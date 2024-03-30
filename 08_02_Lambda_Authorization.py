import base64

def lambda_handler(event, context):
    # Dictionary of authorized users with their authentication information
    users = {
        "vdirken": {"password": "ULB"},
        "user2": {"password": "password2"}
    }
    
    # Retrieve authentication information from the HTTP header
    auth = event['headers'].get('Authorization')
    
    # Check if authentication is present and correct
    if auth:
        auth_parts = auth.split()
        if len(auth_parts) == 2 and auth_parts[0].lower() == 'basic':
            # Decode authentication information
            username_password = base64.b64decode(auth_parts[1]).decode('utf-8').split(':')
            username = username_password[0]
            password = username_password[1]
            
            # Check if authentication information is valid
            if username in users and users[username]["password"] == password:
                # Authentication successful
                print("AUTHENTICATED")
                response = {
                    'statusCode': 200,
                    'body': 'Authentication successful!',
                    'headers': {
                        'Access-Control-Allow-Origin': '*'  # Allow requests from any domain
                    }
                }
                return response
    
    # Authentication failed
    return {
        'statusCode': 401,
        'body': 'Unauthorized access'
    }
