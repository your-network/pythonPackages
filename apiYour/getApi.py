import os
import json
from datetime import datetime
from apiYour.helpers import buildRequestParameters
from loggingYour.localLogging import LocalLogger

class Category:
    @staticmethod
    def get(categoryId: int,
            connection: object,
            lang: str = None,
            logger: LocalLogger = None,
            **kwargs):

        ## logging
        if logger and bool(os.getenv('DEBUG', 'False')):
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
                if logger and bool(os.getenv('DEBUG', 'False')):
                    log_message = {"topic": f"No data on category get",
                                   "function": "getCategory",
                                   "endpoint": "/Category/{categoryId}",
                                   "code": status_code,
                                   "response": resp_data,
                                   "categoryId": categoryId}
                    logger.createDebugLog(message=log_message)

        else:
            ## logging
            if logger and bool(os.getenv('DEBUG', 'False')):
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

        ## logging
        if logger and bool(os.getenv('DEBUG', 'False')):
            log_message = {"topic": f"Start get all categories",
                           "function": "getAllCategories",
                           "endpoint": "/Category/GetAll"}
            logger.createDebugLog(message=log_message,
                                  **base_params)

        next_page = True
        categories = []
        while next_page:
            base_params.update({"page": page})

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
                    break
            else:
                ## logging
                if logger and bool(os.getenv('DEBUG', 'False')):
                    log_message = {"topic": f"Error get all categories",
                                   "function": "getAllCategories",
                                   "code": response_code,
                                   "response": response_text,
                                   "endpoint": "/Category/GetAll"}
                    logger.createErrorLog(message=log_message,
                                          **base_params)
                break

        ## logging
        if logger and bool(os.getenv('DEBUG', 'False')):
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
        if logger and bool(os.getenv('DEBUG', 'False')):
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
                if logger and bool(os.getenv('DEBUG', 'False')):
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

        ## variables
        func_parameters = locals()
        base_params = buildRequestParameters(parameters=func_parameters)

        ## logging
        if logger and bool(os.getenv('DEBUG', 'False')):
            log_message = {"topic": f"Start get all attributes",
                           "function": "getAllAttributes",
                           "endpoint": "/Attribute"}
            logger.createDebugLog(message=log_message, **base_params)

        attributes = []
        while True:
            base_params.update({"page": page})

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
                    break
            else:
                ## logging
                if logger and bool(os.getenv('DEBUG', 'False')):
                    log_message = {"topic": f"status code not 200",
                                   "function": "getAllAttributes",
                                   "endpoint": "/Attribute",
                                   "code": response_code,
                                   "response": response_text}
                    logger.createErrorLog(message=log_message, **base_params)

                break

        ## logging
        if logger and bool(os.getenv('DEBUG', 'False')):
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
        if logger and bool(os.getenv('DEBUG', 'False')):
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
                if logger and bool(os.getenv('DEBUG', 'False')):
                    log_message = {"topic": f"Error no status code 200",
                                   "function": "getAttributeValueUnits",
                                   "endpoint": "/AttributeValueUnit",
                                   "code": response_code,
                                   "response": response_text}
                    logger.createErrorLog(message=log_message, **base_params)

                break

        ## logging
        if logger and bool(os.getenv('DEBUG', 'False')):
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

        ## logging
        if logger and bool(os.getenv('DEBUG', 'False')):
            log_message = {"topic": f"Start get all",
                           "function": "getAllBrands",
                           "endpoint": "/Brand"}
            logger.createDebugLog(message=log_message, **base_params)

        next_page = True
        page = 1
        brands = []
        while next_page:
            base_params.update({"page": page})

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
                    break

            else:
                ## logging
                if logger and bool(os.getenv('DEBUG', 'False')):
                    log_message = {"topic": f"Error get all",
                                   "function": "getAllBrands",
                                   "endpoint": "/Brand",
                                   "code": response_code,
                                   "response": response_text}
                    logger.createErrorLog(message=log_message, **base_params)
                break

        ## logging
        if logger and bool(os.getenv('DEBUG', 'False')):
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

        ## variables
        func_parameters = locals()
        base_params = buildRequestParameters(parameters=func_parameters)

        ## logging
        if logger and bool(os.getenv('DEBUG', 'False')):
            log_message = {"topic": f"Start get all",
                           "function": "getAllSeries",
                           "endpoint": "/Series"}
            logger.createDebugLog(message=log_message, **base_params)

        next_page = True
        series = []
        try:
            while next_page:
                base_params.update({"page": page})

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
                        break

                else:
                    ## logging
                    if logger and bool(os.getenv('DEBUG', 'False')):
                        log_message = {"topic": f"Error get all",
                                       "function": "getAllSeries",
                                       "endpoint": "/Series",
                                       "code": response_code,
                                       "response": response_text}
                        logger.createErrorLog(message=log_message, **base_params)
                    break

        except Exception as e:
            ## logging
            if logger and bool(os.getenv('DEBUG', 'False')):
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
               max_results: int = 100000000,
               page_results: int = 1000,
               page: int = None,
               category_id: int = None,
               brand_id: int = None,
               language: str = "en",
               sorting: str = "Popularity",
               optional_fields: list = [],
               query: str = None,
               **kwargs) -> list:

        ## variables
        func_parameters = locals()
        base_params = buildRequestParameters(parameters=func_parameters)

        ## logging
        if logger and bool(os.getenv('DEBUG', 'False')):
            log_message = {"topic": f"Error get all products",
                           "function": "getAllProducts",
                           "endpoint": "/Product"}
            logger.createDebugLog(message=log_message, **base_params)

        products = []
        try:
            while True:
                if len(products) < max_results:
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
                        if len(data.get('results', [])) > 0:
                            products = products + data['results']
                            page += 1
                            page_set_parameters = base_params.update({'page': page})
                            continue

                        else:
                            break
                    else:
                        ## logging
                        if logger and bool(os.getenv('DEBUG', 'False')):
                            log_message = {"topic": f"Error get all products",
                                           "function": "getAllProducts",
                                           "endpoint": "/Product",
                                           "code": response_code,
                                           "response": response_text}
                            logger.createDebugLog(message=log_message, **base_params)
                        break
                else:
                    ## logging
                    if logger and bool(os.getenv('DEBUG', 'False')):
                        log_message = {"topic": f"Max results reached",
                                       "function": "getAllProducts",
                                       "endpoint": "/Product",
                                       "maxResults": max_results}
                        logger.createDebugLog(message=log_message, **base_params)
                    break

        except Exception as e:
            ## logging
            if logger and bool(os.getenv('DEBUG', 'False')):
                log_message = {"topic": f"Error get all",
                               "function": "getAllProducts",
                               "endpoint": "/Product",
                               "error": str(e)}
                logger.createErrorLog(message=log_message, **base_params)

        return products

    @staticmethod
    def getAllExternalIds(connection: object,
                          logger: LocalLogger = None,
                          sourceId: int = None,
                          **kwargs) -> dict:

        ## variables
        func_parameters = locals()
        base_params = buildRequestParameters(parameters=func_parameters)

        ## logging
        if logger and bool(os.getenv('DEBUG', 'False')):
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
                if logger and bool(os.getenv('DEBUG', 'False')):
                    log_message = {"topic": f"Error get all",
                                   "function": "getAllExternalProductIds",
                                   "endpoint": "/Product/GetAllExternalIDs",
                                   "code": response_code,
                                   "response": response_text}
                    logger.createErrorLog(message=log_message, **base_params)

        except Exception as e:
            ## logging
            if logger and bool(os.getenv('DEBUG', 'False')):
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
        if logger and bool(os.getenv('DEBUG', 'False')):
            log_message = {"topic": f"Start get all",
                           "function": "getProduct",
                           "endpoint": "/Product/{productId}",
                           "requestParams": param_url}
            logger.createDebugLog(message=log_message)

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
            ## logging
            if logger and bool(os.getenv('DEBUG', 'False')):
                log_message = {"topic": f"Error get all",
                               "function": "getProduct",
                               "endpoint": "/Product/{productId}",
                               "requestParams": param_url,
                               "code": response_code,
                               "response": response_text}
                logger.createErrorLog(message=log_message)

        return {}

def getUserSearch(identifier: str,
                  identifierType: str,
                  connection: object,
                  logger: LocalLogger = None,
                  **kwargs) -> dict:

    ## logging
    if logger and bool(os.getenv('DEBUG', 'False')):
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
        if logger and bool(os.getenv('DEBUG', 'False')):
            log_message = {"topic": f"Error get",
                           "function": "getUserSearch",
                           "endpoint": "/User/Search",
                           "code": response_code,
                           "response": response_text}
            logger.createErrorLog(message=log_message)

    return {}
