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


def uploadBytesMedia(amazonS3Client, bucket, media_bytes, media_name, content_type):
    try:
        media_bytes.seek(0)
        # Upload image to s3
        amazonS3Client.upload_fileobj(
            media_bytes,
            bucket,
            media_name,
            ExtraArgs={'ContentType': content_type, 'ACL': "public-read"}
        )
        # print(f"Media name: {media_name}, uploaded to amazon")
        return True
    except ClientError as e:
        print(e)
        return False
