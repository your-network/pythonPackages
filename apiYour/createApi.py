import os
import requests
import json
from datetime import datetime
from loggingYour.messageHandler import messageHandler

class Brand:
    @staticmethod
    def create(logger: object,
               connection: object,
               data: dict) -> int:

        brand_id = None

        ## logging
        if bool(os.environ['DEBUG']):
            start_time = datetime.now()
            msg_handler = messageHandler(logger=logger, level="DEBUG",
                                         labels={'function': 'createBrand',
                                                 'endpoint': '/Brand'})
            msg_handler.logStruct(topic=f"createBrand: start create brand.\n start time: {start_time}",
                                  data=data,
                                  level="DEBUG")

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

            if success:
                brand_id = resp_data['id']

                ## logging
                if bool(os.environ['DEBUG']):
                    msg_handler.logStruct(topic=f"createBrand: finished create brand. brand id: {brand_id}",
                                          status_code=status_code,
                                          response_text=resp_data,
                                          level="DEBUG")

            elif code == 11:
                brand_id = resp_data.get('id')

                ## logging
                if bool(os.environ['DEBUG']):
                    msg_handler.logStruct(topic=f"createBrand: brand already existed, cat_id: {brand_id}",
                                          status_code=status_code,
                                          response_text=resp_data,
                                          level="DEBUG")

            else:
                ## logging
                if bool(os.environ['DEBUG']):
                    msg_handler.logStruct(topic=f"createBrand: no response data",
                                          status_code=status_code,
                                          response_text=resp_data,
                                          level="WARNING")

        else:
            ## logging
            msg_handler.logStruct(
                level="ERROR",
                topic=f"createBrand: error create brand",
                status_code=status_code,
                response_text=resp_data)

        ## logging
        if bool(os.environ['DEBUG']):
            msg_handler.logStruct(topic=f"createBrand: Api brand create finished,\n processing time: {datetime.now() - start_time}")

        return brand_id

class Category:
    @staticmethod
    def create(payload: dict,
               logger: object,
               connection: object,
               additional_labels: dict = None) -> int:

        cat_id = None

        ## logging
        if bool(os.environ['DEBUG']):
            labels = {'function': 'createCategory', 'endpoint': '/Category/'}
            if additional_labels:
                labels.update(additional_labels)

            msg_handler = messageHandler(logger=logger, level="DEBUG", labels=labels)
            start_time = datetime.now()
            msg_handler.logStruct(topic=f"createCategory: start create category. start time: {start_time}", data=payload)

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

            if success:
                cat_id = resp_data.get('id')

                ## logging
                if bool(os.environ['DEBUG']):
                    msg_handler.logStruct(topic=f"createCategory: category created finished, cat_id: {cat_id}",
                                          status_code=status_code,
                                          response_text=resp_data)

            elif code == 11:
                cat_id = resp_data.get('id')
                ## logging
                if bool(os.environ['DEBUG']):
                    msg_handler.logStruct(topic=f"createCategory: category already existed, cat_id: {cat_id}",
                                          status_code=status_code,
                                          response_text=resp_data)

            else:
                ## logging
                if bool(os.environ['DEBUG']):
                    msg_handler.logStruct(topic=f"createCategory: no response data",
                                          status_code=status_code,
                                          response_text=resp_data,
                                          level="WARNING")

        else:
            ## logging
            if bool(os.environ['DEBUG']):
                msg_handler.logStruct(level="ERROR",
                               topic="createCategory: Error create category",
                               status_code=status_code,
                               response_text=resp_data)

        return cat_id

