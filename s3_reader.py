from os import getenv, remove
import logging
import boto3
from botocore.exceptions import NoCredentialsError

S3_BUCKET_NAME = getenv('s3_bucket_name')

def read_file_from_s3(file_key, local_path):
    # Initialize a session using the provided AWS credentials
    session = boto3.Session(
        aws_access_key_id=getenv('aws_access_key_id'),
        aws_secret_access_key=getenv('aws_secret_access_key'),
    )

    # Create an S3 client using the session
    s3 = session.client('s3')
    try:
        response = s3.get_object(Bucket=S3_BUCKET_NAME, Key=file_key)
        file_content = response['Body'].read()

        # Write the file content to the local file system
        with open(local_path, 'wb') as file:
            file.write(file_content)

        return local_path
    except NoCredentialsError:
        print("Credentials not available")
        return None

def delete_os_file(file_path):
    try:
        remove(file_path)
        logging.info(f"File {file_path} deleted successfully.")
    except FileNotFoundError:
        logging.info(f"File {file_path} not found.")
    except Exception as e:
        logging.info(f"Error deleting file {file_path}: {e}")