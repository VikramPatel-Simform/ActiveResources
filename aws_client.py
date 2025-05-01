from dotenv import load_dotenv
import os
import boto3

# Load environment variables from .env file
load_dotenv()

# Create boto3 client with all credentials including session token
def get_boto3_client(service_name , region):
    return boto3.client(
        service_name,
        aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
        aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
        aws_session_token=os.getenv('AWS_SESSION_TOKEN'),
        region_name= region
    )