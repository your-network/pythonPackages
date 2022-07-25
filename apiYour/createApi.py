import os
import requests
import json
from datetime import datetime
from loggingYour.logging import logging_error_message

def createCategory(payload):
    r = requests.post('https://api.yourcontent.io/Category/',
                      json=payload,
                      headers={'Authorization': 'Bearer ' + os.environ["YOUR_API_TOKEN"]})
    if r.status_code == 200:
        resp_data = json.loads(r.text).get('data')
        if resp_data:
            cat_id = resp_data.get('id')
            media = resp_data.get('duplicates')
            return cat_id, media
    else:
        logging_error_message("create", "create category", payload, r.text, r.status_code)
        return None, None

def createProductBulk(data_bulk):
    start_time = datetime.now()
    print(f"YourApi process product bulk. Start time: {start_time}")
    r = requests.post(f"https://api.yourcontent.io/Product/CreateOrUpdateBulk",
                     json=data_bulk,
                     headers={'Authorization': 'Bearer ' + os.environ["YOUR_API_TOKEN"]})
    print(f"Bulk response: {r.text}")
    if r.status_code == 200:
        print(f"Success in product bulk insert. Number products: {len(data_bulk)}")
        resp_data = json.loads(r.text)
        product_bulk_response = resp_data
    else:
        logging_error_message("create", "bulk product insert", data_bulk, r.text, r.status_code)
        product_bulk_response = None

    end_time = datetime.now()
    print(f"Api product bulk insert finished, processing time: {end_time - start_time}")
    return product_bulk_response

def createProductQueue(data_bulk):
    start_time = datetime.now()
    print(f"YourApi process product queue. Start time: {start_time}")
    r = requests.post(f"https://api.yourcontent.io/Product/QueueForCreateBulk",
                     json=data_bulk,
                     headers={'Authorization': 'Bearer ' + os.environ["YOUR_API_TOKEN"]})
    print(f"Bulk response: {r.text}")
    if r.status_code == 200:
        print(f"Success in product queue insert. Number products: {len(data_bulk)}")
        resp_data = json.loads(r.text)
        product_bulk_response = resp_data
    else:
        logging_error_message("create", "queue product insert", data_bulk, r.text, r.status_code)
        product_bulk_response = None

    end_time = datetime.now()
    print(f"Api product queue insert finished, processing time: {end_time - start_time}")
    return product_bulk_response

def createAttributeUnit(data):
    r = requests.post(f"https://api.yourcontent.io/Attribute/CreateOrUpdateAttributeTypeUnit",
                     json=data,
                     headers={'Authorization': 'Bearer ' + os.environ["YOUR_API_TOKEN"]})
    # print(f"Attribute Unit create response: {r.content}")
    if r.status_code == 200:
        # print(f"Attribute Unit create Success")
        resp_data = json.loads(r.text)
        unit_id = resp_data['data']['id']
    else:
        logging_error_message("create", "create attribute unit", data, r.text, r.status_code)
        unit_id = None
    return unit_id

def createAttributeType(data):
    r = requests.post(f"https://api.yourcontent.io/Attribute/CreateOrUpdateAttributeType",
                     json=data,
                     headers={'Authorization': 'Bearer ' + os.environ["YOUR_API_TOKEN"]})
    # print(f"Attribute Type create response: {r.content}")
    if r.status_code == 200:
        # print(f"Attribute Type create Success")
        resp_data = json.loads(r.text)
        attribute_type_id = resp_data['data']['id']
    else:
        logging_error_message("create", "create attribute type", data, r.text, r.status_code)
        attribute_type_id = None
    return attribute_type_id

def createAttribute(data):
    r = requests.post(f"https://api.yourcontent.io/Attribute/CreateOrUpdate",
                     json=data,
                      headers={'Authorization': 'Bearer ' + os.environ["YOUR_API_TOKEN"]})
    # print(f"Attribute create response: {r.content}")
    if r.status_code == 200:
        # print(f"Attribute create Success")
        resp_data = json.loads(r.text)
        attribute_id = resp_data['data']['id']
    else:
        logging_error_message("create", "create attribute", data, r.text, r.status_code)
        attribute_id = None
    return attribute_id

def createBrand(data):
    r = requests.post(f"https://api.yourcontent.io/Brand",
                     json=data,
                      headers={'Authorization': 'Bearer ' + os.environ["YOUR_API_TOKEN"]})
    if r.status_code == 200:
        resp_data = json.loads(r.text)
        brand_id = resp_data['data']['id']
    else:
        logging_error_message("create", "create brand", data, r.text, r.status_code)
        brand_id = None
    return brand_id

def createSeries(data):
    r = requests.post(f"https://api.yourcontent.io/Series",
                     json=data,
                      headers={'Authorization': 'Bearer ' + os.environ["YOUR_API_TOKEN"]})
    if r.status_code == 200:
        resp_data = json.loads(r.text)
        serie_id = resp_data['data']['id']
    else:
        logging_error_message("create", "create serie", data, r.text, r.status_code)
        serie_id = None
    return serie_id

def createCategoryCategoryRelation(data):
    r = requests.post(f"https://api.yourcontent.io/Relation/CreateCategoryCategory",
                     json=data,
                    headers={'Authorization': 'Bearer ' + os.environ["YOUR_API_TOKEN"]})
    if r.status_code == 200:
        return True
    else:
        logging_error_message("create", "create category category relation", data, r.text, r.status_code)
        return False

def createBrandCategoryRelation(data):
    r = requests.post(f"https://api.yourcontent.io/Relation/CreateBrandCategory",
                     json=data,
                    headers={'Authorization': 'Bearer ' + os.environ["YOUR_API_TOKEN"]})
    if r.status_code == 200:
        return True
    else:
        logging_error_message("create", "create brand category relation", data, r.text, r.status_code)
        return False

def createCategoryAttributeRelation(data):
    r = requests.post(f"https://api.yourcontent.io/Relation/CreateAttributeCategory",
                     json=data,
                    headers={'Authorization': 'Bearer ' + os.environ["YOUR_API_TOKEN"]})
    if r.status_code == 200:
        return True
    else:
        logging_error_message("create", "create category product relation", data, r.text, r.status_code)
        return False

def createProductProductRelation(data):
    r = requests.post(f"https://api.yourcontent.io/Relation/CreateProductProduct",
                     json=data,
                    headers={'Authorization': 'Bearer ' + os.environ["YOUR_API_TOKEN"]})
    if r.status_code == 200:
        return True
    else:
        logging_error_message("create", "create product product relation", data, r.text, r.status_code)
        return False
