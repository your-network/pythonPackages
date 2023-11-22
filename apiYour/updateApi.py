import os
import json
from loggingYour.localLogging import LocalLogger

class Category:
    @staticmethod
    def putUpdate(payload: dict,
                  category_id: int,
                  connection: object,
                  logger: LocalLogger = None) -> list:

        ## logging
        if logger and os.environ.get('DEBUG') == 'DEBUG':
            log_message = {"topic": f"Start update",
                           "function": "updateCategory",
                           "endpoint": "/Category/{category_id}",
                           "categoryId": category_id,
                           "data": payload}
            logger.createDebugLog(message=log_message)

        ## process request from connection pool
        encoded_data = json.dumps(payload).encode('utf-8')
        r = connection.request(method="PUT",
                               url=f"{os.environ['YOUR_API_URL']}/Category/{category_id}",
                               body=encoded_data,
                               headers={'Authorization': 'Bearer ' + os.environ["YOUR_API_TOKEN"],
                                        'Content-Type': 'application/json'})
        status_code = r.status
        response_text = r.data

        if status_code == 200:
            resp_body = json.loads(response_text.decode('utf-8'))
            resp_data = resp_body.get('data')

            if resp_data:
                media = resp_data.get('duplicates', [])

                ## logging
                if logger and os.environ.get('DEBUG') == 'DEBUG':
                    log_message = {"topic": f"Finish update",
                                   "function": "updateCategory",
                                   "endpoint": "/Category/{category_id}",
                                   "categoryId": category_id}
                    logger.createDebugLog(message=log_message)

                return media

        else:
            ## logging
            if logger and os.environ.get('DEBUG') == 'DEBUG':
                log_message = {"topic": f"Error update",
                               "function": "updateCategory",
                               "endpoint": "/Category/{category_id}",
                               "categoryId": category_id,
                               "code": status_code,
                               "response": response_text}
                logger.createErrorLog(message=log_message)

            return []

    @staticmethod
    def patchUpdate(payload: dict,
                   category_id: int,
                   connection: object,
                   logger: LocalLogger = None) -> list:

        ## logging
        if logger and os.environ.get('DEBUG') == 'DEBUG':
            log_message = {"topic": f"Start update",
                           "function": "patchUpdateCategory",
                           "endpoint": "/Category/{category_id}",
                           "categoryId": category_id,
                           "data": payload}
            logger.createDebugLog(message=log_message)

        ## process request from connection pool
        encoded_data = json.dumps(payload).encode('utf-8')
        r = connection.request(method="PATCH",
                               url=f"{os.environ['YOUR_API_URL']}/Category/{category_id}",
                               body=encoded_data,
                               headers={'Authorization': 'Bearer ' + os.environ["YOUR_API_TOKEN"],
                                        'Content-Type': 'application/json'})
        status_code = r.status
        response_text = r.data

        if status_code == 200:
            resp_body = json.loads(response_text.decode('utf-8'))
            resp_data = resp_body.get('data')

            if resp_data:
                media = resp_data.get('duplicates', [])

                ## logging
                if logger and os.environ.get('DEBUG') == 'DEBUG':
                    log_message = {"topic": f"Finish update",
                                   "function": "patchUpdateCategory",
                                   "endpoint": "/Category/{category_id}",
                                   "categoryId": category_id}
                    logger.createDebugLog(message=log_message)

                return media

        else:
            ## logging
            if logger and os.environ.get('DEBUG') == 'DEBUG':
                log_message = {"topic": f"Error update",
                               "function": "patchUpdateCategory",
                               "endpoint": "/Category/{category_id}",
                               "categoryId": category_id,
                               "code": status_code,
                               "response": response_text}
                logger.createErrorLog(message=log_message)

            return []

