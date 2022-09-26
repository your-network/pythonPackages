import os
import requests
import json
from datetime import datetime
from typing import Tuple
from loggingYour.messageHandler import messageHandler
from apiYour.settingsApi import PRODUCTION_ADDRESS, DEVELOPMENT_ADDRESS

def createBrand(logger: object,
                data: dict,
                environment: str = "production") -> int:

    brand_id = None
    duplicate_media = []
    start_time = datetime.now()
    msg_handler = messageHandler(logger=logger, level="DEBUG",
                                 labels={'function': 'createBrand',
                                         'endpoint': '/Brand'})

    ## logging
    msg_handler.logStruct(topic=f"createBrand: start create brand.\n start time: {start_time}",
                          data=data,
                          level="DEBUG")

    ## construct request
    if environment == "production":
        request_url = f"{PRODUCTION_ADDRESS}/Brand"
    elif environment == "development":
        request_url = f"{DEVELOPMENT_ADDRESS}/Brand"

    ## request
    r = requests.post(request_url,
                     json=data,
                      headers={'Authorization': 'Bearer ' + os.environ["YOUR_API_TOKEN"]})

    if r.status_code in [200, 400]:
        resp_body = json.loads(r.text)
        resp_data = resp_body.get('data')
        success = resp_body.get('success')
        code = resp_body.get('code')

        if success:
            brand_id = resp_data['id']
            duplicate_media = resp_data.get('duplicates',[])

            ## logging
            msg_handler.logStruct(topic=f"createBrand: finished create brand. brand id: {brand_id}",
                                  status_code=r.status_code,
                                  response_text=r.text,
                                  level="DEBUG")

        elif code == 11:
            brand_id = resp_data.get('id')
            duplicate_media = resp_data.get('duplicates', [])

            ## logging
            msg_handler.logStruct(topic=f"createBrand: brand already existed, cat_id: {brand_id}, duplicate_media: {duplicate_media}",
                                  status_code=r.status_code,
                                  response_text=r.text,
                                  level="DEBUG")

        else:
            ## logging
            msg_handler.logStruct(topic=f"createBrand: no response data",
                                  status_code=r.status_code,
                                  response_text=r.text,
                                  level="WARNING")

    else:
        ## logging
        msg_handler.logStruct(
            level="ERROR",
            topic=f"createBrand: error create brand",
            status_code=r.status_code,
            response_text=r.text)

    ## logging
    msg_handler.logStruct(topic=f"createBrand: Api brand create finished,\n processing time: {datetime.now() - start_time}")

    # closing the connection
    r.close()

    return brand_id, duplicate_media

def createCategory(payload: dict,
                   logger: object,
                   environment: str = "production") -> Tuple[int, dict]:

    cat_id = None
    media = []
    msg_handler = messageHandler(logger=logger, level="DEBUG", labels={'function': 'createCategory', 'endpoint': '/Category/'})
    start_time = datetime.now()

    ## logging
    msg_handler.logStruct(topic=f"createCategory: start create category. start time: {start_time}", data=payload, level="DEBUG")

    ## construct request
    if environment == "production":
        request_url = f"{PRODUCTION_ADDRESS}/Category"
    elif environment == "development":
        request_url = f"{DEVELOPMENT_ADDRESS}/Category"

    r = requests.post(request_url,
                      json=payload,
                      headers={'Authorization': 'Bearer ' + os.environ["YOUR_API_TOKEN"]})

    if r.status_code in [200, 400]:
        resp_body = json.loads(r.text)
        resp_data = resp_body.get('data')
        success = resp_body.get('success')
        code = resp_body.get('code')

        if success:
            cat_id = resp_data.get('id')
            media = resp_data.get('duplicates',[])

            ## logging
            msg_handler.logStruct(topic=f"createCategory: category created finished, cat_id: {cat_id}, duplicate_media: {media}",
                                  status_code=r.status_code,
                                  response_text=r.text,
                                  level="DEBUG")

        elif code == 11:
            cat_id = resp_data.get('id')
            media = resp_data.get('duplicates', [])
            ## logging
            msg_handler.logStruct(topic=f"createCategory: category already existed, cat_id: {cat_id}, duplicate_media: {media}",
                                  status_code=r.status_code,
                                  response_text=r.text,
                                  level="DEBUG")

        else:
            ## logging
            msg_handler.logStruct(topic=f"createCategory: no response data",
                                  status_code=r.status_code,
                                  response_text=r.text,
                                  level="WARNING")

    else:
        ## logging
        msg_handler.logStruct(level="ERROR",
                       topic="getAllCategories: Error in the get all function",
                       status_code=r.status_code,
                       response_text=r.text)

    # closing the connection
    r.close()

    return cat_id, media

