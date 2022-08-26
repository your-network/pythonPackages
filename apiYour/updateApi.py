import os
import requests
import json
from datetime import datetime
from loggingYour.messageHandler import messageHandler

def updateCategory(logger: object, payload: dict, category_id: int) -> list:
    start_time = datetime.now()
    msg_handler = messageHandler(logger=logger, level="DEBUG",
                                 labels={'function': 'updateCategory', 'endpoint': '/Category/{category_id}'})

    ## logging
    msg_handler.logStruct(topic=f"updateCategory: categoryId: {category_id}, start updating product.", data=payload)

    ## request
    r = requests.put(f"https://api.yourcontent.io/Category/{category_id}",
                      json=payload,
                      headers={'Authorization': 'Bearer ' + os.environ["YOUR_API_TOKEN"]})

    if r.status_code == 200:
        resp_data = json.loads(r.text).get('data')
        if resp_data:
            media = resp_data.get('duplicates', [])

            ## logging
            msg_handler.logStruct(topic=f"updateCategory: categoryId: {category_id}, update category success",
                                  status_code=r.status_code,
                                  response_text=r.text)
            return media

    else:
        ## logging
        msg_handler.logStruct(level="ERROR",
                              topic=f"updateCategory:  categoryId: {category_id}, update category error",
                              status_code=r.status_code,
                              response_text=r.text)
        return []
