import os
import requests
import json
from loggingYour.messageHandler import messageHandler
from apiYour.settingsApi import PRODUCTION_ADDRESS, DEVELOPMENT_ADDRESS

class Category:
    @staticmethod
    def putUpdate(payload: dict,
                  category_id: int,
                  connection: object,
                  logger: object = None) -> list:

        ## logging
        if bool(os.environ['DEBUG']) and logger:
            msg_handler = messageHandler(logger=logger, level="DEBUG",
                                         labels={'function': 'updateCategory', 'endpoint': '/Category/{category_id}'})
            msg_handler.logStruct(topic=f"updateCategory: categoryId: {category_id}, start updating category.", data=payload)

        ## process request from connection pool
        encoded_data = json.dumps(payload).encode('utf-8')
        r = connection.request(method="PUT",
                               url=f"{os.environ['YOUR_API_URL']}/Category/{category_id}",
                               body=encoded_data,
                               headers={'Authorization': 'Bearer ' + os.environ["YOUR_API_TOKEN"],
                                        'Content-Type': 'application/json'})
        status_code = r.status

        if status_code == 200:
            resp_body = json.loads(r.data.decode('utf-8'))
            resp_data = resp_body.get('data')

            if resp_data:
                media = resp_data.get('duplicates', [])

                ## logging
                if bool(os.environ['DEBUG']) and logger:
                    msg_handler.logStruct(topic=f"updateCategory: categoryId: {category_id}, update category success",
                                          status_code=r.status,
                                          response_text=r.text)
                return media

        else:
            ## logging
            if bool(os.environ['DEBUG']) and logger:
                msg_handler.logStruct(level="ERROR",
                                      topic=f"updateCategory:  categoryId: {category_id}, update category error",
                                      status_code=r.status,
                                      response_text=r.text)
            return []

class Brand:
    @staticmethod
    def putUpdate(logger: object,
                  payload: dict,
                  brand_id: int,
                  connection: object) -> list:

        ## logging
        if bool(os.environ['DEBUG']):
            msg_handler = messageHandler(logger=logger, level="DEBUG",
                                         labels={'function': 'updateBrand', 'endpoint': '/Brand/{brand_id}'})
            msg_handler.logStruct(topic=f"updateBrand: brandId: {brand_id}, start updating brand.", data=payload)

        ## process request from connection pool
        encoded_data = json.dumps(payload).encode('utf-8')
        r = connection.request(method="PUT",
                               url=f"{os.environ['YOUR_API_URL']}/Brand/{brand_id}",
                               body=encoded_data,
                               headers={'Authorization': 'Bearer ' + os.environ["YOUR_API_TOKEN"],
                                        'Content-Type': 'application/json'})
        status_code = r.status

        if status_code == 200:
            resp_body = json.loads(r.data.decode('utf-8'))
            resp_data = resp_body.get('data')
            if resp_data:
                media = resp_data.get('duplicates', [])

                ## logging
                if bool(os.environ['DEBUG']):
                    msg_handler.logStruct(topic=f"updateBrand: brandId: {brand_id}, update brand success",
                                          status_code=r.status,
                                          response_text=r.text)
                return media

        else:
            ## logging
            if bool(os.environ['DEBUG']):
                msg_handler.logStruct(level="ERROR",
                                      topic=f"updateBrand:  brandId: {brand_id}, update brand error",
                                      status_code=r.status,
                                      response_text=r.text)
            return []

