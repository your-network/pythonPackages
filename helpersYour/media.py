from PIL import Image
from io import BytesIO
import hashlib
import requests
import numpy as np
import uuid
import os
## your functions
from amazonYour.authenticate import amazon
from .writers import generateUUID

def getIpfsImageDetails(ipfs_url):
    file_directory = ipfs_url.split("//")[-1]

    response = requests.request("GET", f"https://cloudflare-ipfs.com/ipfs/{file_directory}")

    im = Image.open(BytesIO(response.content))
    w, h = im.size

    shA256 = sha256Image(im)

    return {'url': ipfs_url,
            'width': w,
            'heigth': h,
            'format': im.format,
            'shA256': shA256,
            'fileSize': len(response.content)}

def createImageDetailsDic(details,language):
    image_dic = {"url": details['url'],
                 "internalPath": f"/{details['shA256']}.{details['format'].lower()}",
                 "downloadNeeded": False,
                 "contentType": details['format'],
                 "fileSize": details['fileSize'],
                 "height": details['heigth'],
                 "width": details['width'],
                 "shA256": details['shA256'],
                 "languages": [language],
                 "attributes": {
                    }
                }
    return image_dic

def createMediaDetailsDic(url,language):
    details = getMediaFileUrl(url)
    media_dic = {"url": details['url'],
                 'internalPath': f"/{details['shA256']}.{details['fileName'].split('.')[-1]}",
                 "downloadNeeded": False,
                 "contentType": details['contentType'],
                 "fileSize": details['fileSize'],
                 "shA256": details['shA256'],
                 "languages": [language],
                 "attributes": {
                    }
                }
    return media_dic

def imageDetailsUrl(image_url=None,keep=0):
    response = requests.get(image_url)
    content = response.content

    im = Image.open(BytesIO(content))
    w, h = im.size
    sha256 = sha256Image(im)

    return {'url': image_url,
            'width': w,
            'heigth': h,
            'format':im.format,
            'shA256': sha256,
            'fileSize': len(content)}

def getMediaFileUrl(url=None):
    file_name = url.split("/")[-1]

    r = requests.get(url)
    content = r.content
    header = r.headers

    content_type = header.get('content-type')
    sha256 = hashlib.sha256(content).hexdigest()

    return {'url': url,
            'contentType': content_type,
            'fileName': file_name,
            'shA256': sha256,
            'fileSize': len(content)}

def sha256Image(im):
    Na = np.array(im).astype(np.uint16)
    sha256 = hashlib.sha256(Na.tobytes()).hexdigest()
    return sha256