class Brand:
    @staticmethod
    def putUpdate(payload: dict,
                  brand_id: int,
                  connection: object,
                  logger: LocalLogger = None) -> list:

        ## logging
        if logger and os.environ.get('DEBUG') == 'DEBUG':
            log_message = {"topic": f"Start update",
                           "function": "updateBrand",
                           "endpoint": "/Brand/{brandId}",
                           "brandId": brand_id,
                           "data": payload}
            logger.createDebugLog(message=log_message)

        ## process request from connection pool
        encoded_data = json.dumps(payload).encode('utf-8')
        r = connection.request(method="PUT",
                               url=f"{os.environ['YOUR_API_URL']}/Brand/{brand_id}",
                               body=encoded_data,
                               headers={'Authorization': 'Bearer ' + os.environ["YOUR_API_TOKEN"],
                                        'Content-Type': 'application/json'})
        status_code = r.status
        response_text = r.data

        if status_code == 200:
            resp_body = json.loads(response_text.decode('utf-8'))
            resp_data = resp_body.get('data')
            if resp_data:
                media = resp_data.get('duplicates', [])

                ## logging
                if logger and os.environ.get('DEBUG') == 'DEBUG':
                    log_message = {"topic": f"Finish update",
                                   "function": "updateBrand",
                                   "endpoint": "/Brand/{brandId}",
                                   "brandId": brand_id}
                    logger.createDebugLog(message=log_message)

                return media

        else:
            ## logging
            if logger and os.environ.get('DEBUG') == 'DEBUG':
                log_message = {"topic": f"Finish update",
                               "function": "updateBrand",
                               "endpoint": "/Brand/{brandId}",
                               "brandId": brand_id,
                               "code": status_code,
                               "response": response_text}
                logger.createErrorLog(message=log_message)

            return []

class Attribute:
    @staticmethod
    def putUpdate(payload: dict,
                  attribute_id: int,
                  connection: object,
                  logger: LocalLogger = None) -> list:

        ## logging
        if logger and os.environ.get('DEBUG') == 'DEBUG':
            log_message = {"topic": f"Start update",
                           "function": "putUpdateAttribute",
                           "endpoint": "/Attribute/{attributeId}",
                           "attributeId": attribute_id,
                           "data": payload}
            logger.createDebugLog(message=log_message)

        ## process request from connection pool
        encoded_data = json.dumps(payload).encode('utf-8')
        r = connection.request(method="PUT",
                               url=f"{os.environ['YOUR_API_URL']}/Attribute/{attribute_id}",
                               body=encoded_data,
                               headers={'Authorization': 'Bearer ' + os.environ["YOUR_API_TOKEN"],
                                        'Content-Type': 'application/json'})
        status_code = r.status
        response_text = r.data

        if status_code == 200:
            resp_body = json.loads(response_text.decode('utf-8'))
            resp_data = resp_body.get('data')
            if resp_data:
                media = resp_data.get('duplicates', [])

                return media

        else:
            ## logging
            if logger and os.environ.get('DEBUG') == 'DEBUG':
                log_message = {"topic": f"Error update",
                               "function": "putUpdateAttribute",
                               "endpoint": "/Attribute/{attributeId}",
                               "attributeId": attribute_id,
                               "code": status_code,
                               "response": response_text}
                logger.createErrorLog(message=log_message)

            return []

    @staticmethod
    def putUpdateValueUnit(payload: dict,
                           unitId: int,
                           connection: object,
                           logger: LocalLogger = None) -> bool:

        ## logging
        if logger and os.environ.get('DEBUG') == 'DEBUG':
            log_message = {"topic": f"Start update",
                           "function": "putUpdateValueUnit",
                           "endpoint": "/AttributeValueUnit/{unitId}",
                           "unitId": unitId,
                           "data": payload}
            logger.createDebugLog(message=log_message)

        ## process request from connection pool
        encoded_data = json.dumps(payload).encode('utf-8')
        r = connection.request(method="PUT",
                               url=f"{os.environ['YOUR_API_URL']}/AttributeValueUnit/{unitId}",
                               body=encoded_data,
                               headers={'Authorization': 'Bearer ' + os.environ["YOUR_API_TOKEN"],
                                        'Content-Type': 'application/json'})
        status_code = r.status
        response_text = r.data

        if status_code == 200:
            return True

        else:
            ## logging
            if logger and os.environ.get('DEBUG') == 'DEBUG':
                log_message = {"topic": f"Error update",
                               "function": "putUpdateValueUnit",
                               "endpoint": "/AttributeValueUnit/{unitId}",
                               "unitId": unitId,
                               "code": status_code,
                               "response": response_text}
                logger.createErrorLog(message=log_message)

            return False