def createProductBulk(logger: object,
                      data_bulk: list,
                      environment: str = "production"):

    ## logging
    start_time = datetime.now()
    msg_handler = messageHandler(logger=logger, level="DEBUG",
                                 labels={'function': 'createProductBulk', 'endpoint': '/Product/CreateOrUpdateBulk'})
    msg_handler.logStruct(f"createProductBulk: start process product bulk insert, number products: {len(data_bulk)}. Start time: {start_time}",
                   data=data_bulk)

    ## construct request
    if environment == "production":
        request_url = f"{PRODUCTION_ADDRESS}/Product/CreateOrUpdateBulk"
    elif environment == "development":
        request_url = f"{DEVELOPMENT_ADDRESS}/Product/CreateOrUpdateBulk"

    ## request
    r = requests.post(request_url,
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

    # closing the connection
    r.close()

    return product_bulk_response

def createProductQueue(logger: object,
                       data_bulk: list,
                       environment: str = "production",
                       additional_labels: dict = {}):

    ## logging
    start_time = datetime.now()
    labels = {'function': 'createProductQueue', 'endpoint': '/Product/QueueForCreateBulk'}
    if additional_labels:
        labels.update(additional_labels)

    msg_handler = messageHandler(logger=logger, level="DEBUG",
                                 labels=labels)
    msg_handler.logStruct(topic=f"createProductQueue: process product queue. Start time: {start_time}", data=data_bulk)

    ## construct request
    if environment == "production":
        request_url = f"{PRODUCTION_ADDRESS}/Product/QueueForCreateBulk"
    elif environment == "development":
        request_url = f"{DEVELOPMENT_ADDRESS}/Product/QueueForCreateBulk"

    product_bulk_response = None

    ## request
    r = requests.post(request_url,
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
                              level="WARNING",
                              data=data_bulk,
                       status_code=r.status_code,
                       response_text=r.text)

    ## logging
    msg_handler.logStruct(topic=f"createProductBulk: Api product queue insert finished, processing time: {datetime.now() - start_time}")

    # closing the connection
    r.close()

    return product_bulk_response

def createAttributeUnit(logger: object,
                        data: dict,
                        environment: str = "production") -> int:

    ## logging
    start_time = datetime.now()
    msg_handler = messageHandler(logger=logger, level="DEBUG",
                                 labels={'function': 'createAttributeUnit',
                                         'endpoint': '/Attribute/CreateOrUpdateAttributeTypeUnit'})
    msg_handler.logStruct(topic=f"createAttributeUnit: start create attribute unit. Start time: {start_time}", data=data)

    ## construct request
    if environment == "production":
        request_url = f"{PRODUCTION_ADDRESS}/Attribute/CreateOrUpdateAttributeTypeUnit"
    elif environment == "development":
        request_url = f"{DEVELOPMENT_ADDRESS}/Attribute/CreateOrUpdateAttributeTypeUnit"

    unit_id = None

    ## request
    r = requests.post(request_url,
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

    # closing the connection
    r.close()

    return unit_id

def createAttributeType(logger: object,
                        data: dict,
                        environment: str = "production") -> int:

    ## logging
    start_time = datetime.now()
    msg_handler = messageHandler(logger=logger, level="DEBUG",
                                 labels={'function': 'CreateOrUpdateAttributeType',
                                         'endpoint': '/Attribute/CreateOrUpdateAttributeType'})
    msg_handler.logStruct(topic=f"createAttributeType: start create attribute type.\n start time: {start_time}", data=data)

    ## construct request
    if environment == "production":
        request_url = f"{PRODUCTION_ADDRESS}/Attribute/CreateOrUpdateAttributeType"
    elif environment == "development":
        request_url = f"{DEVELOPMENT_ADDRESS}/Attribute/CreateOrUpdateAttributeType"

    attribute_type_id = None

    ## request
    r = requests.post(request_url,
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

    # closing the connection
    r.close()

    return attribute_type_id

def createAttribute(logger: object,
                    data: dict,
                    environment: str = "production") -> int:

    ## logging
    start_time = datetime.now()
    msg_handler = messageHandler(logger=logger, level="DEBUG",
                                 labels={'function': 'createAttribute',
                                         'endpoint': '/Attribute/CreateOrUpdate'})
    msg_handler.logStruct(topic=f"createAttribute: start create attribute.\n start time: {start_time}",
                          data=data)

    ## construct request
    if environment == "production":
        request_url = f"{PRODUCTION_ADDRESS}/Attribute/CreateOrUpdate"
    elif environment == "development":
        request_url = f"{DEVELOPMENT_ADDRESS}/Attribute/CreateOrUpdate"

    attribute_id = None

    ## request
    r = requests.post(request_url,
                     json=data,
                      headers={'Authorization': 'Bearer ' + os.environ["YOUR_API_TOKEN"]})

    allowed_codes = [200, 400]

    if r.status_code in allowed_codes:
        resp_body = json.loads(r.text)
        resp_data = resp_body.get('data')
        success = resp_body.get('success')
        code = resp_body.get('code')

        if success:
            attribute_id = resp_data['id']

            ## logging
            msg_handler.logStruct(topic=f"createAttribute: finished create attribute type. attribute id: {attribute_id}",
                                  status_code=r.status_code,
                                  response_text=r.text,
                                  level="DEBUG")

        elif code == 11:
            attribute_id = resp_data.get('id')

            ## logging
            msg_handler.logStruct(topic=f"createAttribute: attribute already existed, attribute_id: {attribute_id}",
                                  status_code=r.status_code,
                                  response_text=r.text,
                                  level="DEBUG")

        else:
            ## logging
            msg_handler.logStruct(topic=f"createAttribute: no response data",
                                  status_code=r.status_code,
                                  response_text=r.text,
                                  level="WARNING")
    else:
        ## logging
        msg_handler.logStruct(topic=f"createAttribute: status code not {allowed_codes}",
                              status_code=r.status_code,
                              response_text=r.text,
                              level="ERROR")

    # closing the connection
    r.close()

    return attribute_id


def createSeries(logger: object,
                 data=dict,
                 environment: str = "production") -> int:

    ## logging
    start_time = datetime.now()
    msg_handler = messageHandler(logger=logger, level="DEBUG",
                                 labels={'function': 'createSeries',
                                         'endpoint': '/Series'})
    msg_handler.logStruct(topic=f"createSeries: start create serie.\n start time: {start_time}",
                          data=data)

    ## construct request
    if environment == "production":
        request_url = f"{PRODUCTION_ADDRESS}/Series"
    elif environment == "development":
        request_url = f"{DEVELOPMENT_ADDRESS}/Series"

    serie_id = None

    ## request
    r = requests.post(request_url,
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

    # closing the connection
    r.close()

    return serie_id

def createCategoryCategoryRelation(logger: object,
                                   data: dict,
                                   environment: str = "production") -> bool:

    ## logging
    msg_handler = messageHandler(logger=logger, level="DEBUG",
                                 labels={'function': 'createCategoryCategoryRelation',
                                         'endpoint': '/Relation/CreateCategoryCategory'})
    msg_handler.logStruct(topic=f"createCategoryCategoryRelation: Start create category category relation,\n start time: {datetime.now()}", data=data)

    ## construct request
    if environment == "production":
        request_url = f"{PRODUCTION_ADDRESS}/Relation/CreateCategoryCategory"
    elif environment == "development":
        request_url = f"{DEVELOPMENT_ADDRESS}/Relation/CreateCategoryCategory"

    ## request
    r = requests.post(request_url,
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

def createBrandCategoryRelation(logger: object,
                                data: dict,
                                environment: str = "production") -> None:

    ## logging
    msg_handler = messageHandler(logger=logger, level="DEBUG",
                                 labels={'function': 'createBrandCategoryRelation',
                                         'endpoint': '/Relation/CreateBrandCategory'})
    msg_handler.logStruct(topic=f"createBrandCategoryRelation: Start create brand category relation,\n start time: {datetime.now()}", data=data)

    ## construct request
    if environment == "production":
        request_url = f"{PRODUCTION_ADDRESS}/Relation/CreateBrandCategory"
    elif environment == "development":
        request_url = f"{DEVELOPMENT_ADDRESS}/Relation/CreateBrandCategory"

    ## request
    r = requests.post(request_url,
                     json=data,
                    headers={'Authorization': 'Bearer ' + os.environ["YOUR_API_TOKEN"]})

    resp_body = json.loads(r.text)
    success = resp_body.get('success')
    code = resp_body.get('code')

    if r.status_code == [200, 400]:

        if success:
            ## logging
            msg_handler.logStruct(
                topic=f"createBrandCategoryRelation: finished create relation brand category",
                status_code=r.status_code,
                response_text=r.text)

        if code in [10, 11]:
            ## logging
            msg_handler.logStruct(
                topic=f"createBrandCategoryRelation: relation already exist",
                status_code=r.status_code,
                response_text=r.text)

    else:
        ## logging
        msg_handler.logStruct(
            level="ERROR",
            topic=f"createBrandCategoryRelation: error create relation brand category",
            status_code=r.status_code,
            response_text=r.text)

def createCategoryAttributeRelation(logger: object,
                                    data: dict,
                                    environment: str = "production") -> bool:

    ## logging
    msg_handler = messageHandler(logger=logger, level="DEBUG",
                                 labels={'function': 'createCategoryAttributeRelation',
                                         'endpoint': '/Relation/CreateAttributeCategory'})
    msg_handler.logStruct(
        topic=f"createCategoryAttributeRelation: Start create category attribute relation,\n start time: {datetime.now()}", data=data)

    ## construct request
    if environment == "production":
        request_url = f"{PRODUCTION_ADDRESS}/Relation/CreateAttributeCategory"
    elif environment == "development":
        request_url = f"{DEVELOPMENT_ADDRESS}/Relation/CreateAttributeCategory"

    ## request
    r = requests.post(request_url,
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

def createProductProductRelation(logger: object,
                                 data: dict,
                                 environment: str = "production") -> bool:

    ## logging
    msg_handler = messageHandler(logger=logger, level="DEBUG",
                                 labels={'function': 'createProductProductRelation',
                                         'endpoint': '/Relation/CreateProductProduct'})
    msg_handler.logStruct(topic=f"createProductProductRelation: Start create product product relation,\n start time: {datetime.now()}", data=data)

    ## construct request
    if environment == "production":
        request_url = f"{PRODUCTION_ADDRESS}/Relation/CreateProductProduct"
    elif environment == "development":
        request_url = f"{DEVELOPMENT_ADDRESS}/Relation/CreateProductProduct"

    ## request
    r = requests.post(request_url,
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

def createCategoryProductRelation(logger: object,
                                  data: dict,
                                  environment: str = "production") -> bool:

    ## logging
    msg_handler = messageHandler(logger=logger, level="DEBUG",
                                 labels={'function': 'createCategoryProductRelation',
                                         'endpoint': '/Relation/CreateCategoryProduct'})
    msg_handler.logStruct(topic=f"createCategoryProductRelation: Start create category product relation,\n start time: {datetime.now()}", data=data)

    ## construct request
    if environment == "production":
        request_url = f"{PRODUCTION_ADDRESS}/Relation/CreateCategoryProduct"
    elif environment == "development":
        request_url = f"{DEVELOPMENT_ADDRESS}/Relation/CreateCategoryProduct"

    ## request
    r = requests.post(request_url,
                     json=data,
                    headers={'Authorization': 'Bearer ' + os.environ["YOUR_API_TOKEN"]})

    if r.status_code == 200:
        ## logging
        msg_handler.logStruct(
            topic=f"createCategoryProductRelation: finished create relation category product",
            status_code=r.status_code,
            response_text=r.text)
        return True

    else:
        ## logging
        msg_handler.logStruct(
            level="ERROR",
            topic=f"createCategoryProductRelation: error create relation category product",
            status_code=r.status_code,
            response_text=r.text)
        return False
