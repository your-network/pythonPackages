import os
import requests
import json
from datetime import datetime

def createCategory(payload):
    r = requests.post('https://api.yourcontent.io/Category/CreateOrUpdate',
                      json=payload,
                      headers={'Authorization': 'Bearer ' + os.environ["YOUR_API_HEADER"]})
    if r.status_code == 200:
        resp_data = json.loads(r.text).get('data')
        if resp_data:
            cat_id = resp_data.get('id')
            print(f"Call Success, response category id: {cat_id}")
            return cat_id
        else:
            print(f"Call Success but no response category id")
            return None
    else:
        print(f"Call failed. Response code: {r.status_code}, text: {r.text}")
        return None

def createProductBulk(data_bulk):
    start_time = datetime.now()
    print(f"YourApi process product bulk. Start time: {start_time}")
    r = requests.get(f"https://api.yourcontent.io/Product/CreateOrUpdateBulk",
                     json=data_bulk,
                     headers={'Authorization': 'Bearer ' + os.environ["YOUR_API_HEADER"]})
    print(f"Bulk response: {r.text}")
    if r.status_code == 200:
        print(f"Success in product bulk insert. Number products: {len(data_bulk)}")
        resp_data = json.loads(r.text)
        product_bulk_response = resp_data['data']
    else:
        print(f"Error in product bulk insert. Response text: {r}")
        product_bulk_response = None

    end_time = datetime.now()
    print(f"Api product bulk insert finished, processing time: {end_time - start_time}")
    return product_bulk_response

def createAttributeUnit(data):
    r = requests.post(f"https://api.yourcontent.io/Attribute/CreateOrUpdateAttributeTypeUnit",
                     json=data,
                     headers={'Authorization': 'Bearer ' + os.environ["YOUR_API_HEADER"]})
    # print(f"Attribute Unit create response: {r.content}")
    if r.status_code == 200:
        # print(f"Attribute Unit create Success")
        resp_data = json.loads(r.text)
        unit_id = resp_data['data']['id']
    else:
        print(f"Attribute Unit create Error."
              f""
              f"Data: {data},"
              f""
              f"Response text: {r.content}")
        unit_id = None
    return unit_id

def createAttributeType(data):
    r = requests.post(f"https://api.yourcontent.io/Attribute/CreateOrUpdateAttributeType",
                     json=data,
                     headers={'Authorization': 'Bearer ' + os.environ["YOUR_API_HEADER"]})
    # print(f"Attribute Type create response: {r.content}")
    if r.status_code == 200:
        # print(f"Attribute Type create Success")
        resp_data = json.loads(r.text)
        attribute_type_id = resp_data['data']['id']
    else:
        print(f"Attribute Type create Error. Response text: {r.content}")
        attribute_type_id = None
    return attribute_type_id

def createAttribute(data):
    r = requests.post(f"https://api.yourcontent.io/Attribute/CreateOrUpdate",
                     json=data,
                      headers={'Authorization': 'Bearer ' + os.environ["YOUR_API_HEADER"]})
    # print(f"Attribute create response: {r.content}")
    if r.status_code == 200:
        # print(f"Attribute create Success")
        resp_data = json.loads(r.text)
        attribute_id = resp_data['data']['id']
    else:
        print(f"Attribute create Error. Response text: {r.content}")
        attribute_id = None
    return attribute_id