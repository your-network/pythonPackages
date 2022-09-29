import os
import requests
import json
from datetime import datetime
from loggingYour.messageHandler import messageHandler
from apiYour.settingsApi import PRODUCTION_ADDRESS, DEVELOPMENT_ADDRESS

def getCategory(logger: object,
                categoryId: int,
                lang: str = "EN",
                environment: str = "production") -> dict:
    ## logging
    msg_handler = messageHandler(logger=logger, level="DEBUG",
                                 labels={'function': 'getCategory',
                                         'endpoint': '/Category/{categoryId'})
    msg_handler.logStruct(topic=f"getCategory: Start get category", data=categoryId)

    ## construct request
    if environment == "production":
        request_url = f"{PRODUCTION_ADDRESS}/Category/{categoryId}"
    elif environment == "development":
        request_url = f"{DEVELOPMENT_ADDRESS}/Category/{categoryId}"

    base_params = {"lang": lang}

    response = requests.get(request_url,
                     headers={'Authorization': 'Bearer ' + os.environ["YOUR_API_TOKEN"]},
                     params=base_params)

    if response.status_code == 200:
        result = json.loads(response.text)
        data = result.get('data')

        if data:
            # closing the connection
            response.close()

            return data
        else:
            msg_handler.logStruct(topic="getCategory: No data on category get",
                                  status_code=response.status_code,
                                  response_text=response.text)

            # closing the connection
            response.close()

            return {}
    else:
        msg_handler.logStruct(level="ERROR",
                              topic="getCategory: Error in the get category function",
                              status_code=response.status_code,
                              response_text=response.text)

        # closing the connection
        response.close()

        return {}

