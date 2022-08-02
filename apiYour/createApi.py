import os
import requests
import json
from datetime import datetime
from typing import Tuple
from loggingYour.messageHandler import messageHandler

def createCategory(payload: dict, logger: object) -> Tuple[int, dict]:
    msg_handler = messageHandler(logger=logger, level="DEBUG", labels={'function': 'createCategory', 'endpoint': '/Category/'})
    start_time = datetime.now()
    resp_data = None

    msg_handler.logStruct(topic=f"createCategory: start create category. start time: {start_time}", data=payload)

    r = requests.post('https://api.yourcontent.io/Category/',
                      json=payload,
                      headers={'Authorization': 'Bearer ' + os.environ["YOUR_API_TOKEN"]})

    if r.status_code == 200:
        resp_data = json.loads(r.text).get('data')

        if resp_data:
            cat_id = resp_data.get('id')
            media = resp_data.get('duplicates')

            ## logging
            msg_handler.logStruct(
                           topic=f"createCategory: category created finished, cat_id: {cat_id}, duplicate_media: {media}",
                           status_code=r.status_code,
                           response_text=r.text
                           )

            return cat_id, media

        else:
            ## logging
            msg_handler.logStruct(topic=f"createCategory: no response data",
                                  status_code=r.status_code,
                                  response_text=r.text)

    else:
        ## logging
        msg_handler.logStruct(level="ERROR",
                       topic="getAllCategories: Error in the get all function",
                       status_code=r.status_code,
                       response_text=r.text)

    return None, None

def createProductBulk(logger: object, data_bulk: list):
    msg_handler = messageHandler(logger=logger, level="DEBUG", labels={'function': 'createProductBulk', 'endpoint': '/Product/CreateOrUpdateBulk'})
    start_time = datetime.now()

    ## logging
    msg_handler.logStruct(f"createProductBulk: start process product bulk insert, number products: {len(data_bulk)}. Start time: {start_time}",
                   data=data_bulk)

    ## request
    r = requests.post(f"https://api.yourcontent.io/Product/CreateOrUpdateBulk",
                     json=data_bulk,
                     headers={'Authorization': 'Bearer ' + os.environ["YOUR_API_TOKEN"]})

    if r.status_code == 200:
        resp_data = json.loads(r.text)
        product_bulk_response = resp_data

        ## logging
        msg_handler.logStruct(topic=f"createProductBulk: Success in product bulk insert. Number products: {len(data_bulk)}",
                       status_code=r.status_code,
                       response_text=r.text)

    else:
        ## logging
        msg_handler.logStruct(level="ERROR",
                       topic="createProductBulk: Error in product bulk insert",
                       status_code=r.status_code,
                       response_text=r.text)

        product_bulk_response = None

        ## logging
        msg_handler.logStruct(topic=f"createProductBulk: Api product bulk insert finished, processing time: {datetime.now() - start_time}",
                   status_code=r.status_code,
                   response_text=r.text)

    return product_bulk_response

def createProductQueue(logger: object, data_bulk: list):
    product_bulk_response = None
    msg_handler = messageHandler(logger=logger, level="DEBUG", labels={'function': 'createProductQueue', 'endpoint': '/Product/QueueForCreateBulk'})
    start_time = datetime.now()

    ## logging
    msg_handler.logStruct(topic=f"createProductQueue: process product queue. Start time: {start_time}", data=data_bulk)

    ## request
    r = requests.post(f"https://api.yourcontent.io/Product/QueueForCreateBulk",
                     json=data_bulk,
                     headers={'Authorization': 'Bearer ' + os.environ["YOUR_API_TOKEN"]})

    if r.status_code == 200:
        resp_data = json.loads(r.text)
        product_bulk_response = resp_data

        ## logging
        msg_handler.logStruct(topic=f"createProductQueue: Success in product queue insert. Number products: {len(data_bulk)}",
                       status_code=r.status_code,
                       response_text=r.text)
    else:
        ## logging
        msg_handler.logStruct(topic="createProductQueue: Error product bulk insert",
                              level="DEBUG",
                       status_code=r.status_code,
                       response_text=r.text)

    ## logging
    msg_handler.logStruct(topic=f"createProductBulk: Api product queue insert finished, processing time: {datetime.now() - start_time}")

    return product_bulk_response

def createAttributeUnit(logger: object, data: dict) -> int:
    unit_id = None
    start_time = datetime.now()
    msg_handler = messageHandler(logger=logger, level="DEBUG",
                                 labels={'function': 'createAttributeUnit', 'endpoint': '/Attribute/CreateOrUpdateAttributeTypeUnit'})

    ## logging
    msg_handler.logStruct(topic=f"createAttributeUnit: start create attribute unit. Start time: {start_time}", data=data)

    ## request
    r = requests.post(f"https://api.yourcontent.io/Attribute/CreateOrUpdateAttributeTypeUnit",
                     json=data,
                     headers={'Authorization': 'Bearer ' + os.environ["YOUR_API_TOKEN"]})

    if r.status_code == 200:
        resp_data = json.loads(r.text)
        unit_id = resp_data['data']['id']

        ## logging
        msg_handler.logStruct(topic=f"createAttributeUnit: create attribute unit success. Unit_id: {unit_id}",
                       status_code=r.status_code,
                       response_text=r.text)

    else:
        ## logging
        msg_handler.logStruct(topic="createAttributeUnit: Error attribute unit insert",
                              level="ERROR",
                       status_code=r.status_code,
                       response_text=r.text)

    ## logging
    msg_handler.logStruct(topic=f"createAttributeUnit: Api attribute unit insert finished, processing time: {datetime.now() - start_time}")

    return unit_id

