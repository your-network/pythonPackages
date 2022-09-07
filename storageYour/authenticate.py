import boto3

def getStorageClient(ACCESS_KEY, SECRET_KEY):
    storage_client = boto3.client('s3', aws_access_key_id=ACCESS_KEY, aws_secret_access_key=SECRET_KEY)
    return storage_client

def getAmazonClient(S3_ACCESS_KEY,S3_SECRET_KEY):
    s3_client = boto3.client('s3', aws_access_key_id=S3_ACCESS_KEY, aws_secret_access_key=S3_SECRET_KEY)
    return s3_client