def getAllCategories(logger: object,
                     query: str = None,
                     resultsPerPage: int = 1000,
                     page: int = 1,
                     categoryId: int = None,
                     brandId: int = None,
                     withImagesOnly: bool = False,
                     withChildrenOnly: bool = False,
                     withProductsOnly: bool = False,
                     lang: str = "EN",
                     sortBy: str = None,
                     includeServiceCategories: bool = False,
                     environment: str = "production",
                     session: object = None) -> list:

    start_time = datetime.now()
    msg_handler = messageHandler(logger=logger, level="DEBUG",
                                 labels={'function': 'getAllCategories',
                                         'endpoint': '/Category/GetAll'})

    ## logging
    msg_handler.logStruct(topic=f"getAllCategories: Start get all categories.\n start time: {start_time}")

    ## construct request
    if environment == "production":
        request_url = f"{PRODUCTION_ADDRESS}/Category/GetAll"
    elif environment == "development":
        request_url = f"{DEVELOPMENT_ADDRESS}/Category/GetAll"

    base_params = {"resultsPerPage": resultsPerPage,
                   "withImagesOnly": withImagesOnly,
                   "withChildrenOnly": withChildrenOnly,
                   "withProductsOnly": withProductsOnly,
                   "includeServiceCategories": includeServiceCategories,
                   "lang": lang,
                   "page": page}

    if categoryId:
        base_params.update({"categoryId": categoryId})
    if brandId:
        base_params.update({"brandId": brandId})
    if query:
        base_params.update({"query": query})
    if sortBy:
        base_params.update({"sortBy": sortBy})

    next_page = True
    categories = []
    while next_page:
        base_params.update({"page": page})

        ## logging
        msg_handler.logStruct(topic=f"getAllCategories: Request {request_url} with params: {base_params}")

        ## handle request through session or normal
        if session:
            r = session.get(url=request_url,
                            params=base_params,
                            headers={'Authorization': 'Bearer ' + os.environ["YOUR_API_TOKEN"]})
        else:
            r = requests.get(url=request_url,
                             params=base_params,
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

    msg_handler.logStruct(topic=f"getAllCategories: Finish get all categories. Length: {len(categories)}.\n processing time: {datetime.now()-start_time}")

    if session == None:
        # closing the connection
        r.close()

    return categories

def getCategoryChilds(logger: object,
                      categoryId: int,
                      resultsPerPage: int = 1000,
                      page: int = 1,
                      lang: str = "EN",
                      sortBy: str = None,
                      includeServiceCategories: bool = False,
                      environment: str = "production") -> list:

    start_time = datetime.now()
    msg_handler = messageHandler(logger=logger, level="DEBUG",
                                 labels={'function': 'getCategoryChilds',
                                         'endpoint': '/Category/{categoryId}/Categories'})

    ## logging
    msg_handler.logStruct(topic=f"getCategoryChilds: Start get all category childs")

    ## construct request
    if environment == "production":
        request_url = f"{PRODUCTION_ADDRESS}/Category/{categoryId}/Categories"
    elif environment == "development":
        request_url = f"{DEVELOPMENT_ADDRESS}/Category/{categoryId}/Categories"

    base_params = {"resultsPerPage": resultsPerPage,
                   "includeServiceCategories": includeServiceCategories,
                   "lang": lang,
                   "page": page}

    if sortBy:
        base_params.update({"sortBy": sortBy})

    next_page = True
    category_childs = []
    while next_page:
        base_params.update({"page": page})

        ## logging
        msg_handler.logStruct(topic=f"getCategoryChilds: Request {request_url} with params: {base_params}")

        r = requests.get(request_url,
                         headers={'Authorization': 'Bearer ' + os.environ["YOUR_API_TOKEN"]},
                         params=base_params)

        if r.status_code == 200:
            result = json.loads(r.text)
            data = result.get('data')
            if data.get('results'):
                category_childs = category_childs + data['results']
                page += 1
            else:
                msg_handler.logStruct(topic="getCategoryChilds: No new data so all categories childs gathered",
                                      status_code=r.status_code,
                                      response_text=r.text)
                break
        else:
            msg_handler.logStruct(level="ERROR",
                                  topic="getCategoryChilds: Error in the get all function",
                                  status_code=r.status_code,
                                  response_text=r.text)
            break

    msg_handler.logStruct(
        topic=f"getAllCategories: Finish get all category childs. Length: {len(category_childs)}.\n processing time: {datetime.now() - start_time}")

    # closing the connection
    r.close()

    return category_childs

def getAllAttributes(logger: object,
                     resultsPerPage: int = 1000,
                     environment: str = "production",
                     page: int = 1,
                     lang: str = "EN",
                     categoryId: int = None,
                     session: object = None) -> list:

    ## logging
    start_time = datetime.now()
    msg_handler = messageHandler(logger=logger, level="DEBUG",
                                 labels={'function': 'getAllAttributes',
                                         'endpoint': '/Attribute'})
    msg_handler.logStruct(topic=f"getAllAttributes: Start get all attributes")

    ## construct request
    if environment == "production":
        request_url = f"{PRODUCTION_ADDRESS}/Attribute"
    elif environment == "development":
        request_url = f"{DEVELOPMENT_ADDRESS}/Attribute"

    base_params = {"resultsPerPage": resultsPerPage,
                   "lang": lang,
                   "page": page}

    if categoryId:
        base_params.update({"categoryId": categoryId})

    next_page = True
    attributes = []
    while next_page:
        base_params.update({"page": page})

        ## logging
        msg_handler.logStruct(topic=f"getAllAttributes: Request {request_url} with params: {base_params}")

        ## handle request through session or normal
        if session:
            r = session.get(url=request_url,
                            params=base_params,
                            headers={'Authorization': 'Bearer ' + os.environ["YOUR_API_TOKEN"]})
        else:
            r = requests.get(url=request_url,
                             params=base_params,
                             headers={'Authorization': 'Bearer ' + os.environ["YOUR_API_TOKEN"]})

        if r.status_code == 200:
            result = json.loads(r.text)
            data = result['data'].get('results', [])
            if data:
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

    msg_handler.logStruct(topic=f"getAllAttributes: Finish get all attributes. Length: {len(attributes)}."
                                f"Processing time: {datetime.now()-start_time}")

    if session == None:
        # closing the connection
        r.close()

    return attributes

def getAllAttributeTypes(logger: object,
                         environment: str = "production") -> list:

    start_time = datetime.now()
    msg_handler = messageHandler(logger=logger, level="DEBUG",
                                 labels={'function': 'getAllAttributeTypes',
                                         'endpoint': '/AttributeType'})

    ## logging
    msg_handler.logStruct(topic=f"getAllAttributeTypes: Start get all attribute types,\n start time: {start_time}")

    ## construct request
    if environment == "production":
        request_url = PRODUCTION_ADDRESS
    elif environment == "development":
        request_url = DEVELOPMENT_ADDRESS

    next_page = True
    page = 1
    attributeTypes = []
    while next_page:
        r = requests.get(f"{request_url}/AttributeType?resultsPerPage=10000&page={page}",
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

    msg_handler.logStruct(topic=f"getAllAttributeTypes: Finish get all attributes types. Length: {len(attributeTypes)}.\n Process time: {datetime.now()-start_time}")

    # closing the connection
    r.close()

    return attributeTypes

def getAllBrands(logger: object,
                 query: str = None,
                 resultsPerPage: int = 1000,
                 page: int = 1,
                 withImagesOnly: bool = False,
                 desc: bool = False,
                 lang: str = "EN",
                 sortBy: str = None,
                 environment: str = "production",
                 connection: object = None) -> list:

    start_time = datetime.now()
    msg_handler = messageHandler(logger=logger, level="DEBUG",
                                 labels={'function': 'getAllBrands',
                                         'endpoint': '/Brand'})

    ## logging
    msg_handler.logStruct(topic=f"getAllBrands: Start get all brands,\n start time: {start_time}")

    ## construct request
    if environment == "production":
        request_url = f"{PRODUCTION_ADDRESS}/Brand"
    elif environment == "development":
        request_url = f"{DEVELOPMENT_ADDRESS}/Brand"

    base_params = {"resultsPerPage": resultsPerPage,
                   "withImagesOnly": withImagesOnly,
                   "desc": desc,
                   "lang": lang,
                   "page": page}

    if query:
        base_params.update({"query": query})
    if sortBy:
        base_params.update({"sortBy": sortBy})

    next_page = True
    page = 1
    brands = []
    while next_page:
        base_params.update({"page": page})

        ## logging
        msg_handler.logStruct(topic=f"getAllBrands: Request {request_url} with params: {base_params}")

        ## handle request through session or normal
        no_error = True
        if connection:
            ## process request from connection pool
            r = connection.request(method="GET",
                                   url=request_url,
                                   fields=base_params,
                                   headers={'Authorization': 'Bearer ' + os.environ["YOUR_API_TOKEN"]})

            response_code = r.status
            response_text = r.data
            if response_code == 200:
                json.loads(r.data.decode('utf-8'))

            else:
                no_error = False

        else:
            ## process request with requests library. Single connection & request
            r = requests.get(url=request_url,
                             params=base_params,
                             headers={'Authorization': 'Bearer ' + os.environ["YOUR_API_TOKEN"]})

            response_code = r.status_code
            response_text = r.text
            if response_code == 200:
                result = json.loads(r.text)
            else:
                no_error = False

        if no_error:
            ## process data
            data = result.get('data')
            if data.get('results'):
                brands = brands + data['results']
                page += 1
            else:
                msg_handler.logStruct(topic="getAllBrands: No new data so all brands gathered",
                               status_code=response_code,
                               response_text=response_text)
                break

        elif no_error == False:
            ## process if error was in call
            msg_handler.logStruct(level="ERROR",
                           topic="getAllBrands: status code not 200",
                           status_code=response_code,
                           response_text=response_text)
            break

    msg_handler.logStruct(topic=f"getAllBrands: Finish get all brands. Length: {len(brands)}")

    if connection == None:
        # closing the connection
        r.close()

    return brands

def getAllAttributeTypeUnit(logger: object,
                            environment: str = "production") -> list:
    start_time = datetime.now()
    msg_handler = messageHandler(logger=logger, level="DEBUG",
                                 labels={'function': 'getAllAttributeTypeUnit',
                                         'endpoint': '/AttributeTypeUnit'})

    ## logging
    msg_handler.logStruct(topic=f"getAllAttributeTypeUnit: Start get all attribute type units,\n start time: {start_time}")

    ## construct request
    if environment == "production":
        request_url = PRODUCTION_ADDRESS
    elif environment == "development":
        request_url = DEVELOPMENT_ADDRESS

    next_page = True
    page = 1
    attributeTypeUnits = []
    while next_page:
        r = requests.get(f"{request_url}/AttributeTypeUnit?resultsPerPage=10000&page={page}",
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

    msg_handler.logStruct(topic=f"getAllAttributeTypeUnit: Finish get all attribute type units. Length: {len(attributeTypeUnits)}.\n Processing time: {datetime.now()-start_time}")

    # closing the connection
    r.close()

    return attributeTypeUnits

def getAllSeries(logger: object,
                 resultsPerPage: int = 1000,
                 page: int = 1,
                 environment: str = "production",
                 connection: object = None) -> list:

    start_time = datetime.now()
    msg_handler = messageHandler(logger=logger, level="DEBUG",
                                 labels={'function': 'getAllSeries',
                                         'endpoint': '/Series'})

    ## logging
    msg_handler.logStruct(topic=f"getAllSeries: Start get all series,\n start time: {start_time}")

    ## construct request
    if environment == "production":
        request_url = f"{PRODUCTION_ADDRESS}/Series"
    elif environment == "development":
        request_url = f"{DEVELOPMENT_ADDRESS}/Series"

    base_params = {"resultsPerPage": resultsPerPage}

    next_page = True
    series = []
    try:
        while next_page:
            base_params.update({"page": page})
            ## handle request through session or normal
            if connection:
                r = connection.get(url=request_url,
                                params=base_params,
                                headers={'Authorization': 'Bearer ' + os.environ["YOUR_API_TOKEN"]})
            else:
                r = requests.get(url=request_url,
                                 params=base_params,
                                 headers={'Authorization': 'Bearer ' + os.environ["YOUR_API_TOKEN"]})

            if r.status_code == 200:
                result = json.loads(r.text)
                data = result.get('data')
                if data:
                    ## logging
                    msg_handler.logStruct(topic="getAllSeries: get request finished with data present")

                    series = series + data
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

    except Exception as e:
        msg_handler.logStruct(topic="getAllSeries: Error getting all series",
                              error_message=str(e))

    msg_handler.logStruct(topic=f"getAllSeries: Finish get all series. Length: {len(series)}.\n processing time: {datetime.now()-start_time}")

    if connection == None:
        # closing the connection
        r.close()

    return series

def getAllProducts(logger: object,
                   max_results: int = 100000000,
                   page_results: int = 1000,
                   category_id: int = None,
                   brand_id: int = None,
                   language: str = "en",
                   sorting: str = "Popularity",
                   optional_fields: list = [],
                   query: str = None,
                   environment: str = "production") -> list:

    start_time = datetime.now()
    msg_handler = messageHandler(logger=logger, level="DEBUG",
                                 labels={'function': 'getAllProducts',
                                         'endpoint': '/Product'})
    ## construct request
    ## construct request
    if environment == "production":
        request_url = f"{PRODUCTION_ADDRESS}/Product"
    elif environment == "development":
        request_url = f"{DEVELOPMENT_ADDRESS}/Product"

    page = 1
    base_params = {"resultsPerPage": page_results,
                   "sortBy": sorting,
                   "lang": language}

    if category_id:
        base_params.update({"categoryId": category_id})
    if brand_id:
        base_params.update({"brandId": brand_id})
    if query:
        base_params.update({"query": query})
    if optional_fields:
        base_params.update({"optionalFields": optional_fields})

    ## logging
    msg_handler.logStruct(topic=f"getAllProducts: Request: {base_params}, Start get all products,\n start time: {start_time}")

    next_page = True
    products = []
    try:
        while next_page:
            if len(products) < max_results:
                base_params.update({"page": page})

                ## logging
                msg_handler.logStruct(topic=f"getAllProducts: Request {request_url} with params: {base_params}")

                r = requests.get(request_url,
                                 headers={'Authorization': 'Bearer ' + os.environ["YOUR_API_TOKEN"]},
                                 params=base_params)

                if r.status_code == 200:
                    result = json.loads(r.text)
                    data = result.get('data')
                    if data.get('results'):
                        products = products + data['results']
                        page += 1
                    else:
                        msg_handler.logStruct(topic="getAllProducts: No new data so all products gathered",
                                       status_code=r.status_code,
                                       response_text=r.text)
                        break
                else:
                    msg_handler.logStruct(level="ERROR",
                                          topic="getAllProducts: Error in the get all function",
                                    status_code=r.status_code,
                                    response_text=r.text)
                    break
            else:
                msg_handler.logStruct(level="DEBUG",
                                      topic=f"getAllProducts: max results reached. max: {max_results}")
                break

    except Exception as e:
        msg_handler.logStruct(topic="getAllProducts: Error getting all products",
                              error_message=str(e))

    msg_handler.logStruct(topic=f"getAllProducts: Finish get all products. Length: {len(products)}.\n processing time: {datetime.now()-start_time}")

    # closing the connection
    r.close()

    return products

def getAllExternalProductIds(logger:object,
                             sourceId: int = None,
                             environment: str = "production",
                             connection: object = None) -> dict:

    start_time = datetime.now()
    msg_handler = messageHandler(logger=logger, level="DEBUG",
                                 labels={'function': 'getAllExternalProductIds',
                                         'endpoint': '/Product/GetAllExternalIDs'})
    ## construct request
    base_params = {}
    if environment == "production":
        request_url = f"{PRODUCTION_ADDRESS}/Product/GetAllExternalIDs"
    elif environment == "development":
        request_url = f"{DEVELOPMENT_ADDRESS}/Product/GetAllExternalIDs"

    if sourceId:
        base_params = {"sourceId": sourceId}

    ## logging
    msg_handler.logStruct(
        topic=f"getAllExternalProductIds: Request get all external product ids",
        data=base_params)

    ## request variables
    products = {}
    try:
        ## handle request through session or normal
        if connection:
            r = connection.get(url=request_url,
                            params=base_params,
                            headers={'Authorization': 'Bearer ' + os.environ["YOUR_API_TOKEN"]})
        else:
            r = requests.get(url=request_url,
                             params=base_params,
                             headers={'Authorization': 'Bearer ' + os.environ["YOUR_API_TOKEN"]})

        if r.status_code == 200:
            result = json.loads(r.text)
            data = result.get('data')
            if data:
                products = data
            else:
                msg_handler.logStruct(topic="getAllExternalProductIds: No data in request",
                                      status_code=r.status_code,
                                      response_text=r.text)
        else:
            msg_handler.logStruct(level="ERROR",
                                  topic="getAllExternalProductIds: Error in the get all function",
                                  status_code=r.status_code,
                                  response_text=r.text)

    except Exception as e:
        msg_handler.logStruct(topic="getAllExternalProductIds: Error getting all external product ids",
                              error_message=str(e))

    msg_handler.logStruct(
        topic=f"getAllExternalProductIds: Finish get all products external ids. Length: {len(products)}.\n processing time: {datetime.now() - start_time}")

    if connection == None:
        # closing the connection
        r.close()

    return products




