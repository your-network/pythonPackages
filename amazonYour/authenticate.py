from botocore.exceptions import ClientError
import boto3
import csv
from io import StringIO, BytesIO

def getAmazonClient(S3_ACCESS_KEY,S3_SECRET_KEY):
    s3_client = boto3.client('s3', aws_access_key_id=S3_ACCESS_KEY, aws_secret_access_key=S3_SECRET_KEY)
    return s3_client
