import os
import json
from loggingYour.localLogging import LocalLogger


class Product:
    @staticmethod
    def es_sync(connection: object,
                product_ids: list,
                logger: LocalLogger = None) -> bool:

        ## logging
        if logger and os.environ.get('DEBUG') == 'DEBUG':
            log_message = {"topic": f"start create brand",
                           "function": "esProductSync",
                           "endpoint": "/Product",
                           "productIds": product_ids}
            logger.createDebugLog(message=log_message)

        # Process
        encoded_data = json.dumps(product_ids).encode('utf-8')
        r = connection.request(method="POST",
                               url=f"{os.environ['YOUR_API_URL']}/Product/EnforceSyncWithES",
                               body=encoded_data,
                               headers={'Authorization': 'Bearer ' + os.environ["YOUR_API_TOKEN"],
                                        'Content-Type': 'application/json'})
        status_code = r.status
        resp_data = r.data

        if status_code == 200:
            return True

        else:
            return False

    @staticmethod
    def patch(connection: object,
              product_id: str,
              payload: dict,
              logger: LocalLogger = None) -> bool:

        ## logging
        if logger and os.environ.get('DEBUG') == 'DEBUG':
            log_message = {"topic": f"start create brand",
                           "function": "ProductPatch",
                           "endpoint": "/Product",
                           "productId": product_id,
                           "payload": payload}
            logger.createDebugLog(message=log_message)

        # Process
        encoded_data = json.dumps(payload).encode('utf-8')
        r = connection.request(method="PATCH",
                               url=f"{os.environ['YOUR_API_URL']}/Product/{product_id}",
                               body=encoded_data,
                               headers={'Authorization': 'Bearer ' + os.environ["YOUR_API_TOKEN"],
                                        'Content-Type': 'application/json'})
        status_code = r.status
        resp_data = r.data

        if status_code == 200:
            return True

        else:
            return False


class Brand:
    @staticmethod
    def create(connection: object,
               data: dict,
               logger: LocalLogger = None) -> int:

        ## logging
        if logger and os.environ.get('DEBUG') == 'DEBUG':
            log_message = {"topic": f"start create brand",
                           "function": "createBrand",
                           "endpoint": "/Brand",
                           "data": data}
            logger.createDebugLog(message=log_message)

        ## process request from connection pool
        encoded_data = json.dumps(data).encode('utf-8')
        r = connection.request(method="POST",
                               url=f"{os.environ['YOUR_API_URL']}/Brand",
                               body=encoded_data,
                               headers={'Authorization': 'Bearer ' + os.environ["YOUR_API_TOKEN"],
                                        'Content-Type': 'application/json'})
        status_code = r.status
        resp_data = r.data

        if status_code in [200, 400]:
            resp_body = json.loads(resp_data.decode('utf-8'))
            resp_data = resp_body.get('data')
            success = resp_body.get('success')
            code = resp_body.get('code')

            if success or code == 11:
                brand_id = resp_data.get('id')

                ## logging
                if logger and os.environ.get('DEBUG') == 'DEBUG':
                    log_message = {"topic": f"finished create brand",
                                   "function": "createBrand",
                                   "status_code": status_code,
                                   "brandId": brand_id,
                                   "endpoint": "/Brand"}
                    logger.createDebugLog(message=log_message)

                return brand_id

            else:
                ## logging
                if logger and os.environ.get('DEBUG') == 'DEBUG':
                    log_message = {"topic": f"no response data",
                                   "function": "createBrand",
                                   "status_code": status_code,
                                   "response_text": resp_data,
                                   "endpoint": "/Brand"}
                    logger.createWarningLog(message=log_message)

        else:
            ## logging
            if logger and os.environ.get('DEBUG') == 'DEBUG':
                log_message = {"topic": f"error create brand",
                               "function": "createBrand",
                               "status_code": status_code,
                               "response_text": resp_data,
                               "endpoint": "/Brand"}
                logger.createErrorLog(message=log_message)

        return

