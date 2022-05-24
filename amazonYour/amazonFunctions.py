from botocore.exceptions import ClientError
import boto3
import csv
from io import StringIO, BytesIO

class amazon:
    S3_ACCESS_KEY = 'AKIA5RELSNU5H4KJHZXQ'
    S3_SECRET_KEY = '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'
    s3_client = boto3.client('s3', aws_access_key_id=S3_ACCESS_KEY, aws_secret_access_key=S3_SECRET_KEY)

    def uploadCsv(self, bucket, file_name, data):
        field_separator = ","
        csv_buffer = StringIO()
        data.to_csv(csv_buffer, sep=field_separator, quotechar='"', doublequote=True, quoting=csv.QUOTE_ALL, escapechar=None, index=False)
        # Upload the file
        try:
            response = self.s3_client.put_object(ACL='public-read',
                                            Body=csv_buffer.getvalue(),
                                            Bucket=bucket,
                                            Key=file_name)
            return True
        except ClientError as e:
            print(e)
            return False

    def uploadBytesImage(self, bucket, image_name, image):
        try:
            in_mem_file = BytesIO()
            image.save(in_mem_file, format=image.format)
            in_mem_file.seek(0)
            # Upload image to s3
            self.s3_client.upload_fileobj(
                in_mem_file,
                bucket,
                image_name,
                ExtraArgs={
                    'ACL': 'public-read'
                }
            )
            return True
        except ClientError as e:
            print(e)
            return False
