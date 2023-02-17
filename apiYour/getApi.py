import os
import requests
import json
from datetime import datetime
from loggingYour.messageHandler import messageHandler
from apiYour.settingsApi import PRODUCTION_ADDRESS, DEVELOPMENT_ADDRESS
from apiYour.helpers import buildRequestParameters

class Category:
    @staticmethod
    def get(logger: object,
            categoryId: int,
            connection: object,
            lang: str = None,
            **kwargs):

        ## logging
        if bool(os.getenv('DEBUG','False')):
            msg_handler = messageHandler(logger=logger, level="DEBUG",
                                         labels={'function': 'getCategory',
                                                 'endpoint': '/Category/{categoryId'})
            msg_handler.logStruct(topic=f"getCategory: Start get category", data=categoryId)

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
                if bool(os.getenv('DEBUG','False')):
                    msg_handler.logStruct(topic="getCategory: No data on category get",
                                          status_code=status_code,
                                          response_text=resp_data)

                return {}
        else:
            if bool(os.getenv('DEBUG','False')):
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
               includeServiceCategories: bool = False,
               **kwargs):

        ## logging
        if bool(os.getenv('DEBUG','False')) and logger:
            msg_handler = messageHandler(logger=logger, level="DEBUG",
                                         labels={'function': 'getAllCategories',
                                                 'endpoint': '/Category/GetAll'})
            msg_handler.logStruct(topic=f"getAllCategories: Start get all categories.")

        ## variables
        func_parameters = locals()
        base_params = buildRequestParameters(parameters=func_parameters)

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
                    if bool(os.getenv('DEBUG','False')) and logger:
                        msg_handler.logStruct(topic="getAllCategories: No new data so all categories gathered",
                                       status_code=response_code,
                                       response_text=response_text)
                    break
            else:
                if bool(os.getenv('DEBUG','False')) and logger:
                    msg_handler.logStruct(level="ERROR",
                                          topic="getAllCategories: Error in the get all function",
                                          status_code=response_code,
                                          response_text=response_text)
                break

        if bool(os.getenv('DEBUG','False')) and logger:
            msg_handler.logStruct(topic=f"getAllCategories: Finish get all categories. Length: {len(categories)}.")


        return categories

    @staticmethod
    def getChilds(connection: object,
                  logger: object,
                  categoryId: int,
                  resultsPerPage: int = 1000,
                  page: int = 1,
                  lang: str = None,
                  sortBy: str = None,
                  includeServiceCategories: bool = False,
                  **kwargs) -> list:

        start_time = datetime.now()
        ## logging
        if bool(os.getenv('DEBUG','False')):
            msg_handler = messageHandler(logger=logger, level="DEBUG",
                                         labels={'function': 'getCategoryChilds',
                                                 'endpoint': f"/Category/{categoryId}/Categories"})
            msg_handler.logStruct(topic=f"getCategoryChilds: Start get all category childs")

        ## variables
        func_parameters = locals()
        base_params = buildRequestParameters(parameters=func_parameters)

        category_childs = []
        while True:
            base_params.update({"page": page})

            ## logging
            if bool(os.getenv('DEBUG','False')):
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
                    if bool(os.getenv('DEBUG','False')):
                        msg_handler.logStruct(topic="getCategoryChilds: No new data so all categories childs gathered",
                                              status_code=response_code,
                                              response_text=response_text)
                    break
            else:
                if bool(os.getenv('DEBUG','False')):
                    msg_handler.logStruct(level="ERROR",
                                          topic="getCategoryChilds: Error in the get all function",
                                          status_code=response_code,
                                          response_text=response_text)
                break

        ## logging
        if bool(os.getenv('DEBUG','False')):
            msg_handler.logStruct(topic=f"getAllCategories: Finish get all category childs. "
                                        f"Length: {len(category_childs)}.")

        return category_childs