def createAttributeType(logger: object, data: dict) -> int:
    attribute_type_id = None
    start_time = datetime.now()
    msg_handler = messageHandler(logger=logger, level="DEBUG",
                                 labels={'function': 'CreateOrUpdateAttributeType',
                                         'endpoint': '/Attribute/CreateOrUpdateAttributeType'})
    ## logging
    msg_handler.logStruct(topic=f"createAttributeType: start create attribute type.\n start time: {start_time}", data=data)

    ## request
    r = requests.post(f"https://api.yourcontent.io/Attribute/CreateOrUpdateAttributeType",
                     json=data,
                     headers={'Authorization': 'Bearer ' + os.environ["YOUR_API_TOKEN"]})

    if r.status_code == 200:
        resp_data = json.loads(r.text)
        attribute_type_id = resp_data['data']['id']

        ## logging
        msg_handler.logStruct(topic=f"createAttributeType: finished create attribute type. attribute id type: {attribute_type_id}",
                              status_code=r.status_code,
                              response_text=r.text)

    else:
        ## logging
        msg_handler.logStruct(
            level="ERROR",
            topic=f"createAttributeType: error create attribute type",
            status_code=r.status_code,
            response_text=r.text)

    ## logging
    msg_handler.logStruct(topic=f"createAttributeUnit: Api attribute unit create finished,\n processing time: {datetime.now() - start_time}")

    return attribute_type_id

def createAttribute(logger: object, data: dict) -> int:
    attribute_id = None
    start_time = datetime.now()
    msg_handler = messageHandler(logger=logger, level="DEBUG",
                                 labels={'function': 'createAttribute',
                                         'endpoint': '/Attribute/CreateOrUpdate'})

    ## logging
    msg_handler.logStruct(topic=f"createAttribute: start create attribute.\n start time: {start_time}",
                          data=data)

    ## request
    r = requests.post(f"https://api.yourcontent.io/Attribute/CreateOrUpdate",
                     json=data,
                      headers={'Authorization': 'Bearer ' + os.environ["YOUR_API_TOKEN"]})

    if r.status_code == 200:
        # print(f"Attribute create Success")
        resp_data = json.loads(r.text)
        attribute_id = resp_data['data']['id']

        ## logging
        msg_handler.logStruct(
            topic=f"createAttributeType: finished create attribute type. attribute id: {attribute_id}",
            status_code=r.status_code,
            response_text=r.text)

    else:
        ## logging
        msg_handler.logStruct(
            level="ERROR",
            topic=f"createAttribute: error create attribute",
            status_code=r.status_code,
            response_text=r.text)

    ## logging
    msg_handler.logStruct(topic=f"createAttribute: Api attribute create finished,\n processing time: {datetime.now() - start_time}")

    return attribute_id

def createBrand(logger: object, data: dict) -> int:
    brand_id = None
    start_time = datetime.now()
    msg_handler = messageHandler(logger=logger, level="DEBUG",
                                 labels={'function': 'createBrand',
                                         'endpoint': '/Brand'})

    ## logging
    msg_handler.logStruct(topic=f"createBrand: start create attribute.\n start time: {start_time}",
                          data=data)

    ## request
    r = requests.post(f"https://api.yourcontent.io/Brand",
                     json=data,
                      headers={'Authorization': 'Bearer ' + os.environ["YOUR_API_TOKEN"]})

    if r.status_code == 200:
        resp_data = json.loads(r.text)
        brand_id = resp_data['data']['id']

        ## logging
        msg_handler.logStruct(
            topic=f"createBrand: finished create brand. brand id: {brand_id}",
            status_code=r.status_code,
            response_text=r.text)

    else:
        ## logging
        msg_handler.logStruct(
            level="ERROR",
            topic=f"createBrand: error create brand",
            status_code=r.status_code,
            response_text=r.text)

    ## logging
    msg_handler.logStruct(topic=f"createBrand: Api brand create finished,\n processing time: {datetime.now() - start_time}")

    return brand_id

