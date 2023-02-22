from PIL import Image
import traceback
import os
Image.MAX_IMAGE_PIXELS = None
from helpersYour.settings import HEADER
from io import BytesIO
import hashlib
import requests
from loggingYour.localLogging import LocalLogger
import mimetypes

def getIpfsImageDetails(logger: LocalLogger, ipfs_url: str) -> dict:
    ## logging
    if logger and bool(os.getenv('DEBUG', 'False')):
        log_message = {"topic": f"Start get",
                       "function": "getIpfsImageDetails",
                       "url": ipfs_url}
        logger.createDebugLog(message=log_message)

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

    except:
        ## logging
        if logger and bool(os.getenv('DEBUG', 'False')):
            error = traceback.format_exc()
            log_message = {"topic": f"Start get",
                           "function": "getIpfsImageDetails",
                           "url": ipfs_url,
                           "error": str(error)}
            logger.createErrorLog(message=log_message)

        return {}

def createImageDetailsDic(details: dict,language: str = "EN") -> dict:
    image_dic = {"url": details['url'],
                 "internalPath": f"/m/{details['shA256']}.{details['extension']}",
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

def createMediaDetailsDic(logger: LocalLogger,
                          url: str,
                          language: str,
                          connection: object = None) -> dict:

    details = getMediaFileUrl(logger=logger,
                              url=url,
                              connection=connection)

    if details:
        media_dic = {"url": details['url'],
                     'internalPath': f"/m/{details['shA256']}.{details['extension']}",
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

def getImageFromFile(logger: LocalLogger,
                     image_file_dic: dict) -> dict:
    ## logging
    if logger and bool(os.getenv('DEBUG', 'False')):
        log_message = {"topic": f"Start get",
                       "function": "getImageFromFile",
                       "data": image_file_dic["file_path"]}
        logger.createDebugLog(message=log_message)

    try:
        with open(image_file_dic["file_path"], "rb") as f:
            bytes = f.read()
            sha256 = hashlib.sha256(bytes).hexdigest();
            im = Image.open(BytesIO(bytes))
            size = len(bytes)
            w, h = im.size

        content_type = mimetypes.guess_type(image_file_dic["file_path"])
        if isinstance(content_type, tuple):
            content_type = content_type[0]

        return {'url': "https://your.io",
                'width': w,
                'heigth': h,
                'format': content_type,
                'shA256': sha256,
                'fileSize': size,
                'extension': image_file_dic["extension"]}

    except:
        ## logging
        if logger and bool(os.getenv('DEBUG', 'False')):
            error = traceback.format_exc()
            log_message = {"topic": f"Start get",
                           "function": "getImageFromFile",
                           "data": image_file_dic["file_path"],
                           "error": str(error)}
            logger.createErrorLog(message=log_message)

        return {}

def imageDetailsUrl(logger: LocalLogger,
                    additional_labels: dict = {},
                    image_url: str =None,
                    connection: object = None) -> dict:

    ## logging
    if logger and bool(os.getenv('DEBUG', 'False')):
        log_message = {"topic": f"Start get",
                       "function": "imageDetailsUrl",
                       "imageUrl": image_url}
        logger.createDebugLog(message=log_message, **additional_labels)

    try:
        if connection:
            ## process request from connection pool
            r = connection.request(method="GET",
                                   url=image_url,
                                   headers=HEADER)
            response_code = r.status
            header = r.headers
            content = r.data

        else:
            ## process request with requests library. Single connection & request
            response = requests.get(image_url, headers=HEADER)
            response_code = response.status_code
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
            sha256 = hashlib.sha256(content).hexdigest()
            extension = im.get_format_mimetype().split('/')[-1]
            file_format = im.get_format_mimetype()
            im.close()

        if connection == None:
            # closing the connection
            response.close()

        return {'url': image_url,
                'width': w,
                'heigth': h,
                'format': file_format,
                'shA256': sha256,
                'fileSize': len(content),
                'extension': extension}

    except:
        ## logging
        if logger and bool(os.getenv('DEBUG', 'False')):
            error = traceback.format_exc()
            log_message = {"topic": f"Error imageDetailsUrl",
                           "function": "imageDetailsUrl",
                           "imageUrl": image_url,
                           "error": str(error)}
            logger.createErrorLog(message=log_message, **additional_labels)

        return {}

def getMediaFileUrl(logger: LocalLogger,
                    url: str,
                    connection: object = None) -> dict:

    ## logging
    if logger and bool(os.getenv('DEBUG', 'False')):
        log_message = {"topic": f"Start get",
                       "function": "getMediaFileUrl",
                       "url": url}
        logger.createDebugLog(message=log_message)

    try:
        file_name = url.split("/")[-1]

        if connection:
            ## process request from connection pool
            r = connection.request(method="GET",
                                   url=url)
            response_code = r.status
            header = r.headers
            content = r.data

        else:
            ## process request with requests library. Single connection & request
            response = requests.get(url=url)
            response_code = response.status_code
            content = response.content
            header = response.headers

        content_type = header.get('content-type')
        sha256 = hashlib.sha256(content).hexdigest()

        if connection == None:
            # closing the connection
            response.close()

        return {'url': url,
                'contentType': content_type,
                'fileName': file_name,
                'shA256': sha256,
                'fileSize': len(content),
                'extension': content_type.lower().split('/')[-1]}

    except:
        ## logging
        if logger and bool(os.getenv('DEBUG', 'False')):
            error = traceback.format_exc()
            log_message = {"topic": f"media reading error",
                           "function": "getMediaFileUrl",
                           "url": url,
                           "error": str(error)}
            logger.createErrorLog(message=log_message)

        return {}
