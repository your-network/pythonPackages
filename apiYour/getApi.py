import os
import requests
import json
from datetime import datetime
from loggingYour.messageHandler import messageHandler
from apiYour.settingsApi import PRODUCTION_ADDRESS, DEVELOPMENT_ADDRESS

class Category:
    @staticmethod
    def get(logger: object,
            categoryId: int,
            connection: object,
            lang: str = None):

        ## logging
        if bool(os.environ['DEBUG']):
            msg_handler = messageHandler(logger=logger, level="DEBUG",
                                         labels={'function': 'getCategory',
                                                 'endpoint': '/Category/{categoryId'})
            msg_handler.logStruct(topic=f"getCategory: Start get category", data=categoryId)

        ## variables
        base_params = {}
        if lang:
            base_params.update({"lang": lang})

        ## process request from connection pool
        r = connection.request(method="GET",
                               url=f"{os.environ['YOUR_API_URL']}/Category/{categoryId}",
                               fields=base_params,
                               headers={'Authorization': 'Bearer ' + os.environ["YOUR_API_TOKEN"],
                                        'Content-Type': 'application/json'})
        status_code = r.status
        resp_data = r.data

        if status_code in [200, 400]:
            resp_body = json.loads(resp_data.decode('utf-8'))
            data = resp_body.get('data')

            if data:
                return data
            else:
                if bool(os.environ['DEBUG']):
                    msg_handler.logStruct(topic="getCategory: No data on category get",
                                          status_code=status_code,
                                          response_text=resp_data)

                return {}
        else:
            if bool(os.environ['DEBUG']):
                msg_handler.logStruct(level="ERROR",
                                      topic="getCategory: Error in the get category function",
                                      status_code=status_code,
                                      response_text=resp_data)

            return {}

    @staticmethod
    def getAll(connection: object,
               logger: object = None,
               query: str = None,
               resultsPerPage: int = 1000,
               page: int = 1,
               categoryId: int = None,
               brandId: int = None,
               withImagesOnly: bool = False,
               withChildrenOnly: bool = False,
               withProductsOnly: bool = False,
               lang: str = None,
               sortBy: str = None,
               includeServiceCategories: bool = False):

        start_time = datetime.now()
        ## logging
        if bool(os.environ['DEBUG']) and logger:
            msg_handler = messageHandler(logger=logger, level="DEBUG",
                                         labels={'function': 'getAllCategories',
                                                 'endpoint': '/Category/GetAll'})
            msg_handler.logStruct(topic=f"getAllCategories: Start get all categories.\n start time: {start_time}")

        base_params = {"resultsPerPage": resultsPerPage,
                       "withImagesOnly": withImagesOnly,
                       "withChildrenOnly": withChildrenOnly,
                       "withProductsOnly": withProductsOnly,
                       "includeServiceCategories": includeServiceCategories,
                       "page": page}

        if categoryId:
            base_params.update({"categoryId": categoryId})
        if brandId:
            base_params.update({"brandId": brandId})
        if query:
            base_params.update({"query": query})
        if sortBy:
            base_params.update({"sortBy": sortBy})
        if lang:
            base_params.update({"lang": lang})

        next_page = True
        categories = []
        while next_page:
            base_params.update({"page": page})

            ## logging
            if logger:
                msg_handler.logStruct(topic=f"getAllCategories: params: {base_params}")

            ## process request from connection pool
            r = connection.request(method="GET",
                                   url=f"{os.environ['YOUR_API_URL']}/Category/GetAll",
                                   fields=base_params,
                                   headers={'Authorization': 'Bearer ' + os.environ["YOUR_API_TOKEN"],
                                            'Content-Type': 'application/json'})

            response_code = r.status
            response_text = r.data
            if response_code == 200:
                result = json.loads(response_text.decode('utf-8'))
                data = result.get('data')
                if data.get('results'):
                    categories = categories + data['results']
                    page += 1
                else:
                    if bool(os.environ['DEBUG']) and logger:
                        msg_handler.logStruct(topic="getAllCategories: No new data so all categories gathered",
                                       status_code=response_code,
                                       response_text=response_text)
                    break
            else:
                if bool(os.environ['DEBUG']) and logger:
                    msg_handler.logStruct(level="ERROR",
                                          topic="getAllCategories: Error in the get all function",
                                          status_code=response_code,
                                          response_text=response_text)
                break

        if bool(os.environ['DEBUG']) and logger:
            msg_handler.logStruct(topic=f"getAllCategories: Finish get all categories. Length: {len(categories)}.\n processing time: {datetime.now()-start_time}")


        return categories

    @staticmethod
    def getChilds(connection: object,
                  logger: object,
                  categoryId: int,
                  resultsPerPage: int = 1000,
                  page: int = 1,
                  lang: str = None,
                  sortBy: str = None,
                  includeServiceCategories: bool = False) -> list:

        start_time = datetime.now()
        ## logging
        if bool(os.environ['DEBUG']):
            msg_handler = messageHandler(logger=logger, level="DEBUG",
                                         labels={'function': 'getCategoryChilds',
                                                 'endpoint': f"/Category/{categoryId}/Categories"})
            msg_handler.logStruct(topic=f"getCategoryChilds: Start get all category childs")

        ## params builder
        base_params = {"resultsPerPage": resultsPerPage,
                       "includeServiceCategories": includeServiceCategories,
                       "page": page}
        if sortBy:
            base_params.update({"sortBy": sortBy})
        if lang:
            base_params.update({"lang": lang})

        category_childs = []
        while True:
            base_params.update({"page": page})

            ## logging
            if bool(os.environ['DEBUG']):
                msg_handler.logStruct(topic=f"getCategoryChilds: params: {base_params}")

            ## process request from connection pool
            r = connection.request(method="GET",
                                   url=f"{os.environ['YOUR_API_URL']}/Category/{categoryId}/Categories",
                                   fields=base_params,
                                   headers={'Authorization': 'Bearer ' + os.environ["YOUR_API_TOKEN"],
                                            'Content-Type': 'application/json'})

            response_code = r.status
            response_text = r.data
            if response_code == 200:
                result = json.loads(response_text.decode('utf-8'))
                data = result.get('data')
                if data.get('results'):
                    category_childs = category_childs + data['results']
                    page += 1
                else:
                    if bool(os.environ['DEBUG']):
                        msg_handler.logStruct(topic="getCategoryChilds: No new data so all categories childs gathered",
                                              status_code=response_code,
                                              response_text=response_text)
                    break
            else:
                if bool(os.environ['DEBUG']):
                    msg_handler.logStruct(level="ERROR",
                                          topic="getCategoryChilds: Error in the get all function",
                                          status_code=response_code,
                                          response_text=response_text)
                break

        ## logging
        if bool(os.environ['DEBUG']):
            msg_handler.logStruct(topic=f"getAllCategories: Finish get all category childs. "
                                        f"Length: {len(category_childs)}.\n "
                                        f"processing time: {datetime.now() - start_time}")

        return category_childs