def createSeries(logger: object, data=dict) -> int:
    serie_id = None
    start_time = datetime.now()
    msg_handler = messageHandler(logger=logger, level="DEBUG",
                                 labels={'function': 'createSeries',
                                         'endpoint': '/Series'})

    ## logging
    msg_handler.logStruct(topic=f"createSeries: start create serie.\n start time: {start_time}",
                          data=data)

    ## request
    r = requests.post(f"https://api.yourcontent.io/Series",
                     json=data,
                      headers={'Authorization': 'Bearer ' + os.environ["YOUR_API_TOKEN"]})

    if r.status_code == 200:
        resp_data = json.loads(r.text)
        serie_id = resp_data['data']['id']

        ## logging
        msg_handler.logStruct(
            topic=f"createSeries: finished create serie. serie id: {serie_id}",
            status_code=r.status_code,
            response_text=r.text)

    else:
        ## logging
        msg_handler.logStruct(
            level="ERROR",
            topic=f"createSeries: error create serie",
            status_code=r.status_code,
            response_text=r.text)

    ## logging
    msg_handler.logStruct(topic=f"createSeries: Api create serie finished,\n processing time: {datetime.now() - start_time}")

    return serie_id

def createCategoryCategoryRelation(logger: object, data: dict) -> bool:
    msg_handler = messageHandler(logger=logger, level="DEBUG",
                                 labels={'function': 'createCategoryCategoryRelation',
                                         'endpoint': '/Relation/CreateCategoryCategory'})

    ## logging
    msg_handler.logStruct(topic=f"createCategoryCategoryRelation: Start create category category relation,\n start time: {datetime.now()}")

    ## request
    r = requests.post(f"https://api.yourcontent.io/Relation/CreateCategoryCategory",
                     json=data,
                    headers={'Authorization': 'Bearer ' + os.environ["YOUR_API_TOKEN"]})

    if r.status_code == 200:
        ## logging
        msg_handler.logStruct(
            topic=f"createCategoryCategoryRelation: finished create relation category category",
            status_code=r.status_code,
            response_text=r.text)

        return True

    else:
        ## logging
        msg_handler.logStruct(
            level="ERROR",
            topic=f"createCategoryCategoryRelation: error create relation category category",
            status_code=r.status_code,
            response_text=r.text)

        return False

def createBrandCategoryRelation(logger: object, data: dict) -> bool:
    msg_handler = messageHandler(logger=logger, level="DEBUG",
                                 labels={'function': 'createBrandCategoryRelation',
                                         'endpoint': '/Relation/CreateBrandCategory'})

    ## logging
    msg_handler.logStruct(topic=f"createBrandCategoryRelation: Start create brand category relation,\n start time: {datetime.now()}")

    ## request
    r = requests.post(f"https://api.yourcontent.io/Relation/CreateBrandCategory",
                     json=data,
                    headers={'Authorization': 'Bearer ' + os.environ["YOUR_API_TOKEN"]})

    if r.status_code == 200:
        ## logging
        msg_handler.logStruct(
            topic=f"createBrandCategoryRelation: finished create relation brand category",
            status_code=r.status_code,
            response_text=r.text)
        return True

    else:
        ## logging
        msg_handler.logStruct(
            level="ERROR",
            topic=f"createBrandCategoryRelation: error create relation brand category",
            status_code=r.status_code,
            response_text=r.text)
        return False

def createCategoryAttributeRelation(logger: object, data: dict) -> bool:
    msg_handler = messageHandler(logger=logger, level="DEBUG",
                                 labels={'function': 'createCategoryAttributeRelation',
                                         'endpoint': '/Relation/CreateAttributeCategory'})

    ## logging
    msg_handler.logStruct(
        topic=f"createCategoryAttributeRelation: Start create category attribute relation,\n start time: {datetime.now()}")

    ## request
    r = requests.post(f"https://api.yourcontent.io/Relation/CreateAttributeCategory",
                     json=data,
                    headers={'Authorization': 'Bearer ' + os.environ["YOUR_API_TOKEN"]})

    if r.status_code == 200:
        ## logging
        msg_handler.logStruct(
            topic=f"createCategoryAttributeRelation: finished create relation category attribute",
            status_code=r.status_code,
            response_text=r.text)
        return True

    else:
        ## logging
        msg_handler.logStruct(
            level="ERROR",
            topic=f"createCategoryAttributeRelation: error create relation category attribute",
            status_code=r.status_code,
            response_text=r.text)
        return False

def createProductProductRelation(logger: object, data: dict) -> bool:
    msg_handler = messageHandler(logger=logger, level="DEBUG",
                                 labels={'function': 'createProductProductRelation',
                                         'endpoint': '/Relation/CreateProductProduct'})

    ## logging
    msg_handler.logStruct(topic=f"createProductProductRelation: Start create product product relation,\n start time: {datetime.now()}")

    ## request
    r = requests.post(f"https://api.yourcontent.io/Relation/CreateProductProduct",
                     json=data,
                    headers={'Authorization': 'Bearer ' + os.environ["YOUR_API_TOKEN"]})

    if r.status_code == 200:
        ## logging
        msg_handler.logStruct(
            topic=f"createProductProductRelation: finished create relation product product",
            status_code=r.status_code,
            response_text=r.text)
        return True

    else:
        ## logging
        msg_handler.logStruct(
            level="ERROR",
            topic=f"createProductProductRelation: error create relation product product",
            status_code=r.status_code,
            response_text=r.text)
        return False