class Category:
    @staticmethod
    def create(payload: dict,
               connection: object,
               logger: LocalLogger = None,
               additional_labels: dict = {}) -> int:

        ## logging
        if logger and os.environ.get('DEBUG') == 'DEBUG':
            log_message = {"topic": f"start create category",
                           "function": "createCategory",
                           "endpoint": "/Category",
                           "data": payload,
                           "labels": additional_labels}
            logger.createDebugLog(message=log_message)

        ## process request from connection pool
        encoded_data = json.dumps(payload).encode('utf-8')
        r = connection.request(method="POST",
                               url=f"{os.environ['YOUR_API_URL']}/Category",
                               body=encoded_data,
                               headers={'Authorization': 'Bearer ' + os.environ["YOUR_API_TOKEN"],
                                        'Content-Type': 'application/json'})
        status_code = r.status
        resp_data = r.data

        if status_code in [200, 400]:
            resp_body = json.loads(resp_data.decode('utf-8'))
            resp_data = resp_body.get('data')
            success = resp_body.get('success')
            code = resp_body.get('code')

            if resp_data and (success or code == 11):
                cat_id = resp_data.get('id')

                ## logging
                if logger and os.environ.get('DEBUG') == 'DEBUG':
                    log_message = {"topic": f"category created or exist finished",
                                   "function": "createCategory",
                                   "endpoint": "/Category",
                                   "code": status_code,
                                   "response": resp_data,
                                   "categoryId": cat_id,
                                   "labels": additional_labels}
                    logger.createDebugLog(message=log_message)

                return cat_id

            else:
                ## logging
                if logger and os.environ.get('DEBUG') == 'DEBUG':
                    log_message = {"topic": f"no response data",
                                   "function": "createCategory",
                                   "endpoint": "/Category",
                                   "code": status_code,
                                   "response": resp_data,
                                   "labels": additional_labels}
                    logger.createWarningLog(message=log_message)

        else:
            ## logging
            if logger and os.environ.get('DEBUG') == 'DEBUG':
                log_message = {"topic": f"Error create category",
                               "function": "createCategory",
                               "endpoint": "/Category",
                               "code": status_code,
                               "response": resp_data,
                               "labels": additional_labels}
                logger.createErrorLog(message=log_message)


class Series:
    @staticmethod
    def create(data: dict,
               connection: object,
               logger: LocalLogger = None,
               labels: dict = {}) -> int:

        ## logging
        if logger and os.environ.get('DEBUG') == 'DEBUG':
            log_message = {"topic": f"start create series",
                           "function": "createSeries",
                           "endpoint": "/Series",
                           "data": data,
                           "labels": labels}
            logger.createDebugLog(message=log_message)

        ## process request from connection pool
        encoded_data = json.dumps(data).encode('utf-8')
        r = connection.request(method="POST",
                               url=f"{os.environ['YOUR_API_URL']}/Series",
                               body=encoded_data,
                               headers={'Authorization': 'Bearer ' + os.environ["YOUR_API_TOKEN"],
                                        'Content-Type': 'application/json'})
        status_code = r.status
        resp_data = r.data

        if status_code == 200:
            resp_body = json.loads(resp_data.decode('utf-8'))
            resp_data = resp_body.get('data')
            serie_id = resp_data['data']['id']

            ## logging
            if logger and os.environ.get('DEBUG') == 'DEBUG':
                log_message = {"topic": f"finished create or exist series",
                               "function": "createSeries",
                               "endpoint": "/Series",
                               "code": status_code,
                               "response": resp_data,
                               "seriesId": serie_id,
                               "labels": labels}
                logger.createDebugLog(message=log_message)

            return serie_id

        else:
            ## logging
            if logger and os.environ.get('DEBUG') == 'DEBUG':
                log_message = {"topic": f"error create series",
                               "function": "createSeries",
                               "endpoint": "/Series",
                               "code": status_code,
                               "response": resp_data,
                               "labels": labels}
                logger.createErrorLog(message=log_message)


