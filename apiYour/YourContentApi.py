import requests
import json
from datetime import datetime

class Api:
    api_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJodHRwOi8vc2NoZW1hcy54bWxzb2FwLm9yZy93cy8yMDA1LzA1L2lkZW50aXR5L2NsYWltcy9uYW1lIjoidGhpam1lbkB5b3VyLmlvIiwianRpIjoiNDE3NjdmODQtNGQ3NS00NDA2LTljODgtZjZiNjdkOTc3MDQ4IiwiaHR0cDovL3NjaGVtYXMubWljcm9zb2Z0LmNvbS93cy8yMDA4LzA2L2lkZW50aXR5L2NsYWltcy9yb2xlIjoiU3VwZXJBZG1pbiIsImV4cCI6MTY4MjUwNTMwMywiaXNzIjoiaHR0cDovL2xvY2FsaG9zdDo1MDAwIiwiYXVkIjoiaHR0cDovL2xvY2FsaG9zdDo1MDAwIn0.Eu7uIM-ECgMKuHjjoSOOBX2QC_SaDkHjsSOVCTwm7TU"
    header = {'Authorization': 'Bearer ' + api_token}

    def UpdateCategory(self, payload):
        r = requests.post('https://api.yourcontent.io/Category/CreateOrUpdate',
                          json=payload,
                          headers=self.header)
        if r.status_code == 200:
            print(f"Update Call Succes, category id: {payload.get('categoryId')}")
            return 200
        else:
            print(f"Update Call failed. Response code: {r.status_code}, text: {r.text}")
            return r.status_code

    def CreateCategory(self, payload):
        r = requests.post('https://api.yourcontent.io/Category/CreateOrUpdate',
                          json=payload,
                          headers=self.header)
        if r.status_code == 200:
            resp_data = json.loads(r.text).get('data')
            if resp_data:
                cat_id = resp_data.get('id')
                print(f"Call Succes, response category id: {cat_id}")
                return cat_id
            else:
                print(f"Call Succes but no response category id")
                return None
        else:
            print(f"Call failed. Response code: {r.status_code}, text: {r.text}")
            return None

    def GetAllCategories(self):
        start_time = datetime.now()
        print(f"YourApi get all categories. Start time: {start_time}")
        category_list = []
        page = 1
        pagination = True
        while pagination:
            r = requests.get(f"https://api.yourcontent.io/Category/GetAll?resultsPerPage=100&page={page}",
                             headers=self.header)
            if r.status_code == 200:
                resp_data = json.loads(r.text)
                categories = resp_data.get('data')
                if len(categories) > 0:
                    category_list = category_list + categories
                    print(
                        f"Call Success page: {page}, number of categories added to the list: {len(categories)}, total: {len(category_list)}")
                    page += 1
                else:
                    break
        end_time = datetime.now()
        print(f"Extraction finished, processing time: {end_time - start_time}")
        return category_list

    def createProductBulk(self,data_bulk):
        start_time = datetime.now()
        print(f"YourApi process product bulk. Start time: {start_time}")
        r = requests.get(f"https://api.yourcontent.io/Product/CreateOrUpdateBulk",
                         json=data_bulk,
                         headers=self.header)
        print(f"Bulk response: {r.text}")
        if r.status_code == 200:
            print(f"Success in product bulk insert. Number products: {len(data_bulk)}")
            resp_data = json.loads(r.text)
            product_bulk_response = resp_data['data']
        else:
            print(f"Error in product bulk insert. Response text: {r}")
            product_bulk_response = None

        end_time = datetime.now()
        print(f"Api product bulk insert finished, processing time: {end_time - start_time}")
        return product_bulk_response

    def createAttributeUnit(self,data):
        r = requests.post(f"https://api.yourcontent.io/Attribute/CreateOrUpdateAttributeTypeUnit",
                         json=data,
                         headers=self.header)
        # print(f"Attribute Unit create response: {r.content}")
        if r.status_code == 200:
            # print(f"Attribute Unit create Success")
            resp_data = json.loads(r.text)
            unit_id = resp_data['data']['id']
        else:
            print(f"Attribute Unit create Error."
                  f""
                  f"Data: {data},"
                  f""
                  f"Response text: {r.content}")
            unit_id = None
        return unit_id

    def createAttributeType(self,data):
        r = requests.post(f"https://api.yourcontent.io/Attribute/CreateOrUpdateAttributeType",
                         json=data,
                         headers=self.header)
        # print(f"Attribute Type create response: {r.content}")
        if r.status_code == 200:
            # print(f"Attribute Type create Success")
            resp_data = json.loads(r.text)
            attribute_type_id = resp_data['data']['id']
        else:
            print(f"Attribute Type create Error. Response text: {r.content}")
            attribute_type_id = None
        return attribute_type_id

    def createAttribute(self,data):
        r = requests.post(f"https://api.yourcontent.io/Attribute/CreateOrUpdate",
                         json=data,
                         headers=self.header)
        # print(f"Attribute create response: {r.content}")
        if r.status_code == 200:
            # print(f"Attribute create Success")
            resp_data = json.loads(r.text)
            attribute_id = resp_data['data']['id']
        else:
            print(f"Attribute create Error. Response text: {r.content}")
            attribute_id = None
        return attribute_id

    def getAllCategories(self):
        next_page = True
        page = 1
        categories = []
        while next_page:
            r = requests.get(f"https://api.yourcontent.io/Category/GetAll?resultsPerPage=100&page={page}",
                              headers=self.header)
            if r.status_code == 200:
                result = json.loads(r.text)
                data = result.get('data')
                if len(data) > 0:
                    categories = categories + data
                    page += 1
                else:
                    break
            else:
                print(f"Attribute create Error. Response text: {r.content}")
                break

        return categories

