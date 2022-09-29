import os
import requests
import json
from loggingYour.messageHandler import messageHandler
from apiYour.settingsApi import PRODUCTION_ADDRESS, DEVELOPMENT_ADDRESS

def updateCategory(logger: object,
                   payload: dict,
                   category_id: int,
                   environment: str = "production") -> list:

    ## logging
    msg_handler = messageHandler(logger=logger, level="DEBUG",
                                 labels={'function': 'updateCategory', 'endpoint': '/Category/{category_id}'})
    msg_handler.logStruct(topic=f"updateCategory: categoryId: {category_id}, start updating category.", data=payload)

    ## construct request
    if environment == "production":
        request_url = f"{PRODUCTION_ADDRESS}/Category/{category_id}"
    elif environment == "development":
        request_url = f"{DEVELOPMENT_ADDRESS}/Category/{category_id}"

    ## request
    r = requests.put(request_url,
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

def updateBrand(logger: object,
                payload: dict,
                brand_id: int,
                environment: str = "production") -> list:

    ## logging
    msg_handler = messageHandler(logger=logger, level="DEBUG",
                                 labels={'function': 'updateBrand', 'endpoint': '/Brand/{brand_id}'})
    msg_handler.logStruct(topic=f"updateBrand: brandId: {brand_id}, start updating brand.", data=payload)

    ## construct request
    if environment == "production":
        request_url = f"{PRODUCTION_ADDRESS}/Brand/{brand_id}"
    elif environment == "development":
        request_url = f"{DEVELOPMENT_ADDRESS}/Brand/{brand_id}"

    ## request
    r = requests.put(request_url,
                      json=payload,
                      headers={'Authorization': 'Bearer ' + os.environ["YOUR_API_TOKEN"]})

    if r.status_code == 200:
        resp_data = json.loads(r.text).get('data')
        if resp_data:
            media = resp_data.get('duplicates', [])

            ## logging
            msg_handler.logStruct(topic=f"updateBrand: brandId: {brand_id}, update brand success",
                                  status_code=r.status_code,
                                  response_text=r.text)
            return media

    else:
        ## logging
        msg_handler.logStruct(level="ERROR",
                              topic=f"updateBrand:  brandId: {brand_id}, update brand error",
                              status_code=r.status_code,
                              response_text=r.text)
        return []

def updateAttribute(logger: object,
                    payload: dict,
                    attribute_id: int,
                    environment: str = "production") -> list:

    ## logging
    msg_handler = messageHandler(logger=logger, level="DEBUG",
                                 labels={'function': 'updateAttribute', 'endpoint': '/Attribute/{attributeId}'})
    msg_handler.logStruct(topic=f"updateAttribute: attributeId: {attribute_id}, start updating attribute.", data=payload)

    ## construct request
    if environment == "production":
        request_url = f"{PRODUCTION_ADDRESS}/Attribute/{attribute_id}"
    elif environment == "development":
        request_url = f"{DEVELOPMENT_ADDRESS}/Attribute/{attribute_id}"

    ## request
    r = requests.put(request_url,
                      json=payload,
                      headers={'Authorization': 'Bearer ' + os.environ["YOUR_API_TOKEN"]})

    if r.status_code == 200:
        resp_data = json.loads(r.text).get('data')
        if resp_data:
            media = resp_data.get('duplicates', [])

            ## logging
            msg_handler.logStruct(topic=f"updateAttribute: attributeId: {attribute_id}, update attribute success",
                                  status_code=r.status_code,
                                  response_text=r.text)
            return media

    else:
        ## logging
        msg_handler.logStruct(level="ERROR",
                              topic=f"updateAttribute:  attributeId: {attribute_id}, update attribute error",
                              status_code=r.status_code,
                              response_text=r.text)
        return []

def updateProduct(logger: object,
                  productId: int,
                  payload: dict,
                  environment: str = "production",
                  session: object = None,
                  additional_labels: dict = {}) -> list:

    ## logging
    labels = {'function': 'updateProduct', 'endpoint': '/Product/{productId}'}
    if additional_labels:
        labels.update(additional_labels)
    msg_handler = messageHandler(logger=logger, level="DEBUG",
                                 labels=labels)
    msg_handler.logStruct(topic=f"updateProduct: update product",
                          data=payload)

    ## construct request
    if environment == "production":
        request_url = f"{PRODUCTION_ADDRESS}/Product/{productId}"
    elif environment == "development":
        request_url = f"{DEVELOPMENT_ADDRESS}/Product/{productId}"

    ## handle request through session or normal
    if session:
        r = session.put(url=request_url,
                      json=payload,
                      headers={'Authorization': 'Bearer ' + os.environ["YOUR_API_TOKEN"]})
    else:
        r = requests.put(url=request_url,
                          json=payload,
                          headers={'Authorization': 'Bearer ' + os.environ["YOUR_API_TOKEN"]})

    if r.status_code == 200:
        resp_data = json.loads(r.text).get('data')
        if resp_data:
            media = resp_data.get('duplicates', [])

            ## logging
            msg_handler.logStruct(topic=f"updateProduct: productId: {productId}, update product success",
                                  status_code=r.status_code,
                                  response_text=r.text)
            return media

    else:
        ## logging
        msg_handler.logStruct(level="ERROR",
                              topic=f"updateProduct:  productId: {productId}, update product error",
                              status_code=r.status_code,
                              response_text=r.text)
        return []