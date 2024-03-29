import os
import json
from typing import List
from datetime import datetime
from apiYour.helpers import buildRequestParameters
from loggingYour.localLogging import LocalLogger
import urllib

class Category:
    @staticmethod
    def get(categoryId: int,
            connection: object,
            lang: str = None,
            logger: LocalLogger = None,
            **kwargs):

        ## logging
        if logger and os.environ.get('DEBUG') == 'DEBUG':
            log_message = {"topic": f"start get category",
                           "function": "getCategory",
                           "endpoint": "/Category/{categoryId}",
                           "categoryId": categoryId}
            logger.createDebugLog(message=log_message)

        ## variables
        func_parameters = locals()
        base_params = buildRequestParameters(parameters=func_parameters)

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
                ## logging
                if logger and os.environ.get('DEBUG') == 'DEBUG':
                    log_message = {"topic": f"No data on category get",
                                   "function": "getCategory",
                                   "endpoint": "/Category/{categoryId}",
                                   "code": status_code,
                                   "response": resp_data,
                                   "categoryId": categoryId}
                    logger.createDebugLog(message=log_message)

        else:
            ## logging
            if logger and os.environ.get('DEBUG') == 'DEBUG':
                log_message = {"topic": f"Error category get",
                               "function": "getCategory",
                               "endpoint": "/Category/{categoryId}",
                               "code": status_code,
                               "response": resp_data,
                               "categoryId": categoryId}
                logger.createErrorLog(message=log_message)

        return {}

    @staticmethod
    def getAll(connection: object,
               logger: LocalLogger = None,
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
               includeServiceCategories: bool = False,
               **kwargs):

        ## variables
        func_parameters = locals()
        base_params = buildRequestParameters(parameters=func_parameters)

        ## params
        param_url = f"?resultsPerPage={resultsPerPage}"
        if categoryId:
            param_url = param_url + f"&categoryId={categoryId}"
        if brandId:
            param_url = param_url + f"&brandId={brandId}"
        if withProductsOnly:
            param_url = param_url + f"&optionalFields=withProductsOnly"
        if withChildrenOnly:
            param_url = param_url + f"&optionalFields=withChildrenOnly"
        if withImagesOnly:
            param_url = param_url + f"&optionalFields=withImagesOnly"
        if includeServiceCategories:
            param_url = param_url + f"&includeServiceCategories=true"
        if lang:
            param_url = param_url + f"&lang={lang}"

        ## logging
        if logger and os.environ.get('DEBUG') == 'DEBUG':
            log_message = {"topic": f"Start get all categories",
                           "function": "getAllCategories",
                           "endpoint": "/Category/GetAll"}
            logger.createDebugLog(message=log_message,
                                  **base_params)

        categories = []
        while True:
            pare_url_params = param_url + f"&page={page}"

            ## process request from connection pool
            r = connection.request(method="GET",
                                   url=f"{os.environ['YOUR_API_URL']}/Category{pare_url_params}",
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
                    break
            else:
                ## logging
                if logger and os.environ.get('DEBUG') == 'DEBUG':
                    log_message = {"topic": f"Error get all categories",
                                   "function": "getAllCategories",
                                   "code": response_code,
                                   "response": response_text,
                                   "endpoint": "/Category/GetAll"}
                    logger.createErrorLog(message=log_message,
                                          **base_params)
                break

        ## logging
        if logger and os.environ.get('DEBUG') == 'DEBUG':
            log_message = {"topic": f"Error category get",
                           "function": "getCategory",
                           "endpoint": "/Category/{categoryId}",
                           "numberCategories": len(categories)}
            logger.createErrorLog(message=log_message)

        return categories

    @staticmethod
    def getChilds(connection: object,
                  categoryId: int,
                  logger: LocalLogger = None,
                  resultsPerPage: int = 1000,
                  page: int = 1,
                  lang: str = None,
                  sortBy: str = None,
                  includeServiceCategories: bool = False,
                  **kwargs) -> list:

        ## variables
        func_parameters = locals()
        base_params = buildRequestParameters(parameters=func_parameters)

        ## logging
        if logger and os.environ.get('DEBUG') == 'DEBUG':
            log_message = {"topic": f"Start get all category childs",
                           "function": "getCategoryChilds",
                           "endpoint": "/Category/{categoryId}/Categories",
                           "categoryId": categoryId}
            logger.createDebugLog(message=log_message, **base_params)

        category_childs = []
        while True:
            base_params.update({"page": page})

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
                    break
            else:
                ## logging
                if logger and os.environ.get('DEBUG') == 'DEBUG':
                    log_message = {"topic": f"Error in the get all function",
                                   "function": "getCategoryChilds",
                                   "endpoint": "/Category/{categoryId}/Categories",
                                   "code": response_code,
                                   "response": response_text,
                                   "categoryId": categoryId}
                    logger.createErrorLog(message=log_message)

        return category_childs

class Attributes:
    @staticmethod
    def getAll(connection: object,
               logger: LocalLogger = None,
               resultsPerPage: int = 1000,
               page: int = 1,
               lang: str = None,
               categoryId: int = None,
               **kwargs) -> list:

        ## params
        param_url = f"?resultsPerPage={resultsPerPage}"
        if categoryId:
            param_url = param_url + f"&categoryId={categoryId}"
        if lang:
            param_url = param_url + f"&lang={lang}"

        ## logging
        if logger and os.environ.get('DEBUG') == 'DEBUG':
            log_message = {"topic": f"Start get all attributes",
                           "function": "getAllAttributes",
                           "endpoint": "/Attribute"}
            logger.createDebugLog(message=log_message)

        attributes = []
        while True:
            pare_url_params = param_url + f"&page={page}"

            ## process request from connection pool
            r = connection.request(method="GET",
                                   url=f"{os.environ['YOUR_API_URL']}/Attribute{pare_url_params}",
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
                    break
            else:
                ## logging
                if logger and os.environ.get('DEBUG') == 'DEBUG':
                    log_message = {"topic": f"status code not 200",
                                   "function": "getAllAttributes",
                                   "endpoint": "/Attribute",
                                   "code": response_code,
                                   "response": response_text}
                    logger.createErrorLog(message=log_message, **base_params)

                break

        ## logging
        if logger and os.environ.get('DEBUG') == 'DEBUG':
            log_message = {"topic": f"Finish get all attributes",
                           "function": "getAllAttributes",
                           "endpoint": "/Attribute",
                           "numberAttributes": len(attributes)}
            logger.createErrorLog(message=log_message, **base_params)

        return attributes

    @staticmethod
    def getValueUnits(connection: object,
                      logger: LocalLogger = None,
                      resultsPerPage: int = 500,
                      page: int = 1,
                      lang: str = None,
                      **kwargs) -> list:


        ## variables
        func_parameters = locals()
        base_params = buildRequestParameters(parameters=func_parameters)

        ## logging
        if logger and os.environ.get('DEBUG') == 'DEBUG':
            log_message = {"topic": f"Start get all",
                           "function": "getAttributeValueUnits",
                           "endpoint": "/AttributeValueUnit"}
            logger.createDebugLog(message=log_message, **base_params)

        page = 1
        attributeUnits = []
        while True:
            base_params.update({"page": page})

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
                    break

            else:
                ## logging
                if logger and os.environ.get('DEBUG') == 'DEBUG':
                    log_message = {"topic": f"Error no status code 200",
                                   "function": "getAttributeValueUnits",
                                   "endpoint": "/AttributeValueUnit",
                                   "code": response_code,
                                   "response": response_text}
                    logger.createErrorLog(message=log_message, **base_params)

                break

        ## logging
        if logger and os.environ.get('DEBUG') == 'DEBUG':
            log_message = {"topic": f"Finish get all",
                           "function": "getAttributeValueUnits",
                           "endpoint": "/AttributeValueUnit",
                           "numberValueUnits": len(attributeUnits)}
            logger.createDebugLog(message=log_message, **base_params)

        return attributeUnits

class Brands:
    @staticmethod
    def getAll(connection: object,
               logger: LocalLogger = None,
               query: str = None,
               resultsPerPage: int = 1000,
               page: int = 1,
               categoryId: int = None,
               withImagesOnly: bool = False,
               withProductsOnly: bool = False,
               desc: bool = False,
               lang: str = None,
               sortBy: str = None,
               **kwargs) -> list:

        ## variables
        func_parameters = locals()
        base_params = buildRequestParameters(parameters=func_parameters)

        ## params
        param_url = f"?resultsPerPage={resultsPerPage}"
        if categoryId:
            param_url = param_url + f"&categoryId={categoryId}"
        if withProductsOnly:
            param_url = param_url + f"&optionalFields=withProductsOnly"

        ## logging
        if logger and os.environ.get('DEBUG') == 'DEBUG':
            log_message = {"topic": f"Start get all",
                           "function": "getAllBrands",
                           "endpoint": "/Brand"}
            logger.createDebugLog(message=log_message, **base_params)

        page = 1
        brands = []
        while True:
            page_param_url = param_url + f"&page={page}"

            ## process request from connection pool
            r = connection.request(method="GET",
                                   url=f"{os.environ['YOUR_API_URL']}/Brand{page_param_url}",
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
                    break

            else:
                ## logging
                if logger and os.environ.get('DEBUG') == 'DEBUG':
                    log_message = {"topic": f"Error get all",
                                   "function": "getAllBrands",
                                   "endpoint": "/Brand",
                                   "code": response_code,
                                   "response": response_text}
                    logger.createErrorLog(message=log_message, **base_params)
                break

        ## logging
        if logger and os.environ.get('DEBUG') == 'DEBUG':
            log_message = {"topic": f"Finish get all",
                           "function": "getAllBrands",
                           "endpoint": "/Brand",
                           "numberBrands": len(brands)}
            logger.createDebugLog(message=log_message, **base_params)

        return brands

class Series:
    @staticmethod
    def getAll(connection: object,
               logger: LocalLogger = None,
               resultsPerPage: int = 1000,
               page: int = 1,
               **kwargs) -> list:
        ## params
        param_url = f"?resultsPerPage={resultsPerPage}"

        ## logging
        if logger and os.environ.get('DEBUG') == 'DEBUG':
            log_message = {"topic": f"Start get all",
                           "function": "getAllSeries",
                           "endpoint": "/Series",
                           "params": param_url}
            logger.createDebugLog(message=log_message)
        print(f"-------- GET API YOUR ---------- \n"
              f"Start get all series \n"
              f"params: {param_url} \n"
              f"apiUrl: {os.environ['YOUR_API_URL']} \n"
              f"Full: {os.environ['YOUR_API_URL']}/Series{param_url} \n"
              f"-----------------------------------\n")

        next_page = True
        series = []
        try:
            while next_page:
                page_param_url = param_url + f"&page={page}"

                ## process request from connection pool
                r = connection.request(method="GET",
                                       url=f"{os.environ['YOUR_API_URL']}/Series{page_param_url}",
                                       headers={'Authorization': 'Bearer ' + os.environ["YOUR_API_TOKEN"],
                                                'Content-Type': 'application/json'})

                response_code = r.status
                response_text = r.data

                print(f"-------- GET API YOUR ---------- \n"
                      f"Call Made \n"
                      f"params: {page_param_url} \n"
                      f"Full: {os.environ['YOUR_API_URL']}/Series{page_param_url} \n"
                      f"ResponseCode: {response_code} \n"
                      f"ResponseData: {response_text} \n"
                      f"-----------------------------------\n")

                if response_code == 200:
                    result = json.loads(response_text.decode('utf-8'))
                    data = result.get('data')
                    if len(data) > 0:
                        series = series + data
                        page += 1
                        continue

                    else:
                        break

                else:
                    ## logging
                    if logger and os.environ.get('DEBUG') == 'DEBUG':
                        log_message = {"topic": f"Error get all",
                                       "function": "getAllSeries",
                                       "endpoint": "/Series",
                                       "code": response_code,
                                       "response": response_text}
                        logger.createErrorLog(message=log_message, **base_params)
                    break

        except Exception as e:
            ## logging
            if logger and os.environ.get('DEBUG') == 'DEBUG':
                log_message = {"topic": f"Error get all",
                               "function": "getAllSeries",
                               "endpoint": "/Series",
                               "error": str(e)}
                logger.createErrorLog(message=log_message, **base_params)

        return series

class Product:
    @staticmethod
    def getAll(connection: object,
               logger: LocalLogger = None,
               resultsPerPage: int = 1000,
               page: int = 0,
               categoryId: int = None,
               brandId: int = None,
               language: str = "en",
               sorting: str = "Popularity",
               optionalFields: list = [],
               query: str = None,
               **kwargs) -> list:

        ## variables
        func_parameters = locals()
        base_params = buildRequestParameters(parameters=func_parameters)
        url_params = urllib.parse.urlencode(base_params)
        if optionalFields:
            for field in optionalFields:
                url_params = url_params + f"&optionalFields={field}"

        ## logging
        if logger and os.environ.get('DEBUG') == 'DEBUG':
            log_message = {"topic": f"Start get all products",
                           "function": "getAllProducts",
                           "endpoint": "/Product"}
            logger.createDebugLog(message=log_message, **base_params)

        products = []
        page = 0
        try:
            while True:
                ## process request from connection pool
                r = connection.request(method="GET",
                                       url=f"{os.environ['YOUR_API_URL']}/Product",
                                       fields=base_params,
                                       headers={'Authorization': 'Bearer ' + os.environ["YOUR_API_TOKEN"],
                                                'Content-Type': 'application/json'})

                response_code = r.status
                response_text = r.data
                if response_code == 200:
                    result = json.loads(response_text.decode('utf-8'))
                    data = result.get('data')
                    if data.get('results'):
                        products = products + data['results']
                        page += 1
                        page_set_parameters = base_params.update({'page': page})
                        continue

                    else:
                        break

                else:
                    ## logging
                    if logger and os.environ.get('DEBUG') == 'DEBUG':
                        log_message = {"topic": f"Error get all products",
                                       "function": "getAllProducts",
                                       "endpoint": "/Product",
                                       "code": response_code,
                                       "response": str(response_text)}
                        logger.createDebugLog(message=log_message, **base_params)
                        print(log_message)
                    break

        except Exception as e:
            ## logging
            if logger and os.environ.get('DEBUG') == 'DEBUG':
                log_message = {"topic": f"Error get all",
                               "function": "getAllProducts",
                               "endpoint": "/Product",
                               "error": str(e)}
                logger.createErrorLog(message=log_message, **base_params)
                print(log_message)
        return products

    @staticmethod
    def getAttributes(connection: object,
                       logger: LocalLogger = None,
                       productId: int = None,
                       lang: str = "en",
                       attributeTranslations: bool = True,
                       privateAttributes: bool = False,
                       **kwargs) -> dict:

        # Request Url
        request_url = f"{os.environ['YOUR_API_URL']}/Product/{productId}/Attributes?lang={lang}"
        if privateAttributes:
            request_url = request_url + "&optionalFields=PrivateAttributes"
        if attributeTranslations:
            request_url = request_url + "&optionalFields=AttributeTranslations"

        ## logging
        if logger and os.environ.get('DEBUG') == 'DEBUG':
            log_message = {"topic": f"Error get all product attributes",
                           "function": "getProductAttributes",
                           "endpoint": "/Product/<productId>/Attributes"}
            logger.createDebugLog(message=log_message)

        ## request variables
        try:
            ## process request from connection pool
            r = connection.request(method="GET",
                                   url=request_url,
                                   headers={'Authorization': 'Bearer ' + os.environ["YOUR_API_TOKEN"],
                                            'Content-Type': 'application/json'})

            response_code = r.status
            response_text = r.data
            if response_code == 200:
                result = json.loads(response_text.decode('utf-8'))
                data = result.get('data')
                return data
            else:
                ## logging
                if logger and os.environ.get('DEBUG') == 'DEBUG':
                    log_message = {"topic": f"Error get all",
                                   "function": "getProductAttributes",
                                   "endpoint": "/Product/<productId>/Attributes",
                                   "code": response_code,
                                   "response": response_text}
                    logger.createErrorLog(message=log_message)

        except Exception as e:
            ## logging
            if logger and os.environ.get('DEBUG') == 'DEBUG':
                log_message = {"topic": f"Error get all",
                               "function": "getProductAttributes",
                               "endpoint": "/Product/<productId>/Attributes",
                               "error": str(e)}
                logger.createErrorLog(message=log_message)

        return {}

    @staticmethod
    def getImages(connection: object,
                  logger: LocalLogger = None,
                  productId: int = None,
                  lang: str = 'en',
                  optionalFields: List[str] = None,
                  **kwargs) -> list:

        ## variables
        func_parameters = locals()
        base_params = buildRequestParameters(parameters=func_parameters)
        url_params = urllib.parse.urlencode(base_params)
        if optionalFields:
            for field in optionalFields:
                url_params = url_params + f"&optionalFields={field}"

        ## logging
        if logger and os.environ.get('DEBUG') == 'DEBUG':
            log_message = {"topic": f"Error get all product images",
                           "function": "getProductImages",
                           "endpoint": "/Product/<productId>/Images"}
            logger.createDebugLog(message=log_message, **base_params)

        try:
            ## process request from connection pool
            r = connection.request(method="GET",
                                   url=f"{os.environ['YOUR_API_URL']}/Product/{productId}/Images?{url_params}",
                                   headers={'Authorization': 'Bearer ' + os.environ["YOUR_API_TOKEN"],
                                            'Content-Type': 'application/json'})

            response_code = r.status
            response_text = r.data
            if response_code == 200:
                result = json.loads(response_text.decode('utf-8'))
                data = result.get('data')
                return data

            else:
                ## logging
                if logger and os.environ.get('DEBUG') == 'DEBUG':
                    log_message = {"topic": f"Error get all",
                                   "function": "getProductImages",
                                   "endpoint": "/Product/<productId>/Images",
                                   "code": response_code,
                                   "response": response_text}
                    logger.createErrorLog(message=log_message, **base_params)

        except Exception as e:
            ## logging
            if logger and os.environ.get('DEBUG') == 'DEBUG':
                log_message = {"topic": f"Error get all",
                               "function": "getProductImages",
                               "endpoint": "/Product/<productId>/Images",
                               "error": str(e)}
                logger.createErrorLog(message=log_message, **base_params)

        return []

    @staticmethod
    def getMedia(connection: object,
                   logger: LocalLogger = None,
                   productId: int = None,
                   optionalFields: List[str] = None,
                   **kwargs) -> list:

        ## variables
        func_parameters = locals()
        base_params = buildRequestParameters(parameters=func_parameters)
        url_params = urllib.parse.urlencode(base_params)
        if optionalFields:
            for field in optionalFields:
                url_params = url_params + f"&optionalFields={field}"

        ## logging
        if logger and os.environ.get('DEBUG') == 'DEBUG':
            log_message = {"topic": f"Error get all product images",
                           "function": "getProductMedia",
                           "endpoint": "/Product/<productId>/Media"}
            logger.createDebugLog(message=log_message, **base_params)

        try:
            ## process request from connection pool
            r = connection.request(method="GET",
                                   url=f"{os.environ['YOUR_API_URL']}/Product/{productId}/Media?{url_params}",
                                   headers={'Authorization': 'Bearer ' + os.environ["YOUR_API_TOKEN"],
                                            'Content-Type': 'application/json'})

            response_code = r.status
            response_text = r.data
            if response_code == 200:
                result = json.loads(response_text.decode('utf-8'))
                data = result.get('data')
                return data
            else:
                ## logging
                if logger and os.environ.get('DEBUG') == 'DEBUG':
                    log_message = {"topic": f"Error get all",
                                   "function": "getProductMedia",
                                   "endpoint": "/Product/<productId>/Media",
                                   "code": response_code,
                                   "response": response_text}
                    logger.createErrorLog(message=log_message, **base_params)

        except Exception as e:
            ## logging
            if logger and os.environ.get('DEBUG') == 'DEBUG':
                log_message = {"topic": f"Error get all",
                               "function": "getProductMedia",
                               "endpoint": "/Product/<productId>/Media",
                               "error": str(e)}
                logger.createErrorLog(message=log_message, **base_params)

        return []

    @staticmethod
    def getReviews(connection: object,
                   logger: LocalLogger = None,
                   productId: int = None,
                   resultsPerPage: int = 50,
                   page: int = None,
                   lang: str = "en",
                   sortBy: str = "Popularity",
                   desc: bool = True,
                   optional_fields: List[str] = None,
                   query: str = None,
                   **kwargs) -> dict:

        ## variables
        func_parameters = locals()
        base_params = buildRequestParameters(parameters=func_parameters)
        url_params = urllib.parse.urlencode(base_params)
        if optional_fields:
            for field in optional_fields:
                url_params = url_params + f"&optionalFields={field}"

        ## logging
        if logger and os.environ.get('DEBUG') == 'DEBUG':
            log_message = {"topic": f"Error get all product reviews",
                           "function": "getProductReviews",
                           "endpoint": "/Product/<productId>/Reviews"}
            logger.createDebugLog(message=log_message, **base_params)

        try:
            ## process request from connection pool
            r = connection.request(method="GET",
                                   url=f"{os.environ['YOUR_API_URL']}/Product/{productId}/Reviews{url_params}",
                                   headers={'Authorization': 'Bearer ' + os.environ["YOUR_API_TOKEN"],
                                            'Content-Type': 'application/json'})

            response_code = r.status
            response_text = r.data
            if response_code == 200:
                result = json.loads(response_text.decode('utf-8'))
                data = result.get('data')
                return data
            else:
                ## logging
                if logger and os.environ.get('DEBUG') == 'DEBUG':
                    log_message = {"topic": f"Error get all",
                                   "function": "getProductReviews",
                                   "endpoint": "/Product/<productId>/Reviews",
                                   "code": response_code,
                                   "response": response_text}
                    logger.createErrorLog(message=log_message, **base_params)

        except Exception as e:
            ## logging
            if logger and os.environ.get('DEBUG') == 'DEBUG':
                log_message = {"topic": f"Error get all",
                               "function": "getProductReviews",
                               "endpoint": "/Product/<productId>/Reviews",
                               "error": str(e)}
                logger.createErrorLog(message=log_message, **base_params)

        return {}

    @staticmethod
    def getReasonsToBuy(connection: object,
                   logger: LocalLogger = None,
                   productId: int = None,
                   page: int = None,
                   lang: str = "en",
                   optional_fields: List[str] = None,
                   **kwargs) -> list:

        ## variables
        func_parameters = locals()
        base_params = buildRequestParameters(parameters=func_parameters)
        url_params = urllib.parse.urlencode(base_params)
        if optional_fields:
            for field in optional_fields:
                url_params = url_params + f"&optionalFields={field}"

        ## logging
        if logger and os.environ.get('DEBUG') == 'DEBUG':
            log_message = {"topic": f"Error get all product ReasonsToBuy",
                           "function": "getProductReasonsToBuy",
                           "endpoint": "/Product/<productId>/ReasonsToBuy"}
            logger.createDebugLog(message=log_message, **base_params)

        try:
            ## process request from connection pool
            r = connection.request(method="GET",
                                   url=f"{os.environ['YOUR_API_URL']}/Product/{productId}/ReasonsToBuy?{url_params}",
                                   headers={'Authorization': 'Bearer ' + os.environ["YOUR_API_TOKEN"],
                                            'Content-Type': 'application/json'})

            response_code = r.status
            response_text = r.data
            if response_code == 200:
                result = json.loads(response_text.decode('utf-8'))
                data = result.get('data')
                return data
            else:
                ## logging
                if logger and os.environ.get('DEBUG') == 'DEBUG':
                    log_message = {"topic": f"Error get all",
                                   "function": "getProductReasonsToBuy",
                                   "endpoint": "/Product/<productId>/ReasonsToBuy",
                                   "code": response_code,
                                   "response": response_text}
                    logger.createErrorLog(message=log_message, **base_params)

        except Exception as e:
            ## logging
            if logger and os.environ.get('DEBUG') == 'DEBUG':
                log_message = {"topic": f"Error get all",
                               "function": "getProductReasonsToBuy",
                               "endpoint": "/Product/<productId>/ReasonsToBuy",
                               "error": str(e)}
                logger.createErrorLog(message=log_message, **base_params)

        return []

    @staticmethod
    def getAllExternalIds(connection: object,
                          logger: LocalLogger = None,
                          sourceId: int = None,
                          **kwargs) -> dict:

        ## variables
        func_parameters = locals()
        base_params = buildRequestParameters(parameters=func_parameters)

        ## logging
        if logger and os.environ.get('DEBUG') == 'DEBUG':
            log_message = {"topic": f"Start get all",
                           "function": "getAllExternalProductIds",
                           "endpoint": "/Product/GetAllExternalIDs"}
            logger.createDebugLog(message=log_message, **base_params)

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
                    return products
            else:
                ## logging
                if logger and os.environ.get('DEBUG') == 'DEBUG':
                    log_message = {"topic": f"Error get all",
                                   "function": "getAllExternalProductIds",
                                   "endpoint": "/Product/GetAllExternalIDs",
                                   "code": response_code,
                                   "response": response_text}
                    logger.createErrorLog(message=log_message, **base_params)

        except Exception as e:
            ## logging
            if logger and os.environ.get('DEBUG') == 'DEBUG':
                log_message = {"topic": f"Error get all",
                               "function": "getAllExternalProductIds",
                               "endpoint": "/Product/GetAllExternalIDs",
                               "error": str(e)}
                logger.createErrorLog(message=log_message, **base_params)

        return products

    @staticmethod
    def get(productId: str,
            connection: object,
            logger: LocalLogger = None,
            attributes: bool = False,
            privateAttributes: bool = False,
            media: bool = False,
            parentCategories: bool = False,
            ReasonsToBuy: bool = False,
            extraResolutions: bool = True,
            mediaAttributes: bool = True,
            language: str = None,
            **kwargs) -> dict:

        ## params
        param_url = f"?optionalFields=Translations"
        if language:
            param_url = param_url + f"&Lang={language}"
        if attributes:
            param_url = param_url + f"&optionalFields=AttributeTranslations&optionalFields=Attributes"
        if privateAttributes:
            param_url = param_url + f"&optionalFields=PrivateAttributes"
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

        url_constructed = f"{os.environ['YOUR_API_URL']}/Product/{productId}{param_url}"

        ## logging
        if logger and os.environ.get('DEBUG') == 'DEBUG':
            log_message = {"topic": f"Start get all",
                           "function": "getProduct",
                           "endpoint": "/Product/{productId}",
                           "requestParams": param_url}
            logger.createDebugLog(message=log_message)

        ## process request from connection pool
        r = connection.request(method="GET",
                               url=url_constructed,
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
            ## logging
            if logger and os.environ.get('DEBUG') == 'DEBUG':
                log_message = {"topic": f"Error get all",
                               "function": "getProduct",
                               "endpoint": "/Product/{productId}",
                               "requestParams": param_url,
                               "code": response_code,
                               "response": response_text}
                logger.createErrorLog(message=log_message)

        return {}

    @staticmethod
    def exist(id: str,
            connection: object,
            logger: LocalLogger = None,
            idType: str = None,
            **kwargs) -> dict:

        ## logging
        if logger and os.environ.get('DEBUG') == 'DEBUG':
            log_message = {"topic": f"Start get all",
                           "function": "productExists",
                           "endpoint": "/Product/Exists",
                           "id": id,
                           "idType": idType}
            logger.createDebugLog(message=log_message)

        ## process request from connection pool
        r = connection.request(method="GET",
                               url=f"{os.environ['YOUR_API_URL']}/Product/Exists?id={id}&idType={idType}",
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
            ## logging
            if logger and os.environ.get('DEBUG') == 'DEBUG':
                log_message = {"topic": f"Error get all",
                               "function": "getProduct",
                               "endpoint": "/Product/{productId}",
                               "id": id,
                               "idType": idType,
                               "code": response_code,
                               "response": response_text}
                logger.createErrorLog(message=log_message)

        return {}

    def getQuestions(productId: str,
                     connection: object,
                     logger: LocalLogger = None,
                     language: str = None,
                     resultsPerPage: int = 10,
                     optional_fields: List[str] = None,
                     page: int = 1,
                     **kwargs) -> dict:
        ## logging
        if logger and os.environ.get('DEBUG') == 'DEBUG':
            log_message = {"topic": f"Start get all",
                           "function": "getProduct",
                           "endpoint": "/QnA/Question"}
            logger.createDebugLog(message=log_message)

        ## variables
        func_parameters = locals()
        base_params = buildRequestParameters(parameters=func_parameters)
        url_params = urllib.parse.urlencode(base_params)
        if optional_fields:
            for field in optional_fields:
                url_params = url_params + f"&optionalFields={field}"

        ## process request from connection pool
        r = connection.request(method="GET",
                               url=f"{os.environ['YOUR_API_URL']}/Product/{productId}/QnA?{url_params}",
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
            ## logging
            if logger and os.environ.get('DEBUG') == 'DEBUG':
                log_message = {"topic": f"Error get all",
                               "function": "getProduct",
                               "endpoint": "/QnA/Question",
                               "code": response_code,
                               "response": response_text}
                logger.createErrorLog(message=log_message)

        return {}


class Customer:
    @staticmethod
    def getUserSearch(identifier: str,
                      identifierType: str,
                      connection: object,
                      logger: LocalLogger = None,
                      **kwargs) -> dict:

        ## logging
        if logger and os.environ.get('DEBUG') == 'DEBUG':
            log_message = {"topic": f"Start get",
                           "function": "getUserSearch",
                           "endpoint": "/User/Search",
                           "identifier": identifier}
            logger.createErrorLog(message=log_message)

        ## process request from connection pool
        r = connection.request(method="GET",
                               url=f"{os.environ['YOUR_API_URL']}/User/Search",
                               fields={identifierType: identifier},
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
            ## logging
            if logger and os.environ.get('DEBUG') == 'DEBUG':
                log_message = {"topic": f"Error get",
                               "function": "getUserSearch",
                               "endpoint": "/User/Search",
                               "code": response_code,
                               "response": response_text}
                logger.createErrorLog(message=log_message)

        return {}

    @staticmethod
    def getOrganization(customerId: str,
                        connection: object,
                        logger: LocalLogger = None,
                        **kwargs) -> dict:

        ## logging
        if logger and os.environ.get('DEBUG') == 'DEBUG':
            log_message = {"topic": f"Start get",
                           "function": "getCustomerOrganization",
                           "endpoint": "/Organization/{customerId}"}
            logger.createErrorLog(message=log_message)

        ## process request from connection pool
        r = connection.request(method="GET",
                               url=f"{os.environ['YOUR_API_URL']}/Organization/{customerId}",
                               headers={'Authorization': 'Bearer ' + os.environ["YOUR_API_TOKEN"],
                                        'Content-Type': 'application/json'})

        response_code = r.status
        response_text = r.data
        if response_code == 200:
            result = json.loads(response_text.decode('utf-8'))
            return result.get('data')

        else:
            ## logging
            if logger and os.environ.get('DEBUG') == 'DEBUG':
                log_message = {"topic": f"Error get",
                               "function": "getCustomerOrganization",
                               "endpoint": "/Organization/{customerId}",
                               "code": response_code,
                               "response": response_text}
                logger.createErrorLog(message=log_message)

        return {}


class QnA:
    @staticmethod
    def getQuestions(productId: str,
            connection: object,
            logger: LocalLogger = None,
            query: str = None,
            language: str = None,
            resultsPerPage: int = 10,
            page: int = 1,
            withAnswersOnly: bool = True,
            askedByUserOnly: bool = False,
            answeredByUserOnly: bool = False,
            includePending: bool = False,
            includeApproved: bool = True,
            **kwargs) -> dict:

        ## logging
        if logger and os.environ.get('DEBUG') == 'DEBUG':
            log_message = {"topic": f"Start get all",
                           "function": "getProduct",
                           "endpoint": "/QnA/Question"}
            logger.createDebugLog(message=log_message)

        ## variables
        func_parameters = locals()
        base_params = buildRequestParameters(parameters=func_parameters)

        ## process request from connection pool
        r = connection.request(method="GET",
                               fields=base_params,
                               url=f"{os.environ['YOUR_API_URL']}/QnA/Question",
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
            ## logging
            if logger and os.environ.get('DEBUG') == 'DEBUG':
                log_message = {"topic": f"Error get all",
                               "function": "getProduct",
                               "endpoint": "/QnA/Question",
                               "code": response_code,
                               "response": response_text}
                logger.createErrorLog(message=log_message)

        return {}

    @staticmethod
    def getQuestionAnswers(questionId: int,
                           connection: object,
                           logger: LocalLogger = None,
                           resultsPerPage: int = 10,
                           page: int = 1,
                           answeredByUserOnly: bool = False,
                           **kwargs) -> dict:

        ## logging
        if logger and os.environ.get('DEBUG') == 'DEBUG':
            log_message = {"topic": f"Start get all",
                           "function": "getProduct",
                           "endpoint": "/QnA/Question/{questionId}/Answers"}
            logger.createDebugLog(message=log_message)

        ## variables
        func_parameters = locals()
        base_params = buildRequestParameters(parameters=func_parameters)

        ## process request from connection pool
        r = connection.request(method="GET",
                               fields=base_params,
                               url=f"{os.environ['YOUR_API_URL']}/QnA/Question/{questionId}/Answers",
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
            ## logging
            if logger and os.environ.get('DEBUG') == 'DEBUG':
                log_message = {"topic": f"Error get all",
                               "function": "getProduct",
                               "endpoint": "/QnA/Question/{questionId}/Answers",
                               "code": response_code,
                               "response": response_text}
                logger.createErrorLog(message=log_message)

        return {}

