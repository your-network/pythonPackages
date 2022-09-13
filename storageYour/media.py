from io import BytesIO
from storageYour.upload import uploadBytesMedia
import requests

def mediaUrlS3BucketUpload(storageService: object, media_url: str, internal_path: str, msg_handler: object):
    response = requests.get(media_url, timeout=15)

    ## logging
    msg_handler.logStruct(topic=f"mediaUrlS3BucketUpload: url: {media_url}, request made. Status code: {response.status_code}",
                          data=response.status_code,
                          level="DEBUG",
                          labels={"function": "mediaUrlS3BucketUpload"})

    if response.status_code == 200:
        bytes_content = BytesIO(response.content)
        bytes_content.seek(0)
        content_type = response.headers['Content-Type']

        ## upload details
        my_bucket = storageService.Bucket("yourcontent-dev")

        response = my_bucket.upload_fileobj(bytes_content, internal_path, ExtraArgs={'ContentType': content_type, 'ACL': "public-read"})

        print(response)

        return True

    else:
        ## logging
        msg_handler.logStruct(
            topic=f"mediaUrlS3BucketUpload: url: {media_url}, request made. Status code: {response.status_code}",
            data=response.text,
            level="WARNING",
            labels={"function": "mediaUrlS3BucketUpload"})

        return False
