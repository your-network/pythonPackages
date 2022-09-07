from botocore.exceptions import ClientError
import csv
from io import StringIO, BytesIO

def uploadCsv(storageClient: object,
              bucket: str,
              file_name: str,
              data) -> bool:

    field_separator = ","
    csv_buffer = StringIO()
    data.to_csv(csv_buffer, sep=field_separator, quotechar='"', doublequote=True, quoting=csv.QUOTE_ALL,
                escapechar=None, index=False)
    # Upload the file
    try:
        response = storageClient.put_object(ACL='public-read',
                                             Body=csv_buffer.getvalue(),
                                             Bucket=bucket,
                                             Key=file_name)
        return True
    except ClientError as e:
        print(e)
        return False


def uploadBytesMedia(storageClient: object,
                     bucket: str, media_bytes,
                     media_name: str,
                     content_type: str,
                     msg_handler: object) -> bool:

    try:
        media_bytes.seek(0)
        # Upload image to s3
        storageClient.upload_fileobj(
            media_bytes,
            bucket,
            media_name,
            ExtraArgs={'ContentType': content_type, 'ACL': "public-read"}
        )
        ## logging
        msg_handler.logStruct(topic=f"uploadBytesMedia: media name: {media_name}, object uploaded",
                              level="DEBUG",
                              labels={"function": "uploadBytesMedia"})
        return True

    except ClientError as e:
        ## logging
        msg_handler.logStruct(topic=f"uploadBytesMedia: media name: {media_name}, error",
                              error_message=str(e),
                              level="ERROR",
                              labels={"function": "uploadBytesMedia"})
        return False