class Attributes:
    @staticmethod
    def getAll(connection: object,
               logger: object = None,
               resultsPerPage: int = 1000,
               page: int = 1,
               lang: str = None,
               categoryId: int = None) -> list:

        ## logging
        if bool(os.environ['DEBUG']) and logger:
            start_time = datetime.now()
            msg_handler = messageHandler(logger=logger, level="DEBUG",
                                         labels={'function': 'getAllAttributes',
                                                 'endpoint': '/Attribute'})
            msg_handler.logStruct(topic=f"getAllAttributes: Start get all attributes")

        ## construct request
        base_params = {"resultsPerPage": resultsPerPage,
                       "page": page}
        if categoryId:
            base_params.update({"categoryId": categoryId})
        if lang:
            base_params.update({"lang": lang})

        attributes = []
        while True:
            base_params.update({"page": page})

            ## logging
            if bool(os.environ['DEBUG']) and logger:
                msg_handler.logStruct(topic=f"getAllAttributes: params: {base_params}")

            ## process request from connection pool
            r = connection.request(method="GET",
                                   url=f"{os.environ['YOUR_API_URL']}/Attribute",
                                   fields=base_params,
                                   headers={'Authorization': 'Bearer ' + os.environ["YOUR_API_TOKEN"],
                                            'Content-Type': 'application/json'})

            response_code = r.status
            response_text = r.data
            if response_code == 200:
                result = json.loads(response_text.decode('utf-8'))
                data = result['data'].get('results', [])
                if len(data) > 0:
                    attributes = attributes + data
                    page += 1
                else:
                    ## logging
                    if bool(os.environ['DEBUG']) and logger:
                        msg_handler.logStruct(
                                            topic="getAllAttributes: No new data so all attributes gathered",
                                            status_code=response_code,
                                            response_text=response_text,
                                            level="DEBUG")
                    break
            else:
                ## logging
                if bool(os.environ['DEBUG']) and logger:
                    msg_handler.logStruct(
                        level="ERROR",
                        topic="getAllAttributes: status code not 200",
                        status_code=response_code,
                        response_text=response_text)
                break

        ## logging
        if bool(os.environ['DEBUG']) and logger:
            msg_handler.logStruct(topic=f"getAllAttributes: Finish get all attributes. Length: {len(attributes)}."
                                        f"Processing time: {datetime.now()-start_time}")

        return attributes

    @staticmethod
    def getValueUnits(connection: object,
                      logger: object = None,
                      resultsPerPage: int = 500,
                      page: int = 1,
                      lang: str = None) -> list:

        start_time = datetime.now()
        ## logging
        if bool(os.environ['DEBUG']) and logger:
            msg_handler = messageHandler(logger=logger, level="DEBUG",
                                         labels={'function': 'getAttributeValueUnits',
                                                 'endpoint': '/AttributeValueUnit'})
            msg_handler.logStruct(topic=f"getAttributeValueUnits: Start get all,\n start time: {start_time}")

        ## construct request
        base_params = {"resultsPerPage": resultsPerPage,
                       "page": page}
        if lang:
            base_params.update({"lang": lang})

        page = 1
        attributeUnits = []
        while True:
            base_params.update({"page": page})

            ## logging
            if bool(os.environ['DEBUG']) and logger:
                msg_handler.logStruct(topic=f"getAttributeValueUnits: params: {base_params}")

            ## process request from connection pool
            r = connection.request(method="GET",
                                   url=f"{os.environ['YOUR_API_URL']}/AttributeValueUnit",
                                   fields=base_params,
                                   headers={'Authorization': 'Bearer ' + os.environ["YOUR_API_TOKEN"],
                                            'Content-Type': 'application/json'})

            response_code = r.status
            response_text = r.data
            if response_code == 200:
                result = json.loads(response_text.decode('utf-8'))
                ## process data
                data = result.get('data')
                if data and data.get('results'):
                    attributeUnits = attributeUnits + data['results']
                    page += 1
                else:
                    if bool(os.environ['DEBUG']) and logger:
                        msg_handler.logStruct(topic="getAttributeValueUnits: No new data so all gathered",
                                              status_code=response_code,
                                              response_text=response_text)
                    break

            else:
                ## process if error was in call
                if bool(os.environ['DEBUG']) and logger:
                    msg_handler.logStruct(level="ERROR",
                                          topic="getAttributeValueUnits: status code not 200",
                                          status_code=response_code,
                                          response_text=response_text)
                break

        ## logging
        if bool(os.environ['DEBUG']) and logger:
            msg_handler.logStruct(topic=f"getAttributeValueUnits: Finish get all. Length: {len(attributeUnits)}")

        return attributeUnits

    @staticmethod
    def getAllTypeUnit(logger: object,
                        environment: str = "production") -> list:
        start_time = datetime.now()
        msg_handler = messageHandler(logger=logger, level="DEBUG",
                                     labels={'function': 'getAllAttributeTypeUnit',
                                             'endpoint': '/AttributeTypeUnit'})

        ## logging
        msg_handler.logStruct(
            topic=f"getAllAttributeTypeUnit: Start get all attribute type units,\n start time: {start_time}")

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
                    msg_handler.logStruct(
                        topic="getAllAttributeTypeUnit: No new data so all attribute type units gathered",
                        status_code=r.status_code,
                        response_text=r.text)
                    break

            else:
                msg_handler.logStruct(level="ERROR",
                                      topic="getAllAttributeTypeUnit: status code not 200",
                                      status_code=r.status_code,
                                      response_text=r.text)
                break

        msg_handler.logStruct(
            topic=f"getAllAttributeTypeUnit: Finish get all attribute type units. Length: {len(attributeTypeUnits)}.\n Processing time: {datetime.now() - start_time}")

        return attributeTypeUnits

    @staticmethod
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

        return attributeTypes