class Relations:
    @staticmethod
    def createCategoryCategoryRelation(data: dict,
                                        connection: object,
                                       logger: LocalLogger = None,
                                        additional_labels: dict = None) -> bool:
        ## logging
        if logger and os.environ.get('DEBUG') == 'DEBUG':
            log_message = {"topic": f"start relation creation",
                           "function": "createCategoryCategoryRelation",
                           "endpoint": "/Relation/CreateCategoryCategory",
                           "data": data,
                           "labels": additional_labels}
            logger.createDebugLog(message=log_message)

        ## process request from connection pool
        encoded_data = json.dumps(data).encode('utf-8')
        r = connection.request(method="POST",
                               url=f"{os.environ['YOUR_API_URL']}/Relation/CreateCategoryCategory",
                               body=encoded_data,
                               headers={'Authorization': 'Bearer ' + os.environ["YOUR_API_TOKEN"],
                                        'Content-Type': 'application/json'})

        response_code = r.status
        response_text = r.data

        if response_code in [200,400]:
            ## logging
            if logger and os.environ.get('DEBUG') == 'DEBUG':
                log_message = {"topic": f"finished create relation category category",
                               "function": "createCategoryCategoryRelation",
                               "endpoint": "/Relation/CreateCategoryCategory",
                               "code": response_code,
                               "response": response_text,
                               "labels": additional_labels}
                logger.createDebugLog(message=log_message)

            return True

        else:
            ## logging
            if logger and os.environ.get('DEBUG') == 'DEBUG':
                log_message = {"topic": f"warning create relation category category",
                               "function": "createCategoryCategoryRelation",
                               "endpoint": "/Relation/CreateCategoryCategory",
                               "code": response_code,
                               "response": response_text,
                               "labels": additional_labels}
                logger.createWarningLog(message=log_message)

            return False

    @staticmethod
    def createBrandCategoryRelation(data: dict,
                                    connection: object,
                                    logger: LocalLogger = None,
                                    additional_labels: dict = None) -> bool:

        ## logging
        if logger and os.environ.get('DEBUG') == 'DEBUG':
            log_message = {"topic": f"start relation brand category relation",
                           "function": "createBrandCategoryRelation",
                           "endpoint": "/Relation/CreateBrandCategory",
                           "data": data,
                           "labels": additional_labels}
            logger.createDebugLog(message=log_message)

        ## process request from connection pool
        encoded_data = json.dumps(data).encode('utf-8')
        r = connection.request(method="POST",
                               url=f"{os.environ['YOUR_API_URL']}/Relation/CreateBrandCategory",
                               body=encoded_data,
                               headers={'Authorization': 'Bearer ' + os.environ["YOUR_API_TOKEN"],
                                        'Content-Type': 'application/json'})

        response_code = r.status
        response_text = r.data

        if response_code == [200, 400]:
            ## logging
            if logger and os.environ.get('DEBUG') == 'DEBUG':
                log_message = {"topic": f"finished relation brand category relation",
                               "function": "createBrandCategoryRelation",
                               "endpoint": "/Relation/CreateBrandCategory",
                               "code": response_code,
                               "response": response_text,
                               "labels": additional_labels}
                logger.createDebugLog(message=log_message)

            return True

        else:
            ## logging
            if logger and os.environ.get('DEBUG') == 'DEBUG':
                log_message = {"topic": f"warning relation brand category relation",
                               "function": "createBrandCategoryRelation",
                               "endpoint": "/Relation/CreateBrandCategory",
                               "code": response_code,
                               "response": response_text,
                               "labels": additional_labels}
                logger.createWarningLog(message=log_message)

            return False

    @staticmethod
    def createCategoryAttributeRelation(data: dict,
                                        connection: object,
                                        logger: LocalLogger = None,
                                        additional_labels: dict = None) -> bool:

        ## logging
        if logger and os.environ.get('DEBUG') == 'DEBUG':
            log_message = {"topic": f"Start create category attribute relation",
                           "function": "createCategoryAttributeRelation",
                           "endpoint": "/Relation/CreateAttributeCategory",
                           "data": data,
                           "labels": additional_labels}
            logger.createDebugLog(message=log_message)

        ## process request from connection pool
        encoded_data = json.dumps(data).encode('utf-8')
        r = connection.request(method="POST",
                               url=f"{os.environ['YOUR_API_URL']}/Relation/CreateAttributeCategory",
                               body=encoded_data,
                               headers={'Authorization': 'Bearer ' + os.environ["YOUR_API_TOKEN"],
                                        'Content-Type': 'application/json'})

        response_code = r.status
        response_text = r.data

        if response_code in [200, 400]:
            ## logging
            if logger and os.environ.get('DEBUG') == 'DEBUG':
                log_message = {"topic": f"finished create relation category attribute",
                               "function": "createCategoryAttributeRelation",
                               "endpoint": "/Relation/CreateAttributeCategory",
                               "code": response_code,
                               "response": response_text,
                               "labels": additional_labels}
                logger.createDebugLog(message=log_message)

            return True

        else:
            ## logging
            if logger and os.environ.get('DEBUG') == 'DEBUG':
                log_message = {"topic": f"warning create relation category attribute",
                               "function": "createCategoryAttributeRelation",
                               "endpoint": "/Relation/CreateAttributeCategory",
                               "code": response_code,
                               "response": response_text,
                               "labels": additional_labels}
                logger.createWarningLog(message=log_message)

            return False

    @staticmethod
    def createProductProductRelation(data: dict,
                                     connection: object,
                                     logger: LocalLogger = None,
                                     additional_labels: dict = None) -> bool:

        ## logging
        if logger and os.environ.get('DEBUG') == 'DEBUG':
            log_message = {"topic": f"Start create product product relation",
                           "function": "createProductProductRelation",
                           "endpoint": "/Relation/CreateProductProduct",
                           "data": data,
                           "labels": additional_labels}
            logger.createDebugLog(message=log_message)

        ## process request from connection pool
        encoded_data = json.dumps(data).encode('utf-8')
        r = connection.request(method="POST",
                               url=f"{os.environ['YOUR_API_URL']}/Relation/CreateProductProduct",
                               body=encoded_data,
                               headers={'Authorization': 'Bearer ' + os.environ["YOUR_API_TOKEN"],
                                        'Content-Type': 'application/json'})

        response_code = r.status
        response_text = r.data

        if response_code in [200, 400]:
            ## logging
            if logger and os.environ.get('DEBUG') == 'DEBUG':
                log_message = {"topic": f"finished create or exist product product relation",
                               "function": "createProductProductRelation",
                               "endpoint": "/Relation/CreateProductProduct",
                               "code": response_code,
                               "response": response_text,
                               "data": data,
                               "labels": additional_labels}
                logger.createDebugLog(message=log_message)

            return True

        else:
            ## logging
            if logger and os.environ.get('DEBUG') == 'DEBUG':
                log_message = {"topic": f"error create product product relation",
                               "function": "createProductProductRelation",
                               "endpoint": "/Relation/CreateProductProduct",
                               "code": response_code,
                               "response": response_text,
                               "data": data,
                               "labels": additional_labels}
                logger.createWarningLog(message=log_message)

            return False

    @staticmethod
    def createCategoryProductRelation(data: dict,
                                      connection: object,
                                      logger: LocalLogger = None,
                                      additional_labels: dict = None) -> bool:

        ## logging
        if logger and os.environ.get('DEBUG') == 'DEBUG':
            log_message = {"topic": f"Start create category product relation",
                           "function": "createCategoryProductRelation",
                           "endpoint": "/Relation/CreateCategoryProduct",
                           "data": data,
                           "labels": additional_labels}
            logger.createDebugLog(message=log_message)

        ## process request from connection pool
        encoded_data = json.dumps(data).encode('utf-8')
        r = connection.request(method="POST",
                               url=f"{os.environ['YOUR_API_URL']}/Relation/CreateCategoryProduct",
                               body=encoded_data,
                               headers={'Authorization': 'Bearer ' + os.environ["YOUR_API_TOKEN"],
                                        'Content-Type': 'application/json'})

        response_code = r.status
        response_text = r.data

        if response_code in [200, 400]:
            ## logging
            if logger and os.environ.get('DEBUG') == 'DEBUG':
                log_message = {"topic": f"finished create relation category product",
                               "function": "createCategoryProductRelation",
                               "endpoint": "/Relation/CreateCategoryProduct",
                               "code": response_code,
                               "response": response_text,
                               "labels": additional_labels}
                logger.createDebugLog(message=log_message)

            return True

        else:
            ## logging
            if logger and os.environ.get('DEBUG') == 'DEBUG':
                log_message = {"topic": f"error create relation category product",
                               "function": "createCategoryProductRelation",
                               "endpoint": "/Relation/CreateCategoryProduct",
                               "code": response_code,
                               "response": response_text,
                               "labels": additional_labels}
                logger.createWarningLog(message=log_message)

            return False

