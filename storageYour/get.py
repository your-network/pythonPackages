from botocore.exceptions import ClientError
import csv
from io import StringIO, BytesIO
#
# def getFiles(storageService: object,
#               bucket: str,
#               folder: str) -> list:
#
#     ## upload details
#     my_bucket = storageService.Bucket("yourcontent-dev")
#     final_path = f"m{internal_path}"
#
#     objs = mybucket.objects.filter(
#         Prefix=bucket_prefix)
#
#     field_separator = ","
#     csv_buffer = StringIO()
#     data.to_csv(csv_buffer, sep=field_separator, quotechar='"', doublequote=True, quoting=csv.QUOTE_ALL,
#                 escapechar=None, index=False)
#     # Upload the file
#     try:
#         response = storageClient.put_object(ACL='public-read',
#                                              Body=csv_buffer.getvalue(),
#                                              Bucket=bucket,
#                                              Key=file_name)
#         return True
#     except ClientError as e:
#         print(e)
#         return False