class Brands:
    @staticmethod
    def getAll(connection: object,
               logger: object = None,
               query: str = None,
               resultsPerPage: int = 1000,
               page: int = 1,
               categoryId: int = None,
               withImagesOnly: bool = False,
               withProductsOnly: bool = False,
               desc: bool = False,
               lang: str = None,
               sortBy: str = None) -> list:

        start_time = datetime.now()
        msg_handler = messageHandler(logger=logger, level="DEBUG",
                                     labels={'function': 'getAllBrands',
                                             'endpoint': '/Brand'})

        ## logging
        if bool(os.environ['DEBUG']) and logger:
            msg_handler = messageHandler(logger=logger, level="DEBUG",
                                         labels={'function': 'getAllBrands',
                                                 'endpoint': '/Brand'})
            msg_handler.logStruct(topic=f"getAllBrands: Start get all brands,\n start time: {start_time}")

        ## request builder
        base_params = {"resultsPerPage": resultsPerPage,
                       "withImagesOnly": withImagesOnly,
                       "withProductsOnly": withProductsOnly,
                       "desc": desc,
                       "page": page}
        if query:
            base_params.update({"query": query})
        if sortBy:
            base_params.update({"sortBy": sortBy})
        if categoryId:
            base_params.update({"categoryId": categoryId})
        if lang:
            base_params.update({"lang": lang})

        next_page = True
        page = 1
        brands = []
        while next_page:
            base_params.update({"page": page})

            ## logging
            if bool(os.environ['DEBUG']) and logger:
                msg_handler.logStruct(topic=f"getAllBrands: params: {base_params}")

            ## process request from connection pool
            r = connection.request(method="GET",
                                   url=f"{os.environ['YOUR_API_URL']}/Brand",
                                   fields=base_params,
                                   headers={'Authorization': 'Bearer ' + os.environ["YOUR_API_TOKEN"],
                                            'Content-Type': 'application/json'})

            response_code = r.status
            response_text = r.data
            if response_code == 200:
                result = json.loads(response_text.decode('utf-8'))
                data = result.get('data')
                if data.get('results'):
                    brands = brands + data['results']
                    page += 1
                else:
                    if bool(os.environ['DEBUG']) and logger:
                        msg_handler.logStruct(topic="getAllBrands: No new data so all brands gathered",
                                               status_code=response_code,
                                               response_text=response_text)
                    break

            else:
                ## process if error was in call
                if bool(os.environ['DEBUG']) and logger:
                    msg_handler.logStruct(level="ERROR",
                                   topic="getAllBrands: status code not 200",
                                   status_code=response_code,
                                   response_text=response_text)
                break

        ## logging
        if bool(os.environ['DEBUG']) and logger:
            msg_handler.logStruct(topic=f"getAllBrands: Finish get all brands. Length: {len(brands)}")

        return brands

