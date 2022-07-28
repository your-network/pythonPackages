import os
import requests
import json
from datetime import datetime
from loggingYour.messageHandler import messageHandler

def getAllCategories(logger: object) -> list:
    start_time = datetime.now()
    msg_handler = messageHandler(logger=logger, level="DEBUG",
                                 labels={'function': 'getAllCategories',
                                         'endpoint': '/Category/GetAll'})

    ## logging
    msg_handler.logStruct(topic=f"getAllCategories: Start get all categories,\n start time: {start_time}")

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
                msg_handler.logStruct(topic="getAllCategories: No new data so all categories gathered",
                               status_code=r.status_code,
                               response_text=r.text)
                break
        else:
            msg_handler.logStruct(level="ERROR",
                                  topic="getAllCategories: Error in the get all function",
                            status_code=r.status_code,
                            response_text=r.text)
            break

    msg_handler.logStruct(topic=f"getAllCategories: Finish get all categories. Length: {len(categories)}.\n processing time: {datetime.now()-start_time}",
                   data=categories[:10])

    return categories

def getAllAttributes(logger: object) -> list:
    start_time = datetime.now()
    msg_handler = messageHandler(logger=logger, level="DEBUG",
                                 labels={'function': 'getAllAttributes',
                                         'endpoint': '/Attribute'})

    ## logging
    msg_handler.logStruct(topic=f"getAllAttributes: Start get all attributes,\n start time: {start_time}")

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
                msg_handler.logStruct(
                               topic="getAllAttributes: No new data so all attributes gathered",
                               status_code=r.status_code,
                               response_text=r.text)
                break
        else:
            msg_handler.logStruct(
                           level="ERROR",
                           topic="getAllAttributes: status code not 200",
                           status_code=r.status_code,
                           response_text=r.text)
            break

    msg_handler.logStruct(topic=f"getAllAttributes: Finish get all attributes. Length: {len(attributes)}. Processing time: {datetime.now()-start_time}",
                          data=attributes[:10])

    return attributes

def getAllAttributeTypes(logger: object) -> list:
    start_time = datetime.now()
    msg_handler = messageHandler(logger=logger, level="DEBUG",
                                 labels={'function': 'getAllAttributeTypes',
                                         'endpoint': '/AttributeType'})

    ## logging
    msg_handler.logStruct(topic=f"getAllAttributeTypes: Start get all attribute types,\n start time: {start_time}")

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
                msg_handler.logStruct(topic="getAllAttributeTypes: No new data so all attribute types gathered",
                               status_code=r.status_code,
                               response_text=r.text)
                break
        else:
            msg_handler.logStruct(level="ERROR",
                                  topic="getAllAttributeTypes: status code not 200",
                           status_code=r.status_code,
                           response_text=r.text)
            break

    msg_handler.logStruct(topic=f"getAllAttributeTypes: Finish get all attributes types. Length: {len(attributeTypes)}.\n Process time: {datetime.now()-start_time}",
                   data=attributeTypes[:10])

    return attributeTypes

def getAllBrands(logger: object) -> list:
    start_time = datetime.now()
    msg_handler = messageHandler(logger=logger, level="DEBUG",
                                 labels={'function': 'getAllBrands',
                                         'endpoint': '/Brand'})

    ## logging
    msg_handler.logStruct(topic=f"getAllBrands: Start get all brands,\n start time: {start_time}")

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
                msg_handler.logStruct(topic="getAllBrands: No new data so all brands gathered",
                               status_code=r.status_code,
                               response_text=r.text)
                break

        else:
            msg_handler.logStruct(level="ERROR",
                           topic="getAllBrands: status code not 200",
                           status_code=r.status_code,
                           response_text=r.text)
            break

    msg_handler.logStruct(topic=f"getAllBrands: Finish get all brands. Length: {len(brands)}", data=brands[:10])

    return brands

def getAllAttributeTypeUnit(logger: object) -> list:
    start_time = datetime.now()
    msg_handler = messageHandler(logger=logger, level="DEBUG",
                                 labels={'function': 'getAllAttributeTypeUnit',
                                         'endpoint': '/AttributeTypeUnit'})

    ## logging
    msg_handler.logStruct(topic=f"getAllAttributeTypeUnit: Start get all attribute type units,\n start time: {start_time}")

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
                msg_handler.logStruct(topic="getAllAttributeTypeUnit: No new data so all attribute type units gathered",
                               status_code=r.status_code,
                               response_text=r.text)
                break

        else:
            msg_handler.logStruct(level="ERROR",
                           topic="getAllAttributeTypeUnit: status code not 200",
                           status_code=r.status_code,
                           response_text=r.text)
            break

    msg_handler.logStruct(topic=f"getAllAttributeTypeUnit: Finish get all attribute type units. Length: {len(attributeTypeUnits)}.\n Processing time: {datetime.now()-start_time}",
                   data=attributeTypeUnits[:10])

    return attributeTypeUnits

def getAllSeries(logger: object) -> list:
    start_time = datetime.now()
    msg_handler = messageHandler(logger=logger, level="DEBUG",
                                 labels={'function': 'getAllSeries',
                                         'endpoint': '/Series'})

    ## logging
    msg_handler.logStruct(topic=f"getAllSeries: Start get all series,\n start time: {start_time}")

    next_page = True
    page = 1
    series = []
    while next_page:
        r = requests.get(f"https://api.yourcontent.io/Series?resultsPerPage=10000&page={page}",
                         headers={'Authorization': 'Bearer ' + os.environ["YOUR_API_TOKEN"]})

        if r.status_code == 200:
            result = json.loads(r.text)
            data = result.get('data')
            if data.get('results'):
                series = series + data['results']
                page += 1
            else:
                msg_handler.logStruct(topic="getAllSeries: No new data so all categories gathered",
                               status_code=r.status_code,
                               response_text=r.text)
                break
        else:
            msg_handler.logStruct(level="ERROR",
                                  topic="getAllSeries: Error in the get all function",
                            status_code=r.status_code,
                            response_text=r.text)
            break

    msg_handler.logStruct(topic=f"getAllSeries: Finish get all series. Length: {len(series)}.\n processing time: {datetime.now()-start_time}",
                   data=series[:10])

    return series

