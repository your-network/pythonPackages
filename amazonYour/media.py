from PIL import Image
from io import BytesIO
from amazonYour.upload import uploadBytesMedia, uploadMediaFile
import requests

def imageUrlS3BucketUpload(amazonS3Client, media_url, internal_path):
    ## get image
    response = requests.get(media_url)
    image = Image.open(BytesIO(response.content))
    ## upload details
    return uploadBytesMedia(amazonS3Client,
                     "yourcontent-dev",
                     image,
                     internal_path)

def mediaUrlS3BucketUpload(amazonS3Client, media_url, internal_path):
    response = requests.get(media_url)
    ## upload details
    return uploadMediaFile(amazonS3Client,
                    "yourcontent-dev",
                    response,
                    internal_path)