class Series:
    @staticmethod
    def getAll(connection: object,
               logger: object = None,
               resultsPerPage: int = 1000,
               page: int = 1) -> list:

        ## logging
        if bool(os.environ['DEBUG']) and logger:
            start_time = datetime.now()
            msg_handler = messageHandler(logger=logger, level="DEBUG",
                                         labels={'function': 'getAllSeries',
                                                 'endpoint': '/Series'})
            msg_handler.logStruct(topic=f"getAllSeries: Start get all series,\n start time: {start_time}")

        ## construct request
        base_params = {"resultsPerPage": resultsPerPage}

        next_page = True
        series = []
        try:
            while next_page:
                base_params.update({"page": page})

                ## logging
                if bool(os.environ['DEBUG']) and logger:
                    msg_handler.logStruct(topic=f"getAllSeries:params: {base_params}")

                ## process request from connection pool
                r = connection.request(method="GET",
                                       url=f"{os.environ['YOUR_API_URL']}/Series",
                                       fields=base_params,
                                       headers={'Authorization': 'Bearer ' + os.environ["YOUR_API_TOKEN"],
                                                'Content-Type': 'application/json'})

                response_code = r.status
                response_text = r.data
                if response_code == 200:
                    result = json.loads(response_text.decode('utf-8'))
                    data = result.get('data')
                    if len(data) > 0:
                        series = series + data
                        page += 1
                        continue

                    else:
                        ## logging
                        if bool(os.environ['DEBUG']) and logger:
                            msg_handler.logStruct(
                                topic="getAllSeries: No new data so all series gathered",
                                status_code=response_code,
                                response_text=response_text,
                                level="DEBUG")
                        break

                else:
                    if bool(os.environ['DEBUG']) and logger:
                        msg_handler.logStruct(level="ERROR",
                                              topic="getAllSeries: Error in the get all function",
                                              status_code=r.status_code,
                                              response_text=r.text)
                    break

        except Exception as e:
            if bool(os.environ['DEBUG']) and logger:
                msg_handler.logStruct(topic="getAllSeries: Error getting all series",
                                      error_message=str(e))
            else:
                print(f"getAllSeries: Error getting all series. Error: {str(e)}")

        if bool(os.environ['DEBUG']) and logger:
            msg_handler.logStruct(
                topic=f"getAllSeries: Finish get all series. Length: {len(series)}.\n processing time: {datetime.now() - start_time}")

        return series