class Attributes:
    @staticmethod
    def createAttribute(data: dict,
                        connection: object,
                        logger: LocalLogger = None,
                        additional_labels: dict = {}) -> int:

        ## logging
        if logger and os.environ.get('DEBUG') == 'DEBUG':
            log_message = {"topic": f"Start create attribute",
                           "function": "createAttribute",
                           "endpoint": "/Attribute",
                           "data": data,
                           "labels": additional_labels}
            logger.createDebugLog(message=log_message)

        ## process request from connection pool
        encoded_data = json.dumps(data).encode('utf-8')
        r = connection.request(method="POST",
                               url=f"{os.environ['YOUR_API_URL']}/Attribute",
                               body=encoded_data,
                               headers={'Authorization': 'Bearer ' + os.environ["YOUR_API_TOKEN"],
                                        'Content-Type': 'application/json'})
        status_code = r.status
        resp_data = r.data

        if status_code in [200, 400]:
            resp_body = json.loads(resp_data.decode('utf-8'))
            resp_data = resp_body.get('data')
            success = resp_body.get('success')
            code = resp_body.get('code')

            if success or code == 11:
                attribute_id = resp_data['id']

                ## logging
                if logger and os.environ.get('DEBUG') == 'DEBUG':
                    log_message = {"topic": f"finished create attribute",
                                   "function": "createAttribute",
                                   "endpoint": "/Attribute",
                                   "code": status_code,
                                   "response": resp_data,
                                   "attributeId": attribute_id,
                                   "labels": additional_labels}
                    logger.createDebugLog(message=log_message)

                return attribute_id

            else:
                ## logging
                if logger and os.environ.get('DEBUG') == 'DEBUG':
                    log_message = {"topic": f"no response data",
                                   "function": "createCategoryProductRelation",
                                   "endpoint": "/Attribute",
                                   "code": status_code,
                                   "response": resp_data,
                                   "labels": additional_labels}
                    logger.createWarningLog(message=log_message)

        else:
            ## logging
            if logger and os.environ.get('DEBUG') == 'DEBUG':
                log_message = {"topic": f"error creating attribute",
                               "function": "createCategoryProductRelation",
                               "endpoint": "/Attribute",
                               "code": status_code,
                               "response": resp_data,
                               "labels": additional_labels}
                logger.createErrorLog(message=log_message)

        return

    @staticmethod
    def createValueUnit(data: dict,
                        connection: object,
                        logger: LocalLogger = None,
                        additional_labels: dict = None):
        ## logging
        if logger and os.environ.get('DEBUG') == 'DEBUG':
            log_message = {"topic": f"Start create attribute value unit",
                           "function": "createAttributeValueUnit",
                           "endpoint": "/AttributeValueUnit",
                           "data": data,
                           "labels": additional_labels}
            logger.createDebugLog(message=log_message)

        ## process request from connection pool
        encoded_data = json.dumps(data).encode('utf-8')
        r = connection.request(method="POST",
                               url=f"{os.environ['YOUR_API_URL']}/AttributeValueUnit",
                               body=encoded_data,
                               headers={'Authorization': 'Bearer ' + os.environ["YOUR_API_TOKEN"],
                                        'Content-Type': 'application/json'})
        status_code = r.status
        resp_data = r.data

        if status_code in [200, 400]:
            resp_body = json.loads(resp_data.decode('utf-8'))
            if resp_body.get('data'):
                unit_id = resp_body['data'].get('id')

                ## logging
                if logger and os.environ.get('DEBUG') == 'DEBUG':
                    log_message = {"topic": f"finished creating",
                                   "function": "createAttributeValueUnit",
                                   "endpoint": "/AttributeValueUnit",
                                   "code": status_code,
                                   "response": resp_data,
                                   "unitId": unit_id,
                                   "labels": additional_labels}
                    logger.createDebugLog(message=log_message)

                return unit_id

            else:
                ## logging
                if logger and os.environ.get('DEBUG') == 'DEBUG':
                    log_message = {"topic": f"no response data",
                                   "function": "createAttributeValueUnit",
                                   "endpoint": "/AttributeValueUnit",
                                   "code": status_code,
                                   "response": resp_data,
                                   "labels": additional_labels}
                    logger.createWarningLog(message=log_message)

        else:
            ## logging
            if logger and os.environ.get('DEBUG') == 'DEBUG':
                log_message = {"topic": f"error creating attribute value unit",
                               "function": "createAttributeValueUnit",
                               "endpoint": "/AttributeValueUnit",
                               "code": status_code,
                               "response": resp_data,
                               "labels": additional_labels}
                logger.createErrorLog(message=log_message)

        return


