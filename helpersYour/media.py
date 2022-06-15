from PIL import Image
Image.MAX_IMAGE_PIXELS = None
from helpersYour.settings import HEADER
from io import BytesIO
import hashlib
import requests
import numpy as np

import logging
from helpersYour.logging import logging_error_message
logging.basicConfig(filename="mediaReadingLogs.log", level=logging.INFO)

def getIpfsImageDetails(ipfs_url):
    try:
        file_directory = ipfs_url.split("//")[-1]

        response = requests.request("GET", f"https://cloudflare-ipfs.com/ipfs/{file_directory}", headers=HEADER)

        im = Image.open(BytesIO(response.content))
        w, h = im.size

        shA256 = sha256Image(im)

        return {'url': ipfs_url,
                'width': w,
                'heigth': h,
                'format': im.get_format_mimetype(),
                'shA256': shA256,
                'fileSize': len(response.content),
                'extension': im.get_format_mimetype().split('/')[-1]}

    except Exception as e:
        logging_error_message("Ipfs Image reading", ipfs_url, e)

def createImageDetailsDic(details,language):
    image_dic = {"url": details['url'],
                 "internalPath": f"/{details['shA256']}.{details['extension']}",
                 "downloadNeeded": False,
                 "contentType": details['format'],
                 "fileSize": details['fileSize'],
                 "height": details['heigth'],
                 "width": details['width'],
                 "shA256": details['shA256'],
                 "languages": [language],
                 "attributes": []
                }
    return image_dic

def createMediaDetailsDic(url,language):
    details = getMediaFileUrl(url)
    media_dic = {"url": details['url'],
                 'internalPath': f"/{details['shA256']}.{details['extension']}",
                 "downloadNeeded": False,
                 "contentType": details['contentType'],
                 "fileSize": details['fileSize'],
                 "shA256": details['shA256'],
                 "languages": [language],
                 "attributes": []
                }
    return media_dic

def imageDetailsUrl(image_url=None):
    try:
        response = requests.get(image_url, headers=HEADER)
        content = response.content

        header = response.headers
        content_type = header.get('content-type')

        if 'svg' in content_type:
            w, h = 0, 0
            sha256 = hashlib.sha256(content).hexdigest()
            extension = 'svg'
            format = content_type

        else:
            im = Image.open(BytesIO(content))
            w, h = im.size
            sha256 = sha256Image(im)
            extension = im.get_format_mimetype().split('/')[-1]
            format = im.get_format_mimetype()

        return {'url': image_url,
                'width': w,
                'heigth': h,
                'format': format,
                'shA256': sha256,
                'fileSize': len(content),
                'extension': extension}

    except Exception as e:
        logging_error_message("Image reading", image_url, e)

def getMediaFileUrl(url=None):
    try:
        file_name = url.split("/")[-1]

        r = requests.get(url, headers=HEADER)
        content = r.content
        header = r.headers

        content_type = header.get('content-type')
        sha256 = hashlib.sha256(content).hexdigest()

        return {'url': url,
                'contentType': content_type,
                'fileName': file_name,
                'shA256': sha256,
                'fileSize': len(content),
                'extension': content_type.lower().split('/')[-1]}
    except Exception as e:
        logging_error_message("Media file reading", url, e)

def sha256Image(im):
    Na = np.array(im).astype(np.uint16)
    sha256 = hashlib.sha256(Na.tobytes()).hexdigest()
    return sha256
