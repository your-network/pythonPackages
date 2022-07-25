from PIL import Image
Image.MAX_IMAGE_PIXELS = None
from helpersYour.settings import HEADER
from io import BytesIO
import hashlib
import requests
from loggingYour.logging import logging_error_message

def getIpfsImageDetails(ipfs_url):
    try:
        file_directory = ipfs_url.split("//")[-1]

        response = requests.request("GET", f"https://cloudflare-ipfs.com/ipfs/{file_directory}")

        im = Image.open(BytesIO(response.content))
        w, h = im.size

        shA256 = hashlib.sha256(response.content).hexdigest()

        return {'url': ipfs_url,
                'width': w,
                'heigth': h,
                'format': im.get_format_mimetype(),
                'shA256': shA256,
                'fileSize': len(response.content),
                'extension': im.get_format_mimetype().split('/')[-1]}

    except Exception as e:
        logging_error_message("get", "Ipfs Image reading", ipfs_url, e, response.status_code)
        return None

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
    if details:
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
    else:
        return None

def imageDetailsUrl(image_url: str =None) -> dict:
    try:
        response = requests.get(image_url, headers=HEADER)
        content = response.content

        header = response.headers
        content_type = header.get('content-type')

        if 'svg' in content_type:
            w, h = 0, 0
            sha256 = hashlib.sha256(content).hexdigest()
            extension = 'svg'
            file_format = content_type

        else:
            im = Image.open(BytesIO(content))
            w, h = im.size
            sha256 = hashlib.sha256(response.content).hexdigest()
            extension = im.get_format_mimetype().split('/')[-1]
            file_format = im.get_format_mimetype()

        return {'url': image_url,
                'width': w,
                'heigth': h,
                'format': file_format,
                'shA256': sha256,
                'fileSize': len(content),
                'extension': extension}

    except Exception as e:
        logging_error_message("get", "Image reading", image_url, e, response.status_code)
        return {}

def getMediaFileUrl(url=None):
    try:
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
                'fileSize': len(content),
                'extension': content_type.lower().split('/')[-1]}

    except Exception as e:
        logging_error_message("get", "Media file reading", url, e, r.status_code)
        return None