class Questions:
    @staticmethod
    def create(data: dict,
               connection: object,
               logger: LocalLogger = None):
        ## logging
        if logger and os.environ.get('DEBUG') == 'DEBUG':
            log_message = {"topic": f"Start create qna entry value unit",
                           "function": "createQnA",
                           "endpoint": "/QnA/Question",
                           "data": data}
            logger.createDebugLog(message=log_message)

        ## process request from connection pool
        encoded_data = json.dumps(data).encode('utf-8')
        r = connection.request(method="POST",
                               url=f"{os.environ['YOUR_API_URL']}/QnA/Question",
                               body=encoded_data,
                               headers={'Authorization': 'Bearer ' + os.environ["YOUR_API_TOKEN"],
                                        'Content-Type': 'application/json'})
        status_code = r.status
        resp_data = r.data

        if status_code in [200, 400]:
            resp_body = json.loads(resp_data.decode('utf-8'))
            if resp_body.get('data'):
                qna_id = resp_body['data'].get('id')

                ## logging
                if logger and os.environ.get('DEBUG') == 'DEBUG':
                    log_message = {"topic": f"finished creating",
                                   "function": "createQnA",
                                   "endpoint": "/QnA/Question",
                                   "code": status_code,
                                   "response": str(resp_data),
                                   "qnaId": qna_id}
                    logger.createDebugLog(message=log_message)
                    print(log_message)

                return qna_id

            else:
                ## logging
                if logger and os.environ.get('DEBUG') == 'DEBUG':
                    log_message = {"topic": f"no response data",
                                   "function": "createQnA",
                                   "endpoint": "/QnA/Question",
                                   "code": status_code,
                                   "response": str(resp_data)}
                    logger.createWarningLog(message=log_message)
                    print(log_message)

        else:
            ## logging
            if logger and os.environ.get('DEBUG') == 'DEBUG':
                log_message = {"topic": f"error creating qna",
                               "function": "createQnA",
                               "endpoint": "/QnA/Question",
                               "code": status_code,
                               "response": str(resp_data)}
                logger.createErrorLog(message=log_message)
                print(log_message)