class Product:
    @staticmethod
    def putUpdate(productId: int,
                  payload: dict,
                  additional_labels: dict = {},
                  connection: object = None,
                  logger: LocalLogger = None) -> list:

        ## logging
        if logger and os.environ.get('DEBUG') == 'DEBUG':
            log_message = {"topic": f"Start update",
                           "function": "putUpdateProduct",
                           "endpoint": "/Product/{productId}",
                           "productId": productId,
                           "data": payload}
            logger.createDebugLog(message=log_message, **additional_labels)

        ## process request from connection pool
        encoded_data = json.dumps(payload).encode('utf-8')
        r = connection.request(method="PUT",
                               url=f"{os.environ['YOUR_API_URL']}/Product/{productId}",
                               body=encoded_data,
                               headers={'Authorization': 'Bearer ' + os.environ["YOUR_API_TOKEN"],
                                        'Content-Type': 'application/json'})

        response_code = r.status
        response_text = r.data
        if response_code == 200:
            result = json.loads(response_text.decode('utf-8'))
            resp_data = result.get('data')
            if resp_data:
                media = resp_data.get('duplicates', [])

                return media

        else:
            ## logging
            if logger and os.environ.get('DEBUG') == 'DEBUG':
                log_message = {"topic": f"Error update",
                               "function": "putUpdateProduct",
                               "endpoint": "/Product/{productId}",
                               "productId": productId,
                               "code": response_code,
                               "response": response_text}
                logger.createErrorLog(message=log_message, **additional_labels)

            return []

    @staticmethod
    def patch(productId: int,
              payload: dict,
              additional_labels: dict = {},
              connection: object = None,
              logger: LocalLogger = None) -> list:

        ## logging
        if logger and os.environ.get('DEBUG') == 'DEBUG':
            log_message = {"topic": f"Start update",
                           "function": "patchUpdateProduct",
                           "endpoint": "/Product/{productId}",
                           "productId": productId,
                           "data": payload}
            logger.createDebugLog(message=log_message, **additional_labels)
            print(log_message)

        ## process request from connection pool
        encoded_data = json.dumps(payload).encode('utf-8')
        r = connection.request(method="PATCH",
                               url=f"{os.environ['YOUR_API_URL']}/Product/{productId}",
                               body=encoded_data,
                               headers={'Authorization': 'Bearer ' + os.environ["YOUR_API_TOKEN"],
                                        'Content-Type': 'application/json'})

        response_code = r.status
        response_text = r.data
        if response_code == 200:
            result = json.loads(response_text.decode('utf-8'))
            resp_data = result.get('data')
            if resp_data:
                media = resp_data.get('duplicates', [])

                return media

        else:
            ## logging
            if logger and os.environ.get('DEBUG') == 'DEBUG':
                log_message = {"topic": f"Error update",
                               "function": "patchUpdateProduct",
                               "endpoint": "/Product/{productId}",
                               "productId": productId,
                               "code": response_code,
                               "response": str(response_text)}
                logger.createErrorLog(message=log_message, **additional_labels)
                print(log_message)

            return []


class Series:
    @staticmethod
    def putUpdate(seriesId: int,
                  payload: dict,
                  connection: object,
                  additional_labels: dict = {},
                  logger: LocalLogger = None) -> bool:

        ## logging
        if logger and os.environ.get('DEBUG') == 'DEBUG':
            log_message = {"topic": f"Start update",
                           "function": "putUpdateSeries",
                           "endpoint": "/Series/{seriesId}",
                           "seriesId": seriesId,
                           "data": payload}
            logger.createDebugLog(message=log_message, **additional_labels)

        ## process request from connection pool
        encoded_data = json.dumps(payload).encode('utf-8')
        r = connection.request(method="PUT",
                               url=f"{os.environ['YOUR_API_URL']}/Series/{seriesId}",
                               body=encoded_data,
                               headers={'Authorization': 'Bearer ' + os.environ["YOUR_API_TOKEN"],
                                        'Content-Type': 'application/json'})

        response_code = r.status
        response_text = r.data

        if response_code == 200:
            return True

        else:
            ## logging
            if logger and os.environ.get('DEBUG') == 'DEBUG':
                log_message = {"topic": f"Error update",
                               "function": "putUpdateSeries",
                               "endpoint": "/Series/{seriesId}",
                               "seriesId": seriesId,
                               "data": payload,
                               "code": response_code,
                               "response": response_text}
                logger.createErrorLog(message=log_message, **additional_labels)

        return False