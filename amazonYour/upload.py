from botocore.exceptions import ClientError
import boto3
import csv
from io import StringIO, BytesIO

def uploadCsv(s3_client, bucket, file_name, data):
    field_separator = ","
    csv_buffer = StringIO()
    data.to_csv(csv_buffer, sep=field_separator, quotechar='"', doublequote=True, quoting=csv.QUOTE_ALL,
                escapechar=None, index=False)
    # Upload the file
    try:
        response = s3_client.put_object(ACL='public-read',
                                             Body=csv_buffer.getvalue(),
                                             Bucket=bucket,
                                             Key=file_name)
        return True
    except ClientError as e:
        print(e)
        return False


def uploadBytesMedia(s3_client, bucket, media, media_name):
    try:
        in_mem_file = BytesIO()
        media.save(in_mem_file, format=media.format)
        in_mem_file.seek(0)
        # Upload image to s3
        s3_client.upload_fileobj(
            in_mem_file,
            bucket,
            media_name,
            ExtraArgs={
                'ACL': 'public-read'
            }
        )
        return True
    except ClientError as e:
        print(e)
        return False


def uploadMediaFile(amazonS3Client, bucket, request_response, media_name):
    try:
        with request_response as part:
            part.raw.decode_content = True
            conf = amazonS3Client.transfer.TransferConfig(multipart_threshold=10000, max_concurrency=4)
            amazonS3Client.upload_fileobj(part.raw, bucket, media_name, Config=conf)
        return True

    except ClientError as e:
        print(e)
        return False