class Attributes:
    @staticmethod
    def getAll(connection: object,
               logger: object = None,
               resultsPerPage: int = 1000,
               page: int = 1,
               lang: str = None,
               categoryId: int = None,
               **kwargs) -> list:

        ## logging
        if bool(os.getenv('DEBUG','False')) and logger:
            msg_handler = messageHandler(logger=logger, level="DEBUG",
                                         labels={'function': 'getAllAttributes',
                                                 'endpoint': '/Attribute'})
            msg_handler.logStruct(topic=f"getAllAttributes: Start get all attributes")

        ## variables
        func_parameters = locals()
        base_params = buildRequestParameters(parameters=func_parameters)

        attributes = []
        while True:
            base_params.update({"page": page})

            ## logging
            if bool(os.getenv('DEBUG','False')) and logger:
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
                    if bool(os.getenv('DEBUG','False')) and logger:
                        msg_handler.logStruct(
                                            topic="getAllAttributes: No new data so all attributes gathered",
                                            status_code=response_code,
                                            response_text=response_text,
                                            level="DEBUG")
                    break
            else:
                ## logging
                if bool(os.getenv('DEBUG','False')) and logger:
                    msg_handler.logStruct(
                        level="ERROR",
                        topic="getAllAttributes: status code not 200",
                        status_code=response_code,
                        response_text=response_text)
                break

        ## logging
        if bool(os.getenv('DEBUG','False')) and logger:
            msg_handler.logStruct(topic=f"getAllAttributes: Finish get all attributes. Length: {len(attributes)}.")

        return attributes

    @staticmethod
    def getValueUnits(connection: object,
                      logger: object = None,
                      resultsPerPage: int = 500,
                      page: int = 1,
                      lang: str = None,
                      **kwargs) -> list:

        ## logging
        if bool(os.getenv('DEBUG','False')) and logger:
            msg_handler = messageHandler(logger=logger, level="DEBUG",
                                         labels={'function': 'getAttributeValueUnits',
                                                 'endpoint': '/AttributeValueUnit'})
            msg_handler.logStruct(topic=f"getAttributeValueUnits: Start get all")

        ## variables
        func_parameters = locals()
        base_params = buildRequestParameters(parameters=func_parameters)

        page = 1
        attributeUnits = []
        while True:
            base_params.update({"page": page})

            ## logging
            if bool(os.getenv('DEBUG','False')) and logger:
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
                    if bool(os.getenv('DEBUG','False')) and logger:
                        msg_handler.logStruct(topic="getAttributeValueUnits: No new data so all gathered",
                                              status_code=response_code,
                                              response_text=response_text)
                    break

            else:
                ## process if error was in call
                if bool(os.getenv('DEBUG','False')) and logger:
                    msg_handler.logStruct(level="ERROR",
                                          topic="getAttributeValueUnits: status code not 200",
                                          status_code=response_code,
                                          response_text=response_text)
                break

        ## logging
        if bool(os.getenv('DEBUG','False')) and logger:
            msg_handler.logStruct(topic=f"getAttributeValueUnits: Finish get all. Length: {len(attributeUnits)}")

        return attributeUnits

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
               sortBy: str = None,
               **kwargs) -> list:

        ## logging
        if bool(os.getenv('DEBUG', 'False')) and logger:
            msg_handler = messageHandler(logger=logger, level="DEBUG",
                                         labels={'function': 'getAllBrands',
                                                 'endpoint': '/Brand'})
            msg_handler.logStruct(topic=f"getAllBrands: Start get all brands.")

        ## variables
        func_parameters = locals()
        base_params = buildRequestParameters(parameters=func_parameters)

        next_page = True
        page = 1
        brands = []
        while next_page:
            base_params.update({"page": page})

            ## logging
            if bool(os.getenv('DEBUG','False')) and logger:
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
                    if bool(os.getenv('DEBUG','False')) and logger:
                        msg_handler.logStruct(topic="getAllBrands: No new data so all brands gathered",
                                               status_code=response_code,
                                               response_text=response_text)
                    break

            else:
                ## process if error was in call
                if bool(os.getenv('DEBUG','False')) and logger:
                    msg_handler.logStruct(level="ERROR",
                                   topic="getAllBrands: status code not 200",
                                   status_code=response_code,
                                   response_text=response_text)
                break

        ## logging
        if bool(os.getenv('DEBUG','False')) and logger:
            msg_handler.logStruct(topic=f"getAllBrands: Finish get all brands. Length: {len(brands)}")

        return brands