def getImageByStatus(connection: object,
                     logger: object = None,
                     status: str = "Broken",
                     resultsPerPage: int = 1000,
                     maxResults: int = None,
                     page: int = 1,
                     type: str = "product",
                     environment: str = "production"):

    start_time = datetime.now()
    ## logging
    if logger:
        msg_handler = messageHandler(logger=logger, level="DEBUG",
                                     labels={'function': 'getImageByStatus',
                                             'endpoint': '/Internal/GetImagesByStatus'})
        msg_handler.logStruct(topic=f"getImageByStatus: Start get all {status} images for type {type}\n")

    ## construct request
    if environment == "production":
        request_url = f"{PRODUCTION_ADDRESS}/Internal/GetImagesByStatus"
    elif environment == "development":
        request_url = f"{DEVELOPMENT_ADDRESS}/Internal/GetImagesByStatus"

    base_params = {"resultsPerPage": resultsPerPage,
                   "status": status,
                   "page": page}

    next_page = True
    broken_images = []
    while next_page:
        base_params.update({"page": page})

        ## logging
        if logger:
            msg_handler.logStruct(topic=f"getImageByStatus: Request {request_url} with params: {base_params}")

        ## process request from connection pool
        r = connection.request(method="GET",
                               url=request_url,
                               fields=base_params,
                               headers={'Authorization': 'Bearer ' + os.environ["YOUR_API_TOKEN"],
                                        'Content-Type': 'application/json'})

        response_code = r.status
        response_text = r.data
        if response_code == 200:
            result = json.loads(response_text.decode('utf-8'))
            data = result.get('data')
            if data.get('results'):
                for image_row in data['results']:
                    ## product type
                    if type == "product" and image_row.get('productId'):
                        broken_images.append(image_row)

                    ## brand type
                    elif type == "brand" and image_row.get('brandId'):
                        broken_images.append(image_row)

                    ## category type
                    elif type == "category" and image_row.get('categoryId'):
                        broken_images.append(image_row)

                if len(broken_images) >= maxResults:
                    break

                page += 1

            else:
                if logger:
                    msg_handler.logStruct(topic=f"getImageByStatus: No new data so all {type} {status} images gathered",
                                          status_code=response_code,
                                          response_text=response_text)
                break

        else:
            if logger:
                msg_handler.logStruct(level="ERROR",
                                      topic="getImageByStatus: Error in the get all function",
                                      status_code=response_code,
                                      response_text=response_text)
            break

    if logger:
        msg_handler.logStruct(topic=f"getImageByStatus: Finish get all images. Length: {len(broken_images)}.\n processing time: {datetime.now()-start_time}")

    return broken_images, page