class Product:
    @staticmethod
    def createBulk(logger: object,
                  data_bulk: list,
                  labels: dict = {}):

        ## logging
        if bool(os.environ['DEBUG']):
            log_labels = {'function': 'createProductBulk', 'endpoint': '/Product/CreateOrUpdateBulk'}
            if labels:
                log_labels.update(labels)
            start_time = datetime.now()
            msg_handler = messageHandler(logger=logger, level="DEBUG",
                                         labels=log_labels)
            msg_handler.logStruct(f"createProductBulk: start process product bulk insert",
                                  data={"list": data_bulk})

        ## request
        r = requests.post(url=f"{os.environ['YOUR_API_URL']}/Product/CreateOrUpdateBulk",
                          json=data_bulk,
                          headers={'Authorization': 'Bearer ' + os.environ["YOUR_API_TOKEN"]})

        if r.status_code == 200:
            resp_data = json.loads(r.text)
            product_bulk_response = resp_data

            ## logging
            if bool(os.environ['DEBUG']):
                msg_handler.logStruct(topic=f"createProductBulk: Success in product bulk insert. Number products",
                               status_code=r.status_code,
                               response_text=r.text)

        else:
            ## logging
            if bool(os.environ['DEBUG']):
                msg_handler.logStruct(level="ERROR",
                               topic="createProductBulk: Error in product bulk insert",
                               status_code=r.status_code,
                               response_text=r.text)

            product_bulk_response = None

            ## logging
            if bool(os.environ['DEBUG']):
                msg_handler.logStruct(topic=f"createProductBulk: Api product bulk insert finished, processing time: {datetime.now() - start_time}",
                           status_code=r.status_code,
                           response_text=r.text)


        return product_bulk_response

    @staticmethod
    def createQueue(logger: object,
                   data_bulk: list,
                   additional_labels: dict = {}):

        ## logging
        if bool(os.environ['DEBUG']):
            start_time = datetime.now()
            labels = {'function': 'createProductQueue', 'endpoint': "/Product/QueueForCreateBulk"}
            if additional_labels:
                labels.update(additional_labels)

            msg_handler = messageHandler(logger=logger,
                                         level="DEBUG",
                                         labels=labels)
            msg_handler.logStruct(topic=f"createProductQueue: process product queue",
                                  data=data_bulk)

        ## request
        r = requests.post(url=f"{os.environ['YOUR_API_URL']}/Product/QueueForCreateBulk",
                         json=data_bulk,
                         headers={'Authorization': 'Bearer ' + os.environ["YOUR_API_TOKEN"]})

        if r.status_code == 200:
            resp_data = json.loads(r.text)

            ## logging
            if bool(os.environ['DEBUG']):
                msg_handler.logStruct(topic=f"createProductQueue: Success in product queue insert",
                               status_code=r.status_code,
                               response_text=r.text)
        else:
            resp_data = None
            ## logging
            if bool(os.environ['DEBUG']):
                msg_handler.logStruct(topic="createProductQueue: Error product bulk insert",
                                      level="WARNING",
                                      data=data_bulk,
                               status_code=r.status_code,
                               response_text=r.text)

        ## logging
        if bool(os.environ['DEBUG']):
            msg_handler.logStruct(topic=f"createProductBulk: Api product queue insert finished, processing time: {datetime.now()-start_time}")

        return resp_data

class Series:
    @staticmethod
    def create(logger: object,
                 data=dict) -> int:

        ## logging
        if bool(os.environ['DEBUG']):
            start_time = datetime.now()
            msg_handler = messageHandler(logger=logger, level="DEBUG",
                                         labels={'function': 'createSeries',
                                                 'endpoint': '/Series'})
            msg_handler.logStruct(topic=f"createSeries: start create serie.\n start time: {start_time}",
                                  data=data)

        serie_id = None

        ## request
        r = requests.post(url=f"{os.environ['YOUR_API_URL']}/Series",
                          json=data,
                          headers={'Authorization': 'Bearer ' + os.environ["YOUR_API_TOKEN"]})

        if r.status_code == 200:
            resp_data = json.loads(r.text)
            serie_id = resp_data['data']['id']

            ## logging
            if bool(os.environ['DEBUG']):
                msg_handler.logStruct(
                    topic=f"createSeries: finished create serie. serie id: {serie_id}",
                    status_code=r.status_code,
                    response_text=r.text)

        else:
            ## logging
            if bool(os.environ['DEBUG']):
                msg_handler.logStruct(
                    level="ERROR",
                    topic=f"createSeries: error create serie",
                    status_code=r.status_code,
                    response_text=r.text)

        ## logging
        if bool(os.environ['DEBUG']):
            msg_handler.logStruct(topic=f"createSeries: Api create serie finished,\n processing time: {datetime.now() - start_time}")

        return serie_id

