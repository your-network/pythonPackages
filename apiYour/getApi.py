import os
import requests
import json
from loggingYour.messageHandler import messageHandler

def getAllCategories(logger: object) -> list:
    next_page = True
    page = 1
    categories = []
    while next_page:
        r = requests.get(f"https://api.yourcontent.io/Category/GetAll?resultsPerPage=10000&page={page}",
                         headers={'Authorization': 'Bearer ' + os.environ["YOUR_API_TOKEN"]})
        if r.status_code == 200:
            result = json.loads(r.text)
            data = result.get('data')
            if data.get('results'):
                categories = categories + data['results']
                page += 1
            else:
                messageHandler(logger,
                               "INFO",
                               "getAllCategories: No new data so all categories gathered",
                               data=categories,
                               status_code=r.status_code,
                               response_text=r.text)
                break
        else:
            messageHandler(logger,
                            "ERROR",
                            "getAllCategories: Error in the get all function",
                            data=categories,
                            status_code=r.status_code,
                            response_text=r.text)
            break

    messageHandler(logger,
                   "INFO",
                   f"getAllCategories: Finish get all categories. Length: {len(categories)}",
                   data=categories)

    return categories

def getAllAttributes() -> list:
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
            messageHandler("get", "Attributes get all", None, r.text, r.status_code)
            break

    return attributes

def getAllAttributeTypes() -> list:
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
            messageHandler("get", "Attribute Types get all", None, r.text, r.status_code)
            break

    return attributeTypes

def getAllBrands() -> list:
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
            messageHandler("get", "Brands get all", None, r.text, r.status_code)
            break

    return brands

def getAllAttributeTypeUnit() -> list:
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
            messageHandler("get", "Attribute Type Units get all", None, r.text, r.status_code)
            break

    return attributeTypeUnits