class Product:
    @staticmethod
    def getAll(connection: object,
               logger: object = None,
               max_results: int = 100000000,
               page_results: int = 1000,
               page: int = None,
               category_id: int = None,
               brand_id: int = None,
               language: str = "en",
               sorting: str = "Popularity",
               optional_fields: list = [],
               query: str = None) -> list:

        ## logging
        if bool(os.environ['DEBUG']) and logger:
            start_time = datetime.now()
            msg_handler = messageHandler(logger=logger, level="DEBUG",
                                         labels={'function': 'getAllProducts',
                                                 'endpoint': '/Product'})

        ## building parameters
        parameters = f"?resultsPerPage={page_results}&sortBy={sorting}&lang={language}"
        if category_id:
            parameters = parameters + f"&categoryId={category_id}"
        if brand_id:
            parameters = parameters + f"&brandId={brand_id}"
        if query:
            parameters = parameters + f"&query={query}"
        if optional_fields:
            for optional_field in optional_fields:
                parameters = parameters + f"&optionalFields={optional_field}"
        ## set page
        if page:
            pagination = False
        else:
            pagination = True
            page = 1
        page_set_parameters = parameters + f"&page={page}"

        ## logging
        msg_handler.logStruct(topic=f"getAllProducts: Request parameters: {parameters}, Start get all products")

        products = []
        try:
            while True:
                if len(products) < max_results:
                    ## logging
                    msg_handler.logStruct(topic=f"getAllProducts: params: {parameters}")

                    ## process request from connection pool
                    r = connection.request(method="GET",
                                           url=f"{os.environ['YOUR_API_URL']}/Product{page_set_parameters}",
                                           headers={'Authorization': 'Bearer ' + os.environ["YOUR_API_TOKEN"],
                                                    'Content-Type': 'application/json'})

                    response_code = r.status
                    response_text = r.data
                    if response_code == 200:
                        result = json.loads(response_text.decode('utf-8'))
                        data = result.get('data')
                        if len(data.get('results', [])) > 0:
                            products = products + data['results']

                            if pagination:
                                page += 1
                                page_set_parameters = parameters + f"&page={page}"
                                continue
                            else:
                                break

                        else:
                            if bool(os.environ['DEBUG']) and logger:
                                msg_handler.logStruct(topic="getAllProducts: No new data so all products gathered",
                                                      status_code=response_code,
                                                      response_text=response_text)
                            break
                    else:
                        if bool(os.environ['DEBUG']) and logger:
                            msg_handler.logStruct(level="ERROR",
                                                  topic="getAllProducts: Error in the get all function",
                                                  status_code=response_code,
                                                  response_text=response_text)
                        break
                else:
                    if bool(os.environ['DEBUG']) and logger:
                        msg_handler.logStruct(level="DEBUG",
                                              topic=f"getAllProducts: max results reached. max: {max_results}")
                    break

        except Exception as e:
            if bool(os.environ['DEBUG']) and logger:
                msg_handler.logStruct(topic="getAllProducts: Error getting all products",
                                      error_message=str(e))

        if bool(os.environ['DEBUG']) and logger:
            msg_handler.logStruct(
                topic=f"getAllProducts: Finish get all products. Length: {len(products)}.\n "
                      f"processing time: {datetime.now() - start_time}")

        return products

    @staticmethod
    def getAllExternalIds(connection: object,
                          logger: object = None,
                          sourceId: int = None) -> dict:
        ## construct request
        if sourceId:
            base_params = {"sourceId": sourceId}

        if bool(os.environ['DEBUG']) and logger:
            start_time = datetime.now()
            msg_handler = messageHandler(logger=logger, level="DEBUG",
                                         labels={'function': 'getAllExternalProductIds',
                                                 'endpoint': '/Product/GetAllExternalIDs'})
            msg_handler.logStruct(
                topic=f"getAllExternalProductIds: Request get all external product ids",
                data=base_params)

        ## request variables
        products = {}
        try:
            ## process request from connection pool
            r = connection.request(method="GET",
                                   url=f"{os.environ['YOUR_API_URL']}/Product/GetAllExternalIDs",
                                   fields=base_params,
                                   headers={'Authorization': 'Bearer ' + os.environ["YOUR_API_TOKEN"],
                                            'Content-Type': 'application/json'})

            response_code = r.status
            response_text = r.data
            if response_code == 200:
                result = json.loads(response_text.decode('utf-8'))
                data = result.get('data')
                if data:
                    products = data
                else:
                    if bool(os.environ['DEBUG']) and logger:
                        msg_handler.logStruct(topic="getAllExternalProductIds: No data in request",
                                              status_code=response_code,
                                              response_text=response_text)
            else:
                if bool(os.environ['DEBUG']) and logger:
                    msg_handler.logStruct(level="ERROR",
                                          topic="getAllExternalProductIds: Error in the get all function",
                                          status_code=response_code,
                                          response_text=response_text)

        except Exception as e:
            if bool(os.environ['DEBUG']) and logger:
                msg_handler.logStruct(topic="getAllExternalProductIds: Error getting all external product ids",
                                      error_message=str(e))

        if bool(os.environ['DEBUG']) and logger:
            msg_handler.logStruct(
                topic=f"getAllExternalProductIds: Finish get all products external ids. Length: {len(products)}.processing time: {datetime.now() - start_time}")

        return products

    @staticmethod
    def get(productId: str,
            connection: object,
            logger: object = None,
            attributes: bool = False,
            media: bool = False,
            parentCategories: bool = False,
            ReasonsToBuy: bool = False,
            extraResolutions: bool = True,
            mediaAttributes: bool = True,
            language: str = None) -> dict:

        ## params
        param_url = f"?optionalFields=Translations"
        if language:
            param_url = param_url + f"Lang={language}"
        if attributes:
            param_url = param_url + f"&optionalFields=AttributeTranslations&optionalFields=Attributes"
        if media:
            param_url = param_url + f"&optionalFields=Media"
        if parentCategories:
            param_url = param_url + f"&optionalFields=ParentCategories"
        if ReasonsToBuy:
            param_url = param_url + f"&optionalFields=ReasonsToBuy"
        if extraResolutions:
            param_url = param_url + f"&optionalFields=extraResolutions"
        if mediaAttributes:
            param_url = param_url + f"&optionalFields=MediaAttributeValues"

        ## logging
        if bool(os.environ['DEBUG']) and logger:
            msg_handler = messageHandler(logger=logger, level="DEBUG",
                                         labels={'function': 'getProduct',
                                                 'endpoint': '/Category/GetAll'})
            msg_handler.logStruct(topic=f"getProduct: Start get productId {productId}, params: {param_url}")

        ## process request from connection pool
        r = connection.request(method="GET",
                               url=f"{os.environ['YOUR_API_URL']}/Product/{productId}{param_url}",
                               headers={'Authorization': 'Bearer ' + os.environ["YOUR_API_TOKEN"],
                                        'Content-Type': 'application/json'})

        response_code = r.status
        response_text = r.data
        if response_code == 200:
            result = json.loads(response_text.decode('utf-8'))
            data = result.get('data')
            if data:
                return data

        else:
            if bool(os.environ['DEBUG']) and logger:
                msg_handler.logStruct(level="ERROR",
                                      topic="getProduct: Error in the get all function",
                                      status_code=response_code,
                                      response_text=response_text)

        return {}