class Relations:

    @staticmethod
    def createCategoryCategoryRelation(logger: object,
                                        data: dict,
                                        connection: object,
                                        additional_labels: dict = None) -> bool:
        ## logging
        if bool(os.environ['DEBUG']):
            labels = {'function': 'createCategoryCategoryRelation',
                      'endpoint': '/Relation/CreateCategoryCategory'}
            if additional_labels:
                labels.update(additional_labels)
            msg_handler = messageHandler(logger=logger, level="DEBUG",
                                         labels=labels)
            msg_handler.logStruct(topic=f"createCategoryCategoryRelation: Start create category category relation",
                                  data=data)

        ## process request from connection pool
        encoded_data = json.dumps(data).encode('utf-8')
        r = connection.request(method="POST",
                               url=f"{os.environ['YOUR_API_URL']}/Relation/CreateCategoryCategory",
                               body=encoded_data,
                               headers={'Authorization': 'Bearer ' + os.environ["YOUR_API_TOKEN"],
                                        'Content-Type': 'application/json'})

        response_code = r.status
        response_text = r.data

        if response_code == 200:
            ## logging
            if bool(os.environ['DEBUG']):
                msg_handler.logStruct(
                    topic=f"createCategoryCategoryRelation: finished create relation category category",
                    status_code=response_code,
                    response_text=response_text)
                return True

        else:
            ## logging
            if bool(os.environ['DEBUG']):
                msg_handler.logStruct(
                    level="WARNING",
                    topic=f"createCategoryCategoryRelation: error create relation category category",
                    status_code=response_code,
                    response_text=response_text)
                return False

    @staticmethod
    def createBrandCategoryRelation(logger: object,
                                    data: dict,
                                    connection: object,
                                    additional_labels: dict = None) -> bool:

        ## logging
        if bool(os.environ['DEBUG']):
            labels = {'function': 'createBrandCategoryRelation',
                                                 'endpoint': '/Relation/CreateBrandCategory'}
            if additional_labels:
                labels.update(additional_labels)

            msg_handler = messageHandler(logger=logger, level="DEBUG",
                                         labels=labels)
            msg_handler.logStruct(topic=f"createBrandCategoryRelation: Start create brand category relation",
                                  data=data)

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
            if bool(os.environ['DEBUG']):
                msg_handler.logStruct(
                    topic=f"createBrandCategoryRelation: finished create relation brand category",
                    status_code=response_code,
                    response_text=response_text)
            return True

        else:
            ## logging
            if bool(os.environ['DEBUG']):
                msg_handler.logStruct(
                    level="ERROR",
                    topic=f"createBrandCategoryRelation: error create relation brand category",
                    status_code=response_code,
                    response_text=response_text)
            return False

    @staticmethod
    def createCategoryAttributeRelation(logger: object,
                                        data: dict,
                                        connection: object,
                                        additional_labels: dict = None) -> bool:
        ## logging
        if bool(os.environ['DEBUG']):
            labels = {'function': 'createCategoryAttributeRelation',
                                                 'endpoint': '/Relation/CreateAttributeCategory'}
            if additional_labels:
                labels.update(additional_labels)

            msg_handler = messageHandler(logger=logger, level="DEBUG",
                                         labels=labels)

            msg_handler.logStruct(
                topic=f"createCategoryAttributeRelation: Start create category attribute relation",
                data=data)

        ## process request from connection pool
        encoded_data = json.dumps(data).encode('utf-8')
        r = connection.request(method="POST",
                               url=f"{os.environ['YOUR_API_URL']}/Relation/CreateAttributeCategory",
                               body=encoded_data,
                               headers={'Authorization': 'Bearer ' + os.environ["YOUR_API_TOKEN"],
                                        'Content-Type': 'application/json'})

        response_code = r.status
        response_text = r.data

        if response_code == 200:
            ## logging
            if bool(os.environ['DEBUG']):
                msg_handler.logStruct(
                    topic=f"createCategoryAttributeRelation: finished create relation category attribute",
                    status_code=response_code,
                    response_text=response_text)
            return True

        else:
            ## logging
            if bool(os.environ['DEBUG']):
                msg_handler.logStruct(
                    level="WARNING",
                    topic=f"createCategoryAttributeRelation: error create relation category attribute",
                    status_code=response_code,
                    response_text=response_text)
            return False

    @staticmethod
    def createProductProductRelation(logger: object,
                                     data: dict,
                                     connection: object) -> bool:

        ## logging
        if bool(os.environ['DEBUG']):
            msg_handler = messageHandler(logger=logger, level="DEBUG",
                                         labels={'function': 'createProductProductRelation',
                                                 'endpoint': '/Relation/CreateProductProduct'})
            msg_handler.logStruct(topic=f"createProductProductRelation: Start create product product relation,\n start time: {datetime.now()}",
                                  data=data)

        ## process request from connection pool
        encoded_data = json.dumps(data).encode('utf-8')
        r = connection.request(method="POST",
                               url=f"{os.environ['YOUR_API_URL']}/Relation/CreateProductProduct",
                               body=encoded_data,
                               headers={'Authorization': 'Bearer ' + os.environ["YOUR_API_TOKEN"],
                                        'Content-Type': 'application/json'})

        response_code = r.status
        response_text = r.data

        if response_code == 200:
            ## logging
            if bool(os.environ['DEBUG']):
                msg_handler.logStruct(
                    topic=f"createProductProductRelation: finished create relation product product",
                    status_code=response_code,
                    response_text=response_text)
            return True

        else:
            ## logging
            if bool(os.environ['DEBUG']):
                msg_handler.logStruct(
                    level="ERROR",
                    topic=f"createProductProductRelation: error create relation product product",
                    status_code=response_code,
                    response_text=response_text)
            return False

    @staticmethod
    def createCategoryProductRelation(logger: object,
                                      data: dict,
                                      connection: object) -> bool:

        ## logging
        if bool(os.environ['DEBUG']):
            msg_handler = messageHandler(logger=logger, level="DEBUG",
                                         labels={'function': 'createCategoryProductRelation',
                                                 'endpoint': '/Relation/CreateCategoryProduct'})
            msg_handler.logStruct(topic=f"createCategoryProductRelation: Start create category product relation,\n start time: {datetime.now()}", data=data)

        ## process request from connection pool
        encoded_data = json.dumps(data).encode('utf-8')
        r = connection.request(method="POST",
                               url=f"{os.environ['YOUR_API_URL']}/Relation/CreateCategoryProduct",
                               body=encoded_data,
                               headers={'Authorization': 'Bearer ' + os.environ["YOUR_API_TOKEN"],
                                        'Content-Type': 'application/json'})

        response_code = r.status
        response_text = r.data

        if response_code == 200:
            ## logging
            if bool(os.environ['DEBUG']):
                msg_handler.logStruct(
                    topic=f"createCategoryProductRelation: finished create relation category product",
                    status_code=response_code,
                    response_text=response_text)
            return True

        else:
            ## logging
            if bool(os.environ['DEBUG']):
                msg_handler.logStruct(
                    level="ERROR",
                    topic=f"createCategoryProductRelation: error create relation category product",
                    status_code=response_code,
                    response_text=response_text)
            return False

