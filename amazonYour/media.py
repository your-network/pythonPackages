from PIL import Image
from io import BytesIO
from amazonYour.upload import uploadBytesMedia
import requests

def mediaUrlS3BucketUpload(amazonS3Client: object, media_url: str, internal_path: str, msg_handler: object):
    response = requests.get(media_url)

    ## logging
    msg_handler.logStruct(topic=f"mediaUrlS3BucketUpload: url: {media_url}, request made",
                          data=response,
                          level="DEBUG",
                          labels={"function": "mediaUrlS3BucketUpload"})

    if response.status_code == 200:
        bytes_content = BytesIO(response.content)
        content_type = response.headers['Content-Type']
        ## upload details
        return uploadBytesMedia(amazonS3Client,
                                "yourcontent-dev",
                                bytes_content,
                                internal_path,
                                content_type,
                                msg_handler)

    else:
        return False
