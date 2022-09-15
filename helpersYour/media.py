from PIL import Image
import traceback
Image.MAX_IMAGE_PIXELS = None
from helpersYour.settings import HEADER
from io import BytesIO
import hashlib
import requests
from loggingYour.messageHandler import messageHandler

def getIpfsImageDetails(logger: object, ipfs_url: str) -> dict:
    msg_handler = messageHandler(logger=logger, level="DEBUG", labels={'function': 'getIpfsImageDetails'})

    try:
        file_directory = ipfs_url.split("//")[-1]

        response = requests.request("GET", f"https://cloudflare-ipfs.com/ipfs/{file_directory}")

        ## logging
        msg_handler.logStruct(topic=f"getIpfsImageDetails: get ipfs image through cloudflare",
                              data=ipfs_url,
                       status_code=response.status_code)

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

    except:
        ## logging
        error = traceback.format_exc()
        msg_handler.logStruct(level="ERROR",
                              topic=f"getIpfsImageDetails: ipfs image reading error",
                              error_message=str(error))
        return {}

def createImageDetailsDic(details: dict,language: str) -> dict:
    image_dic = {"url": details['url'],
                 "internalPath": f"/{details['shA256']}.{details['extension']}",
                 "downloadNeeded": False,
                 "contentType": details['format'],
                 "imageType": details['imageType'],
                 "fileSize": details['fileSize'],
                 "height": details['heigth'],
                 "width": details['width'],
                 "shA256": details['shA256'],
                 "languages": [language],
                 "attributes": []
                }

    if details.get('ranking'):
        image_dic.update({"ranking": details['ranking']})

    return image_dic

def createMediaDetailsDic(logger: object, url: str,language: str) -> dict:
    details = getMediaFileUrl(logger, url)

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

        if details.get('ranking'):
            media_dic.update({"ranking": details['ranking']})

        return media_dic

    else:
        return {}

def getImageFromFile(logger: object,
                     file_path: str,
                     extension: str) -> dict:
    ## logging
    msg_handler = messageHandler(logger=logger, level="DEBUG", labels={'function': 'getImageFromFile'})
    msg_handler.logStruct(topic=f"getImageFromFile: get image from file",
                          data=file_path)

    try:
        with open(file_path, "rb") as f:
            bytes = f.read()  # read entire file as bytes
            sha256 = hashlib.sha256(bytes).hexdigest();
            im = Image.open(BytesIO(bytes))
            size = len(bytes)
            w, h = im.size
            # print(f"sha256: {sha256}, size: {len(bytes)}, w: {w}, h: {h}")

        return {'url': None,
                'width': w,
                'heigth': h,
                'format': extension,
                'shA256': sha256,
                'fileSize': size,
                'extension': extension}

    except:
        ## logging
        error = traceback.format_exc()
        msg_handler.logStruct(level="ERROR",
                              topic=f"getImageFromFile: image file reading error",
                              error_message=str(error))

        return {}

def imageDetailsUrl(logger: object,
                    image_url: str =None) -> dict:

    msg_handler = messageHandler(logger=logger, level="DEBUG", labels={'function': 'imageDetailsUrl'})

    try:
        response = requests.get(image_url, headers=HEADER)

        ## logging
        msg_handler.logStruct(topic=f"imageDetailsUrl: get image with request",
                              data=image_url,
                              status_code=response.status_code)

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

    except:
        ## logging
        error = traceback.format_exc()
        msg_handler.logStruct(level="ERROR",
                              topic=f"imageDetailsUrl: image reading error",
                              error_message=str(error))
        return {}

def getMediaFileUrl(logger: object, url: str=None) -> dict:
    msg_handler = messageHandler(logger=logger, level="DEBUG", labels={'function': 'getMediaFileUrl'})

    try:
        file_name = url.split("/")[-1]

        r = requests.get(url)

        ## logging
        msg_handler.logStruct(topic=f"getMediaFileUrl: get media with request",
                              data=url,
                              status_code=r.status_code)

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

    except:
        ## logging
        error = traceback.format_exc()
        msg_handler.logStruct(level="ERROR",
                              topic=f"getMediaFileUrl: media reading error",
                              error_message=str(error))

        return {}