class Attributes:

    @staticmethod
    def createAttributeUnit(logger: object,
                            data: dict,
                            connection: object) -> int:

        ## logging
        if bool(os.environ['DEBUG']):
            start_time = datetime.now()
            msg_handler = messageHandler(logger=logger, level="DEBUG",
                                         labels={'function': 'createAttributeUnit',
                                                 'endpoint': '/Attribute/CreateOrUpdateAttributeTypeUnit'})
            msg_handler.logStruct(topic=f"createAttributeUnit: start create attribute unit. Start time: {start_time}",
                                  data=data)

        unit_id = None

        ## process request from connection pool
        encoded_data = json.dumps(data).encode('utf-8')
        r = connection.request(method="POST",
                               url=f"{os.environ['YOUR_API_URL']}/Attribute/CreateOrUpdateAttributeTypeUnit",
                               body=encoded_data,
                               headers={'Authorization': 'Bearer ' + os.environ["YOUR_API_TOKEN"],
                                        'Content-Type': 'application/json'})
        status_code = r.status
        resp_data = r.data

        if status_code == 200:
            resp_data = json.loads(resp_data.decode('utf-8'))
            unit_id = resp_data['data']['id']

            ## logging
            if bool(os.environ['DEBUG']):
                msg_handler.logStruct(topic=f"createAttributeUnit: create attribute unit success. Unit_id: {unit_id}",
                                      status_code=status_code,
                                      response_text=resp_data)

        else:
            ## logging
            if bool(os.environ['DEBUG']):
                msg_handler.logStruct(topic="createAttributeUnit: Error attribute unit insert",
                                      level="ERROR",
                                      status_code=status_code,
                                      response_text=resp_data)

        ## logging
        if bool(os.environ['DEBUG']):
            msg_handler.logStruct(
                topic=f"createAttributeUnit: Api attribute unit insert finished, processing time: {datetime.now() - start_time}")

        return unit_id

    @staticmethod
    def createAttributeType(logger: object,
                            data: dict,
                            connection: object) -> int:

        ## logging
        if bool(os.environ['DEBUG']):
            start_time = datetime.now()
            msg_handler = messageHandler(logger=logger, level="DEBUG",
                                         labels={'function': 'CreateOrUpdateAttributeType',
                                                 'endpoint': '/Attribute/CreateOrUpdateAttributeType'})
            msg_handler.logStruct(topic=f"createAttributeType: start create attribute type.\n start time: {start_time}",
                                  data=data)

        attribute_type_id = None

        ## process request from connection pool
        encoded_data = json.dumps(data).encode('utf-8')
        r = connection.request(method="POST",
                               url=f"{os.environ['YOUR_API_URL']}/Attribute/CreateOrUpdateAttributeType",
                               body=encoded_data,
                               headers={'Authorization': 'Bearer ' + os.environ["YOUR_API_TOKEN"],
                                        'Content-Type': 'application/json'})
        status_code = r.status
        resp_data = r.data

        if status_code == 200:
            resp_data = json.loads(resp_data.decode('utf-8'))
            attribute_type_id = resp_data['data']['id']

            ## logging
            if bool(os.environ['DEBUG']):
                msg_handler.logStruct(
                    topic=f"createAttributeType: finished create attribute type. attribute id type: {attribute_type_id}",
                    status_code=status_code,
                    response_text=resp_data)

        else:
            ## logging
            if bool(os.environ['DEBUG']):
                msg_handler.logStruct(
                    level="ERROR",
                    topic=f"createAttributeType: error create attribute type",
                    status_code=status_code,
                    response_text=resp_data)

        ## logging
        if bool(os.environ['DEBUG']):
            msg_handler.logStruct(
                topic=f"createAttributeUnit: Api attribute unit create finished,\n processing time: {datetime.now() - start_time}")

        return attribute_type_id

    @staticmethod
    def createAttribute(logger: object,
                        data: dict,
                        connection: object) -> int:

        ## logging
        if bool(os.environ['DEBUG']):
            start_time = datetime.now()
            msg_handler = messageHandler(logger=logger, level="DEBUG",
                                         labels={'function': 'createAttribute',
                                                 'endpoint': '/Attribute/CreateOrUpdate'})
            msg_handler.logStruct(topic=f"createAttribute: start create attribute.\n start time: {start_time}",
                                  data=data)

        attribute_id = None

        ## process request from connection pool
        encoded_data = json.dumps(data).encode('utf-8')
        r = connection.request(method="POST",
                               url=f"{os.environ['YOUR_API_URL']}/Attribute",
                               body=encoded_data,
                               headers={'Authorization': 'Bearer ' + os.environ["YOUR_API_TOKEN"],
                                        'Content-Type': 'application/json'})
        status_code = r.status
        resp_data = r.data

        allowed_codes = [200, 400]

        if status_code in allowed_codes:
            resp_body = json.loads(resp_data.decode('utf-8'))
            resp_data = resp_body.get('data')
            success = resp_body.get('success')
            code = resp_body.get('code')

            if success:
                attribute_id = resp_data['id']

                ## logging
                if bool(os.environ['DEBUG']):
                    msg_handler.logStruct(
                        topic=f"createAttribute: finished create attribute type. attribute id: {attribute_id}",
                        status_code=status_code,
                        response_text=resp_data,
                        level="DEBUG")

            elif code == 11:
                attribute_id = resp_data.get('id')

                ## logging
                if bool(os.environ['DEBUG']):
                    msg_handler.logStruct(topic=f"createAttribute: attribute already existed, attribute_id: {attribute_id}",
                                          status_code=status_code,
                                          response_text=resp_data,
                                          level="DEBUG")

            else:
                ## logging
                if bool(os.environ['DEBUG']):
                    msg_handler.logStruct(topic=f"createAttribute: no response data",
                                          status_code=status_code,
                                          response_text=resp_data,
                                          level="WARNING")
        else:
            ## logging
            if bool(os.environ['DEBUG']):
                msg_handler.logStruct(topic=f"createAttribute: status code not {allowed_codes}",
                                      status_code=status_code,
                                      response_text=resp_data,
                                      level="ERROR")

        return attribute_id

    @staticmethod
    def createValueUnit(logger: object,
                         data: dict,
                         connection: object,
                         additional_labels: dict = None) -> bool:
        ## logging
        labels = {'function': 'createAttributeValueUnit',
                  'endpoint': '/AttributeValueUnit'}
        if additional_labels:
            labels.update(additional_labels)
        msg_handler = messageHandler(logger=logger, level="DEBUG",
                                     labels=labels)
        msg_handler.logStruct(topic=f"createAttributeValueUnit: create attribute value unit",
                              data=data)

        ## process request from connection pool
        encoded_data = json.dumps(data).encode('utf-8')
        r = connection.request(method="POST",
                               url=f"{os.environ['YOUR_API_URL']}/AttributeValueUnit",
                               body=encoded_data,
                               headers={'Authorization': 'Bearer ' + os.environ["YOUR_API_TOKEN"],
                                        'Content-Type': 'application/json'})
        status_code = r.status
        resp_data = r.data

        allowed_codes = [200, 400]

        if status_code in allowed_codes:
            resp_body = json.loads(resp_data.decode('utf-8'))
            if resp_body.get('data'):
                unit_id = resp_body['data'].get('id')
                ## logging
                if bool(os.environ['DEBUG']):
                    msg_handler.logStruct(
                        topic=f"createAttributeValueUnit: finished creating",
                        status_code=status_code,
                        response_text=resp_data)
                return unit_id
            else:
                ## logging
                if bool(os.environ['DEBUG']):
                    msg_handler.logStruct(
                        topic=f"createAttributeValueUnit: no data returned",
                        status_code=status_code,
                        response_text=resp_body)
                return None

        else:
            ## logging
            if bool(os.environ['DEBUG']):
                msg_handler.logStruct(
                    level="WARNING",
                    topic=f"createAttributeValueUnit: error creating",
                    status_code=status_code,
                    response_text=resp_data)
            return None