class Attribute:
    @staticmethod
    def putUpdate(logger: object,
                  payload: dict,
                  attribute_id: int,
                  connection: object) -> list:

        ## logging
        if bool(os.environ['DEBUG']):
            msg_handler = messageHandler(logger=logger, level="DEBUG",
                                         labels={'function': 'updateAttribute', 'endpoint': '/Attribute/{attributeId}'})
            msg_handler.logStruct(topic=f"updateAttribute: attributeId: {attribute_id}, start updating attribute.",
                                  data=payload)

        ## process request from connection pool
        encoded_data = json.dumps(payload).encode('utf-8')
        r = connection.request(method="PUT",
                               url=f"{os.environ['YOUR_API_URL']}/Attribute/{attribute_id}",
                               body=encoded_data,
                               headers={'Authorization': 'Bearer ' + os.environ["YOUR_API_TOKEN"],
                                        'Content-Type': 'application/json'})
        status_code = r.status

        if status_code == 200:
            resp_body = json.loads(r.data.decode('utf-8'))
            resp_data = resp_body.get('data')
            if resp_data:
                media = resp_data.get('duplicates', [])

                ## logging
                if bool(os.environ['DEBUG']):
                    msg_handler.logStruct(topic=f"updateAttribute: attributeId: {attribute_id}, update attribute success",
                                          status_code=status_code,
                                          response_text=r.data)
                return media

        else:
            ## logging
            if bool(os.environ['DEBUG']):
                msg_handler.logStruct(level="ERROR",
                                      topic=f"updateAttribute:  attributeId: {attribute_id}, update attribute error",
                                      status_code=status_code,
                                      response_text=r.data)
            return []

    @staticmethod
    def putUpdateValueUnit(logger: object,
                          payload: dict,
                          unitId: int,
                          connection: object) -> bool:

        ## logging
        if bool(os.environ['DEBUG']):
            msg_handler = messageHandler(logger=logger, level="DEBUG",
                                         labels={'function': 'updateAttribute', 'endpoint': '/AttributeValueUnit/{unitId}'})
            msg_handler.logStruct(topic=f"putUpdateValueUnit: valueUnit: {unitId}, start updating attribute.",
                                  data=payload)

        ## process request from connection pool
        encoded_data = json.dumps(payload).encode('utf-8')
        r = connection.request(method="PUT",
                               url=f"{os.environ['YOUR_API_URL']}/AttributeValueUnit/{unitId}",
                               body=encoded_data,
                               headers={'Authorization': 'Bearer ' + os.environ["YOUR_API_TOKEN"],
                                        'Content-Type': 'application/json'})

        if r.status == 200:
            ## logging
            if bool(os.environ['DEBUG']):
                msg_handler.logStruct(topic=f"putUpdateValueUnit: valueUnit: {unitId}, update attribute success",
                                      status_code=r.status,
                                      response_text=r.data)
            return True

        else:
            ## logging
            if bool(os.environ['DEBUG']):
                msg_handler.logStruct(level="ERROR",
                                      topic=f"putUpdateValueUnit:  valueUnit: {unitId}, update attribute error",
                                      status_code=r.status,
                                      response_text=r.data)
            return False

class Product:
    @staticmethod
    def putUpdate(logger: object,
                  productId: int,
                  payload: dict,
                  environment: str = "production",
                  additional_labels: dict = {},
                  connection: object = None) -> list:

        ## logging
        if bool(os.environ['DEBUG']):
            labels = {'function': 'updateProduct', 'endpoint': '/Product/{productId}'}
            if additional_labels:
                labels.update(additional_labels)
            msg_handler = messageHandler(logger=logger, level="DEBUG",
                                         labels=labels)
            msg_handler.logStruct(topic=f"updateProduct: update product",
                                  data=payload)

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

                ## logging
                if bool(os.environ['DEBUG']):
                    msg_handler.logStruct(topic=f"updateProduct: productId: {productId}, update product success",
                                          status_code=response_code,
                                          response_text=response_text)
                return media

        else:
            ## logging
            if bool(os.environ['DEBUG']):
                msg_handler.logStruct(level="ERROR",
                                      topic=f"updateProduct:  productId: {productId}, update product error",
                                      status_code=response_code,
                                      response_text=response_text)
            return []

class Series:
    @staticmethod
    def putUpdate(logger: object,
                  seriesId: int,
                  payload: dict,
                  connection: object,
                  additional_labels: dict = {}) -> bool:

        ## logging
        if bool(os.environ['DEBUG']):
            labels = {'function': 'updateSeries', 'endpoint': '/Series/{seriesId}'}
            if additional_labels:
                labels.update(additional_labels)
            msg_handler = messageHandler(logger=logger, level="DEBUG",
                                         labels=labels)
            msg_handler.logStruct(topic=f"updateSeries: update series",
                                  data=payload)

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
            ## logging
            if bool(os.environ['DEBUG']):
                msg_handler.logStruct(topic=f"updateSeries: seriesId: {seriesId}, update series success",
                                      status_code=response_code,
                                      response_text=response_text)

            return True

        else:
            ## logging
            if bool(os.environ['DEBUG']):
                msg_handler.logStruct(level="ERROR",
                                      topic=f"updateSeries:  seriesId: {seriesId}, update series error",
                                      status_code=response_code,
                                      response_text=response_text)
            return False