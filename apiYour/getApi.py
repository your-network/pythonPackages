import os
import requests
import json
from datetime import datetime
import logging
from apiYour.helpers import logging_error_message
logging.basicConfig(filename="getApiLogs.log", level=logging.INFO)

def getAllCategories():
    next_page = True
    page = 1
    categories = []
    while next_page:
        r = requests.get(f"https://api.yourcontent.io/Category/GetAll?resultsPerPage=10000&page={page}",
                         headers={'Authorization': 'Bearer ' + os.environ["YOUR_API_TOKEN"]})
        if r.status_code == 200:
            result = json.loads(r.text)
            data = result.get('data')
            if len(data) > 0:
                categories = categories + data
                page += 1
            else:
                break
        else:
            logging_error_message("Category get all", r.status_code, r.content, None)
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
            logging_error_message("Attributes get all", r.status_code, r.content, None)
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
            logging_error_message("Attribute Types get all", r.status_code, r.content, None)
            break

    return attributeTypes

def getAllBrands():
    overal_start_time = datetime.now()
    print(f"Start brand getall: {overal_start_time}")
    next_page = True
    page = 1
    brands = []
    while next_page:
        call_start_time = datetime.now()
        print(f"Start call time: {call_start_time}")
        r = requests.get(f"https://api.yourcontent.io/Brand?resultsPerPage=10000&page={page}",
                         headers={'Authorization': 'Bearer ' + os.environ["YOUR_API_TOKEN"]})
        start_processing_time = datetime.now()
        print(f"end call processing time: {start_processing_time-call_start_time}, start processing time: {start_processing_time}")

        if r.status_code == 200:
            result = json.loads(r.text)
            data = result.get('data')
            if len(data) > 0:
                brands = brands + data
                page += 1
                print(f"Append data plus next page number processing time: {datetime.now() - start_processing_time}")
            else:
                print(f"Last page processing time: {datetime.now() - start_processing_time}")
                break

        else:
            logging_error_message("Brands get all", r.status_code, r.content, None)
            break

    print(f"End brand getall, overall processing time: {datetime.now() - overal_start_time}")
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
            logging_error_message("Attribute Types Units get all", r.status_code, r.content, None)
            break

    return attributeTypeUnits

