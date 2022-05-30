import os
import requests
import json
from datetime import datetime
import logging
logging.basicConfig(filename="createApiLogs.log", level=logging.INFO)

def createCategory(payload):
    r = requests.post('https://api.yourcontent.io/Category/CreateOrUpdate',
                      json=payload,
                      headers={'Authorization': 'Bearer ' + os.environ["YOUR_API_TOKEN"]})
    if r.status_code == 200:
        resp_data = json.loads(r.text).get('data')
        if resp_data:
            cat_id = resp_data.get('id')
            print(f"Call Success, response category id: {cat_id}")
            return cat_id
        else:
            logging.error(f"Call create category success but no response data."
                          f""
                          f"Response code: {r.status_code}, "
                          f""
                          f"text: {r.content}, "
                          f""
                          f"data: {payload}")
            print(f"Call Success but no response category id")
            return None
    else:
        logging.error(f"Call create category failed. "
                      f""
                      f"Response code: {r.status_code}, "
                      f""
                      f"Content response: {r.content}, "
                      f""
                      f"data: {payload}")
        print(f"Call failed. Response code: {r.status_code}, text: {r.content}")
        return None

def createProductBulk(data_bulk):
    start_time = datetime.now()
    print(f"YourApi process product bulk. Start time: {start_time}")
    r = requests.get(f"https://api.yourcontent.io/Product/CreateOrUpdateBulk",
                     json=data_bulk,
                     headers={'Authorization': 'Bearer ' + os.environ["YOUR_API_TOKEN"]})
    print(f"Bulk response: {r.text}")
    if r.status_code == 200:
        print(f"Success in product bulk insert. Number products: {len(data_bulk)}")
        resp_data = json.loads(r.text)
        product_bulk_response = resp_data['data']
    else:
        logging.error(f"Call create bulk product failed. "
                      f""
                      f"Response code: {r.status_code}, "
                      f""
                      f"Content response: {r.content}")
        print(f"Error in product bulk insert. Response text: {r.content}")
        product_bulk_response = None

    end_time = datetime.now()
    print(f"Api product bulk insert finished, processing time: {end_time - start_time}")
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
        logging.error(f"Call create attribute unit failed. "
                      f""
                      f"Response code: {r.status_code}, "
                      f""
                      f"Content response: {r.content}, "
                      f""
                      f"data: {data}")
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
        logging.error(f"Call Attribute Type failed. "
                      f""
                      f"Response code: {r.status_code}, "
                      f""
                      f"Content response: {r.content}, "
                      f""
                      f"data: {data}")
        print(f"Attribute Type create Error. Response text: {r.content}")
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
        logging.error(f"Call Attribute create failed. "
                      f""
                      f"Response code: {r.status_code}, "
                      f""
                      f"Content response: {r.content}, "
                      f""
                      f"data: {data}")
        print(f"Attribute create Error. Response text: {r.content}")
        attribute_id = None
    return attribute_id

def createCategoryCategoryRelation(data):
    r = requests.post(f"https://api.yourcontent.io/Relation/CreateCategoryCategory",
                     json=data,
                    headers={'Authorization': 'Bearer ' + os.environ["YOUR_API_TOKEN"]})
    if r.status_code == 200:
        return True
    else:
        # logging.error(f"Call create category category relation failed. "
        #               f""
        #               f"Response code: {r.status_code}, "
        #               f""
        #               f"Content response: {r.content}, "
        #               f""
        #               f"data: {data}")
        # print(f"Create category category relation Error. Response text: {r.content}")
        return False

def createCategoryProductRelation(data):
    r = requests.post(f"https://api.yourcontent.io/Relation/CreateCategoryProduct",
                     json=data,
                    headers={'Authorization': 'Bearer ' + os.environ["YOUR_API_TOKEN"]})
    if r.status_code == 200:
        return True
    else:
        logging.error(f"Call create category product relation failed. "
                      f""
                      f"Response code: {r.status_code}, "
                      f""
                      f"Content response: {r.content}, "
                      f""
                      f"data: {data}")
        print(f"Create category product relation Error. Response text: {r.content}")
        return False

def createProductProductRelation(data):
    r = requests.post(f"https://api.yourcontent.io/Relation/CreateProductProduct",
                     json=data,
                    headers={'Authorization': 'Bearer ' + os.environ["YOUR_API_TOKEN"]})
    if r.status_code == 200:
        return True
    else:
        logging.error(f"Call create product product relation failed. "
                      f""
                      f"Response code: {r.status_code}, "
                      f""
                      f"Content response: {r.content}, "
                      f""
                      f"data: {data}")
        print(f"Create product product relation Error. Response text: {r.content}")
        return False
