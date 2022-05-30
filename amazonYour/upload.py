from botocore.exceptions import ClientError
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


def uploadBytesMedia(s3_client, bucket, media_name, media):
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