import os
import requests
import json
from datetime import datetime
import logging
from helpersYour.logging import logging_error_message

def getAllCategories():
    next_page = True
    page = 1
    categories = []
    while next_page:
        r = requests.get(f"https://api.yourcontent.io/Category/GetAll?resultsPerPage=10000&page={page}",
                         headers={'Authorization': 'Bearer ' + os.environ["YOUR_API_TOKEN"]})
        print(f"print response: {r.text}")
        logging_error_message("get", "Response category get all", None, r.text, r.status_code)
        if r.status_code == 200:
            result = json.loads(r.text)
            data = result.get('data')
            if data.get('results'):
                categories = categories + data['results']
                page += 1
            else:
                break
        else:
            logging_error_message("get", "Category get all", None, r.text, r.status_code)
            break

    return categories

def getAllAttributes():
    next_page = True
    page = 1
    attributes = []
    while next_page:
        r = requests.get(f"https://api.yourcontent.io/Attribute?resultsPerPage=10000&page={page}",
                         headers={'Authorization': 'Bearer ' + os.environ["YOUR_API_TOKEN"]})
        if r.status_code == 200:
            result = json.loads(r.text)
            data = result.get('data')
            if len(data) > 0:
                attributes = attributes + data
                page += 1
            else:
                break
        else:
            logging_error_message("get", "Attributes get all", None, r.text, r.status_code)
            break

    return attributes

def getAllAttributeTypes():
    next_page = True
    page = 1
    attributeTypes = []
    while next_page:
        r = requests.get(f"https://api.yourcontent.io/AttributeType?resultsPerPage=10000&page={page}",
                         headers={'Authorization': 'Bearer ' + os.environ["YOUR_API_TOKEN"]})
        if r.status_code == 200:
            result = json.loads(r.text)
            data = result.get('data')
            if len(data) > 0:
                attributeTypes = attributeTypes + data
                page += 1
            else:
                break
        else:
            logging_error_message("get", "Attribute Types get all", None, r.text, r.status_code)
            break

    return attributeTypes

def getAllBrands():
    next_page = True
    page = 1
    brands = []
    while next_page:
        r = requests.get(f"https://api.yourcontent.io/Brand?resultsPerPage=10000&page={page}",
                         headers={'Authorization': 'Bearer ' + os.environ["YOUR_API_TOKEN"]})

        if r.status_code == 200:
            result = json.loads(r.text)
            data = result.get('data')
            if data.get('results'):
                brands = brands + data['results']
                page += 1
            else:
                break
        else:
            logging_error_message("get", "Brands get all", None, r.text, r.status_code)
            break

    return brands

def getAllAttributeTypeUnit():
    next_page = True
    page = 1
    attributeTypeUnits = []
    while next_page:
        r = requests.get(f"https://api.yourcontent.io/AttributeTypeUnit?resultsPerPage=10000&page={page}",
                         headers={'Authorization': 'Bearer ' + os.environ["YOUR_API_TOKEN"]})
        if r.status_code == 200:
            result = json.loads(r.text)
            data = result.get('data')
            if len(data) > 0:
                attributeTypeUnits = attributeTypeUnits + data
                page += 1
            else:
                break
        else:
            logging_error_message("get", "Attribute Type Units get all", None, r.text, r.status_code)
            break

    return attributeTypeUnits

