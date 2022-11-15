import os
import requests
import json
from datetime import datetime
from typing import Tuple
from loggingYour.messageHandler import messageHandler
from apiYour.settingsApi import PRODUCTION_ADDRESS, DEVELOPMENT_ADDRESS

def removeCategoryMedia(logger:object,
                        media: str,
                        categoryId: int = None,
                        environment: str = "production",
                        connection: object = None) -> dict:

    start_time = datetime.now()
    msg_handler = messageHandler(logger=logger, level="DEBUG",
                                 labels={'function': 'removeCategoryMedia',
                                         'endpoint': '/Category/{categoryId}/Media/{media}'})
    ## construct request
    base_params = {}
    if environment == "production":
        request_url = f"{PRODUCTION_ADDRESS}/Category/{categoryId}/Media/{media}"
    elif environment == "development":
        request_url = f"{DEVELOPMENT_ADDRESS}/Category/{categoryId}/Media/{media}"

    ## logging
    msg_handler.logStruct(
        topic=f"removeCategoryMedia: delete media from category",
        data=base_params)

    ## request variables
    try:
        ## handle request through session or normal
        no_error = True
        if connection:
            ## process request from connection pool
            r = connection.request(method="DELETE",
                                   url=request_url,
                                   headers={'Authorization': 'Bearer ' + os.environ["YOUR_API_TOKEN"],
                                            'Content-Type': 'application/json'})

            response_code = r.status
            response_text = r.data
            r.close()
            if response_code == 200:
                return True
            else:
                return False

        else:
            ## process request with requests library. Single connection & request
            r = requests.delete(url=request_url,
                                headers={'Authorization': 'Bearer ' + os.environ["YOUR_API_TOKEN"]})

            response_code = r.status_code
            response_text = r.text
            if response_code == 200:
                return True
            else:
                return False

    except Exception as e:
        msg_handler.logStruct(topic="removeCategoryMedia: Error removing media",
                              error_message=str(e))

    return False