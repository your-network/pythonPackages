import json
import os
import rootpath
## directory
abs_path = rootpath.detect()
from cacheYour.client import RedisClient

class AttributeCache:
    def __init__(self, client: RedisClient):
        self.client = client
    '''
        Attribute  Cache
    '''
    def checkAttributeStatusCache(self) -> bool:
        status = self.client.conn.get(f"attribute.cache")
        if status and bool(status):
            return True
        else:
            ## logging
            from cacheYour.attributes.topicPackage import attributeLogger
            if os.environ.get('DEBUG') == 'DEBUG':
                log_message = {"topic": f"checkAttributeStatusCache: status false so process",
                               "message": {}}
                attributeLogger.createDebugLog(message=log_message)

            self.processAttributeCache()
            return True

    def processAttributeCache(self):
        from cacheYour.attributes.topicPackage import attributeLogger
        from datetime import datetime
        from cacheYour.appVariables import connectionPool, ACTIVE_LANGUAGES
        from apiYour.getApi import Attributes
        from helpersYour.functions import remove_dic_key

        ## logging
        start_time = datetime.now()
        if os.environ.get('DEBUG') == 'DEBUG':
            log_message = {
                "topic": f"saveAttributeCache: start saving index data",
                "message": {}}
            attributeLogger.createDebugLog(message=log_message)

        attributes = Attributes.getAll(connection=connectionPool)

        for attribute in attributes:
            attr_dic = remove_dic_key(dic=attribute, keys=['categoryRelations'])
            self.processAttributeLanguages(languages=ACTIVE_LANGUAGES,
                                      attribute=attr_dic)

            ## saving external id lookup
            if attr_dic.get('externalId'):
                self.saveExternalAttributeId(externalId=int(attr_dic['externalId']),
                                        source=int(attr_dic['source']),
                                        attributeId=int(attr_dic['id']))

        self.client.conn.set(f"attribute.cache", "True", ex=172800)
        self.client.conn.set(f"attribute.short-term.cache", "True", ex=3000)

        ## logging
        if os.environ.get('DEBUG') == 'DEBUG':
            log_message = {
                "topic": f"saveAttributeCache: finished saving index data",
                "message": {"processingTime": str(datetime.now() - start_time)}}
            attributeLogger.createDebugLog(message=log_message)

    def processAttributeLanguages(self,
                                  languages: list,
                                  attribute: dict) -> None:
        for language in languages:
            if attribute.get('translations'):
                if attribute['translations'].get(language):
                    name = attribute['translations'][language]['name']

                    ## save attribute data
                    data = {**attribute, **{'name': name}}
                    self.saveAttributeDetails(attributeId=attribute['id'],
                                             language=language,
                                             data=data)
                    continue

            ## fallback
            data = {**attribute, **{'name': attribute['name']}}
            self.saveAttributeDetails(attributeId=attribute['id'],
                                     language=language,
                                     data=data)

    def saveAttributeDetails(self,
                             attributeId: int,
                             language: str,
                             data: dict):
        key = f"attribute.{attributeId}.{language}"
        self.client.conn.set(key, json.dumps(data))

    def saveExternalAttributeId(self,
                                externalId: int,
                                source: int,
                                attributeId: int):
        self.client.conn.set(f"externalAttributeId.{externalId}.{source}", str(attributeId))

    '''
        Attribute Value Unit Cache
    '''
    def checkAttributeValueUnitStatusCache(self) -> bool:
        status = self.client.conn.get(f"attributeValueUnit.cache")
        if status and bool(status):
            return True
        else:
            ## logging
            from cacheYour.attributes.topicPackage import attributeLogger
            if os.environ.get('DEBUG') == 'DEBUG':
                log_message = {"topic": f"checkattributeValueUnitStatusCache: status false so process",
                               "message": {}}
                attributeLogger.createDebugLog(message=log_message)

            self.processAttributeValueUnitCache()
            return True

    def processAttributeValueUnitCache(self):
        from cacheYour.attributes.topicPackage import attributeLogger
        from datetime import datetime
        from cacheYour.appVariables import connectionPool, ACTIVE_LANGUAGES
        from apiYour.getApi import Attributes

        ## logging
        start_time = datetime.now()
        if os.environ.get('DEBUG') == 'DEBUG':
            log_message = {
                "topic": f"saveAttributeValueUnitCache: start saving index data",
                "message": {}}
            attributeLogger.createDebugLog(message=log_message)

        attribute_units = Attributes.getValueUnits(connection=connectionPool)

        for unit in attribute_units:
            self.processAttributeValueUnitLanguages(languages=ACTIVE_LANGUAGES,
                                                    attributeValueUnit=unit)

            ## saving external id lookup
            if unit.get('externalId'):
                self.saveExternalAttributeValueUnitId(externalId=int(unit['externalId']),
                                                      source=2,
                                                      attributeValueUnitId=int(unit['id']))

        self.client.conn.set(f"attributeValueUnit.cache", "True", ex=172800)
        self.client.conn.set(f"attributeValueUnit.short-term.cache", "True", ex=3000)

        ## logging
        if os.environ.get('DEBUG') == 'DEBUG':
            log_message = {
                "topic": f"saveAttributeValueUnitCache: finished saving index data",
                "message": {"processingTime": str(datetime.now() - start_time)}}
            attributeLogger.createDebugLog(message=log_message)

    def processAttributeValueUnitLanguages(self,
                                           languages: list,
                                           attributeValueUnit: dict) -> None:
        from cacheYour.attributes.topicPackage import attributeLogger
        fallback_language = 'en'

        for language in languages:
            if attributeValueUnit.get('translations'):
                if attributeValueUnit['translations'].get(language):
                    name = attributeValueUnit['translations'][language]['name']
                    unit = attributeValueUnit['translations'][language]['unit']

                    ## save attribute data
                    data = {'name': name,
                            'unit': unit,
                            'externalId': attributeValueUnit['externalId']}
                    self.saveAttributeValueUnitDetails(attributeValueUnitId=attributeValueUnit['id'],
                                                       language=language,
                                                       data=data)
                    continue

                elif attributeValueUnit['translations'].get(fallback_language):
                    ## fallback
                    if os.environ.get('DEBUG') == 'DEBUG':
                        log_message = {
                            "topic": f"Error attribute value unit don't have translations for language: {language} "
                                     f"but for yes fallback language: {fallback_language}",
                            "data": attributeValueUnit}
                        attributeLogger.createDebugLog(message=log_message)

                    name = attributeValueUnit['translations'][fallback_language]['name']
                    unit = attributeValueUnit['translations'][fallback_language]['unit']

                    ## save attribute data
                    data = {'name': name,
                            'unit': unit,
                            'externalId': attributeValueUnit['externalId']}
                    self.saveAttributeValueUnitDetails(attributeValueUnitId=attributeValueUnit['id'],
                                                       language=language,
                                                       data=data)
                    continue

            ## fallback
            if os.environ.get('DEBUG') == 'DEBUG':
                log_message = {
                    "topic": f"Error attribute value unit don't have translations for language: {language} "
                             f"also not fallback language: {fallback_language}",
                    "data": attributeValueUnit}
                attributeLogger.createDebugLog(message=log_message)

            data = {'name': attributeValueUnit['name'],
                    'unit': "",
                    'externalId': attributeValueUnit['externalId']}
            self.saveAttributeValueUnitDetails(attributeValueUnitId=attributeValueUnit['id'],
                                               language=language,
                                               data=data)

    def saveAttributeValueUnitDetails(self,
                                      attributeValueUnitId: int,
                                      language: str,
                                      data: dict):
        key = f"attributeValueUnitId.{attributeValueUnitId}.{language}"
        self.client.conn.set(key, json.dumps(data))

    def saveExternalAttributeValueUnitId(self,
                                         externalId: int,
                                         source: int,
                                         attributeValueUnitId: int):
        self.client.conn.set(f"externalAttributeValueUnitId.{externalId}.{source}", str(attributeValueUnitId))

    ## GET METHODS
    @staticmethod
    def getAttributeDetails(client: RedisClient,
                            attributeId: int,
                            language: str):
        search_key = f"attribute.{attributeId}.{language}"
        attribute_details = client.conn.get(search_key)
        if attribute_details:
            return json.loads(attribute_details)

        else:
            ## logging
            from cacheYour.attributes.topicPackage import attributeLogger
            ## logging
            if os.environ.get('DEBUG') == 'DEBUG':
                log_message = {"topic": f"getAttributeDetails: key not found so "
                                        f"verify cache moment and if needed process cache",
                               "message": {"key": search_key}}
                attributeLogger.createDebugLog(message=log_message)

            ## short term cache check to fix looping on new category creation
            status = client.conn.get(f"attribute.short-term.cache")

            if status and bool(status):
                return {}

            else:
                cache = AttributeCache(client=client)
                cache.processAttributeCache()
                attribute_details = client.conn.get(search_key)
                return attribute_details

    @staticmethod
    def getInternalAttributeId(client: RedisClient,
                               externalId: int,
                               source: int):
        search_key = f"externalAttributeId.{externalId}.{source}"
        attribute_id = client.conn.get(search_key)
        if attribute_id:
            return int(attribute_id)

        else:
            ## logging
            from cacheYour.attributes.topicPackage import attributeLogger
            ## logging
            if os.environ.get('DEBUG') == 'DEBUG':
                log_message = {"topic": f"getInternalAttributeId: key not found so "
                                        f"verify cache moment and if needed process cache",
                               "message": {"key": search_key}}
                attributeLogger.createDebugLog(message=log_message)

            ## short term cache check to fix looping on new category creation
            status = client.conn.get(f"attribute.short-term.cache")

            if status and bool(status):
                return None

            else:
                ## process cache
                cache = AttributeCache(client=client)
                cache.processAttributeCache()
                attribute_id = client.conn.get(search_key)
                if attribute_id:
                    return int(attribute_id)
                else:
                    return None

    @staticmethod
    def getAttributeValueUnitDetails(client: RedisClient,
                                     attributeValueUnitId: int,
                                     language: str):
        search_key = f"attributeValueUnitId.{attributeValueUnitId}.{language}"
        attributeValueUnit_details = client.conn.get(search_key)
        if attributeValueUnit_details:
            return json.loads(attributeValueUnit_details)

        else:
            ## logging
            from cacheYour.attributes.topicPackage import attributeLogger
            ## logging
            if os.environ.get('DEBUG') == 'DEBUG':
                log_message = {"topic": f"getAttributeValueUnitDetails: key not found so "
                                        f"verify cache moment and if needed process cache",
                               "message": {"key": search_key}}
                attributeLogger.createDebugLog(message=log_message)

            ## short term cache check to fix looping on new category creation
            status = client.conn.get(f"attributeValueUnit.short-term.cache")

            if status and bool(status):
                return {}
            else:
                ## process cache
                cache = AttributeCache(client=client)
                cache.processAttributeValueUnitCache()
                attributeValueUnit_details = client.conn.get(search_key)
                return attributeValueUnit_details

    @staticmethod
    def getInternalAttributeValueUnitId(client: RedisClient,
                                        externalId: int,
                                        source: int):
        search_key = f"externalAttributeValueUnitId.{externalId}.{source}"
        attributeValueUnit_id = client.conn.get(search_key)
        if attributeValueUnit_id:
            return int(attributeValueUnit_id)

        else:
            ## logging
            from cacheYour.attributes.topicPackage import attributeLogger
            ## logging
            if os.environ.get('DEBUG') == 'DEBUG':
                log_message = {"topic": f"getInternalAttributeValueUnitId: key not found so "
                                        f"verify cache moment and if needed process cache",
                               "message": {"key": search_key}}
                attributeLogger.createDebugLog(message=log_message)

            ## short term cache check to fix looping on new category creation
            status = client.conn.get(f"attributeValueUnit.short-term.cache")

            if status and bool(status):
                return None
            else:
                ## process cache
                cache = AttributeCache(client=client)
                cache.processAttributeValueUnitCache()
                attributeValueUnit_id = client.conn.get(search_key)
                if attributeValueUnit_id:
                    return int(attributeValueUnit_id)
                else:
                    return None