class Series:
    @staticmethod
    def getAll(connection: object,
               logger: object = None,
               resultsPerPage: int = 1000,
               page: int = 1,
               **kwargs) -> list:

        ## logging
        if bool(os.getenv('DEBUG','False')) and logger:
            msg_handler = messageHandler(logger=logger, level="DEBUG",
                                         labels={'function': 'getAllSeries',
                                                 'endpoint': '/Series'})
            msg_handler.logStruct(topic=f"getAllSeries: Start get all series.")

        ## variables
        func_parameters = locals()
        base_params = buildRequestParameters(parameters=func_parameters)

        next_page = True
        series = []
        try:
            while next_page:
                base_params.update({"page": page})

                ## logging
                if bool(os.getenv('DEBUG','False')) and logger:
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
                        if bool(os.getenv('DEBUG','False')) and logger:
                            msg_handler.logStruct(
                                topic="getAllSeries: No new data so all series gathered",
                                status_code=response_code,
                                response_text=response_text,
                                level="DEBUG")
                        break

                else:
                    if bool(os.getenv('DEBUG','False')) and logger:
                        msg_handler.logStruct(level="ERROR",
                                              topic="getAllSeries: Error in the get all function",
                                              status_code=r.status_code,
                                              response_text=r.text)
                    break

        except Exception as e:
            if bool(os.getenv('DEBUG', 'False')) and logger:
                msg_handler.logStruct(topic="getAllSeries: Error getting all series",
                                      error_message=str(e))
            else:
                print(f"getAllSeries: Error getting all series. Error: {str(e)}")

        if bool(os.getenv('DEBUG','False')) and logger:
            msg_handler.logStruct(topic=f"getAllSeries: Finish get all series. Length: {len(series)}.")

        return series

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
               query: str = None,
               **kwargs) -> list:

        ## variables
        func_parameters = locals()
        base_params = buildRequestParameters(parameters=func_parameters)

        ## logging
        if bool(os.getenv('DEBUG','False')) and logger:
            start_time = datetime.now()
            msg_handler = messageHandler(logger=logger, level="DEBUG",
                                         labels={'function': 'getAllProducts',
                                                 'endpoint': '/Product',
                                                 'data': base_params})

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
                            if bool(os.getenv('DEBUG','False')) and logger:
                                msg_handler.logStruct(topic="getAllProducts: No new data so all products gathered",
                                                      status_code=response_code,
                                                      response_text=response_text)
                            break
                    else:
                        if bool(os.getenv('DEBUG','False')) and logger:
                            msg_handler.logStruct(level="ERROR",
                                                  topic="getAllProducts: Error in the get all function",
                                                  status_code=response_code,
                                                  response_text=response_text)
                        break
                else:
                    if bool(os.getenv('DEBUG','False')) and logger:
                        msg_handler.logStruct(level="DEBUG",
                                              topic=f"getAllProducts: max results reached. max: {max_results}")
                    break

        except Exception as e:
            if bool(os.getenv('DEBUG','False')) and logger:
                msg_handler.logStruct(topic="getAllProducts: Error getting all products",
                                      error_message=str(e))

        if bool(os.getenv('DEBUG','False')) and logger:
            msg_handler.logStruct(
                topic=f"getAllProducts: Finish get all products. Length: {len(products)}.\n "
                      f"processing time: {datetime.now() - start_time}")

        return products

    @staticmethod
    def getAllExternalIds(connection: object,
                          logger: object = None,
                          sourceId: int = None,
                          **kwargs) -> dict:

        ## variables
        func_parameters = locals()
        base_params = buildRequestParameters(parameters=func_parameters)

        if bool(os.getenv('DEBUG','False')) and logger:
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
                    if bool(os.getenv('DEBUG','False')) and logger:
                        msg_handler.logStruct(topic="getAllExternalProductIds: No data in request",
                                              status_code=response_code,
                                              response_text=response_text)
            else:
                if bool(os.getenv('DEBUG','False')) and logger:
                    msg_handler.logStruct(level="ERROR",
                                          topic="getAllExternalProductIds: Error in the get all function",
                                          status_code=response_code,
                                          response_text=response_text)

        except Exception as e:
            if bool(os.getenv('DEBUG','False')) and logger:
                msg_handler.logStruct(topic="getAllExternalProductIds: Error getting all external product ids",
                                      error_message=str(e))

        if bool(os.getenv('DEBUG','False')) and logger:
            msg_handler.logStruct(
                topic=f"getAllExternalProductIds: Finish get all products external ids. Length: {len(products)}")

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
        if bool(os.getenv('DEBUG','False')) and logger:
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
            if bool(os.getenv('DEBUG','False')) and logger:
                msg_handler.logStruct(level="ERROR",
                                      topic="getProduct: Error in the get all function",
                                      status_code=response_code,
                                      response_text=response_text)

        return {}


def getUserSearch(identifier: str,
                  identifierType: str,
                  connection: object,
                  logger: object = None,
                  **kwargs) -> dict:

    ## logging
    if logger:
        msg_handler = messageHandler(logger=logger, level="DEBUG",
                                     labels={'function': 'getUserSearch',
                                             'endpoint': '/User/Search'})
        msg_handler.logStruct(topic=f"getUserSearch: Start get user {identifier}")

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
        if logger:
            msg_handler.logStruct(level="ERROR",
                                  topic="getUserSearch: Error in the get function",
                                  status_code=response_code,
                                  response_text=response_text)

    return {}
