import json
import os
from datetime import datetime
import rootpath
from cacheYour.client import RedisClient

## directory
abs_path = rootpath.detect()

class AttributeIndex:
    def __init__(self, client: RedisClient):
        self.client = client

    def checkAttributeStatusCache(self,
                                  index_attributes: dict):
        while True:
            status = self.client.conn.get(f"attribute.index.cache")
            if status and bool(status):
                return True
            else:
                self.processIndexAttributeCache(index_attributes=index_attributes)
                return True

    def processIndexAttributeCache(self,
                                   index_attributes: dict):
        from cacheYour.appVariables import connectionPool, ACTIVE_LANGUAGES
        from apiYour.getApi import Category, Attributes
        from cacheYour.attributes.topicPackage import attributeLogger
        from helpersYour.functions import remove_dic_key

        ## logging
        start_time = datetime.now()
        if os.environ.get('DEBUG') == 'DEBUG':
            log_message = {
                "topic": f"saveAttributeCategoryCache: start saving index data",
                "message": {}}
            attributeLogger.createDebugLog(message=log_message)

        ## get all brands
        categories = Category.getAll(includeServiceCategories=False,
                                     connection=connectionPool)

        ## process category attributes
        for category in categories:
            if category['public']:
                attributes = Attributes.getAll(categoryId=category['id'],
                                               connection=connectionPool)

                for attribute in attributes:
                    if attribute['searchable']:
                        attr_dic = remove_dic_key(dic=attribute, keys=['categoryRelations'])
                        self.processAttributeLanguages(languages=ACTIVE_LANGUAGES,
                                                       categoryId=category['id'],
                                                       mapped_attributes=index_attributes,
                                                       attribute=attr_dic)

        self.client.conn.set(f"attribute.index.cache", "True", ex=172800)

        ## logging
        if os.environ.get('DEBUG') == 'DEBUG':
            log_message = {
                "topic": f"saveAttributeCategoryCache: finished saving index data",
                "message": {"processingTime": str(datetime.now() - start_time)}}
            attributeLogger.createDebugLog(message=log_message)

    def processAttributeLanguages(self,
                                  languages: list,
                                  attribute: dict,
                                  categoryId: int,
                                  mapped_attributes: dict) -> None:
        for language in languages:
            ## mapped type attribute data
            mapped_type = None
            if mapped_attributes[language].get(str(attribute['id'])):
                mapped_type = mapped_attributes[language].get(str(attribute['id']))['type']

            if attribute.get('translations'):
                if attribute['translations'].get(language):
                    name = attribute['translations'][language]['name']

                    ## save attribute data
                    attribute.update({'mapped_type': mapped_type,
                                      'name': name})
                    self.saveIndexAttributeDetails(attributeId=attribute['id'],
                                                   categoryId=categoryId,
                                                   language=language,
                                                   data=attribute)
                    continue

            ## fallback
            attribute.update({'mapped_type': mapped_type,
                              'name': attribute['name']})
            self.saveIndexAttributeDetails(attributeId=attribute['id'],
                                           categoryId=categoryId,
                                           language=language,
                                           data=attribute)

    def saveIndexAttributeDetails(self,
                                  attributeId: int,
                                  categoryId: int,
                                  language: str,
                                  data: dict):
        key = f"attribute.index.{attributeId}.{categoryId}.{language}"
        self.client.conn.set(key, json.dumps(data))

    ## GET METHODS
    @staticmethod
    def getIndexAttributeDetails(client: RedisClient,
                                 attributeId: int,
                                 categoryId: int,
                                 language: str):
        search_key = f"attribute.index.{attributeId}.{categoryId}.{language}"
        attribute_details = client.conn.get(search_key)
        if attribute_details:
            return json.loads(attribute_details)

        else:
            return None