def getUserSearch(identifier: str,
                  identifierType: str,
                  connection: object,
            logger: object = None,
            environment: str = "production") -> dict:

    ## logging
    if logger:
        msg_handler = messageHandler(logger=logger, level="DEBUG",
                                     labels={'function': 'getUserSearch',
                                             'endpoint': '/User/Search'})
        msg_handler.logStruct(topic=f"getUserSearch: Start get user {identifier}")

    ## construct request
    if environment == "production":
        request_url = f"{PRODUCTION_ADDRESS}/User/Search"
    elif environment == "development":
        request_url = f"{DEVELOPMENT_ADDRESS}/User/Search"

    ## logging
    if logger:
        msg_handler.logStruct(topic=f"getUserSearch: Request {request_url}")

    ## process request from connection pool
    r = connection.request(method="GET",
                           url=request_url,
                           fields= {identifierType: identifier},
                           headers={'Authorization': 'Bearer ' + os.environ["YOUR_API_TOKEN"],
                                    'Content-Type': 'application/json'})

    response_code = r.status
    response_text = r.data
    if response_code == 200:
        result = json.loads(response_text.decode('utf-8'))
        data = result.get('data')
        if data:
            return data

    else:
        if logger:
            msg_handler.logStruct(level="ERROR",
                                  topic="getUserSearch: Error in the get function",
                                  status_code=response_code,
                                  response_text=response_text)

    return {}
