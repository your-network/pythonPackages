from PIL import Image
from io import BytesIO
from amazonYour.upload import uploadBytesMedia
import requests

def mediaUrlS3BucketUpload(amazonS3Client, media_url, internal_path):
    response = requests.get(media_url)
    if response.status_code == 200:
        bytes_content = BytesIO(response.content)
        content_type = response.headers['Content-Type']
        ## upload details
        return uploadBytesMedia(amazonS3Client,
                        "yourcontent-dev",
                        bytes_content,
                        internal_path,
                        content_type)

    else:
        return False
