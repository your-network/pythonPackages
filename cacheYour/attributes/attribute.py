import json
import os
import rootpath
## directory
abs_path = rootpath.detect()
from redis import Redis
from cacheYour.helpers.text import process_lookup_name

class AttributeCache:
    def __init__(self, connection: Redis):
        self.connection = connection
    '''
        Attribute  Cache
    '''
    def checkAttributeStatusCache(self,
                                  source_attributes: dict) -> bool:
        status = self.connection.get(f"attribute.cache")
        if status and bool(status):
            return True
        else:
            ## logging
            from cacheYour.attributes.topicPackage import attributeLogger
            if os.environ.get('DEBUG') == 'DEBUG':
                log_message = {"topic": f"checkAttributeStatusCache: status false so process",
                               "message": {}}
                attributeLogger.createDebugLog(message=log_message)

            self.processAttributeCache(source_attributes=source_attributes)
            return True

    def processFeedAttribute(self,
                            attribute: dict,
                            source_id: int) -> None:
        ## saving external name data
        if attribute.get('ExternalId'):
            self.saveExternalAttributeId(externalId=attribute['ExternalId'],
                                         source=source_id,
                                         attributeId=int(attribute['InternalId']))

        ## saving external id data
        if attribute.get('ExternalName'):
            self.saveExternalAttributeName(externalName=attribute['ExternalName'],
                                           source=source_id,
                                           attributeId=int(attribute['InternalId']))


    def processAttributeCache(self,
                              source_attributes: dict):
        from cacheYour.attributes.topicPackage import attributeLogger
        from datetime import datetime
        from cacheYour.appVariables import connectionPool, ACTIVE_LANGUAGES
        from apiYour.getApi import Attributes
        from helpersYour.functions import remove_dic_key
        from cacheYour.attributes.helpers import processAttributeIndexDetails

        ## logging
        start_time = datetime.now()
        if os.environ.get('DEBUG') == 'DEBUG':
            log_message = {
                "topic": f"saveAttributeCache: start saving attribute data",
                "message": {}}
            attributeLogger.createDebugLog(message=log_message)

        attributes = Attributes.getAll(connection=connectionPool)
        print(f"Process number attributes: {len(attributes)}")

        for attribute in attributes:
            attr_dic = remove_dic_key(dic=attribute, keys=['categoryRelations'])

            ## index type
            attribute = processAttributeIndexDetails(attribute=attribute)

            self.processAttributeLanguages(languages=ACTIVE_LANGUAGES,
                                           attribute=attr_dic)

            ## saving external id lookup
            if attr_dic.get('externalId'):
                self.saveExternalAttributeId(externalId=attr_dic['externalId'],
                                             source=attr_dic['source'],
                                             attributeId=attr_dic['id'])

            ## saving details based on name
            self.saveAttributeNameDetails(attributeName=attribute['name'],
                                          data=attr_dic)

        # Feed attributes
        if source_attributes:
            for attribute in source_attributes:
                self.processFeedAttribute(attribute=attribute,
                                          source_id=attr_dic['source'])

        self.connection.set(f"attribute.cache", "True", ex=172800)
        self.connection.set(f"attribute.short-term.cache", "True", ex=6000)

        ## logging
        if os.environ.get('DEBUG') == 'DEBUG':
            log_message = {
                "topic": f"saveAttributeCache: finished saving attribute data",
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
        self.connection.set(key, json.dumps(data))

    def saveAttributeNameDetails(self,
                                 attributeName: str,
                                 data: dict):
        key = f"attribute.{process_lookup_name(attributeName)}"
        self.connection.set(key, json.dumps(data))

    def saveExternalAttributeId(self,
                                externalId: any,
                                source: int,
                                attributeId: int):
        self.connection.set(f"externalAttributeId.{externalId}.{source}", str(attributeId))

    def saveExternalAttributeName(self,
                                  externalName: str,
                                  source: int,
                                  attributeId: int):
        self.connection.set(f"externalAttributeName.{externalName}.{source}", str(attributeId))

    '''
        Attribute Value Unit Cache
    '''
    def checkAttributeValueUnitStatusCache(self) -> bool:
        status = self.connection.get(f"attributeValueUnit.cache")
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
                self.saveExternalAttributeValueUnitId(externalId=unit['externalId'],
                                                      source=2,
                                                      attributeValueUnitId=unit['id'])

        self.connection.set(f"attributeValueUnit.cache", "True", ex=172800)
        self.connection.set(f"attributeValueUnit.short-term.cache", "True", ex=3000)

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
        self.connection.set(key, json.dumps(data))

    def saveExternalAttributeValueUnitId(self,
                                         externalId: int,
                                         source: int,
                                         attributeValueUnitId: int):
        self.connection.set(f"externalAttributeValueUnitId.{externalId}.{source}", str(attributeValueUnitId))

    ## GET METHODS
    @staticmethod
    def getAttributeDetails(connection: Redis,
                            attributeId: int,
                            language: str):
        search_key = f"attribute.{attributeId}.{language}"
        attribute_details = connection.get(search_key)
        if attribute_details:
            return json.loads(attribute_details)

        else:
            return AttributeCache.keyNotFoundLogic(search_key=search_key,
                                                   cache_key="attribute.short-term.cache",
                                                   connection=connection,
                                                   content_type=dict)

    @staticmethod
    def getAttributeNameDetails(connection: Redis,
                                attributeName: str):
        search_key = f"attribute.{process_lookup_name(attributeName)}"
        attribute_details = connection.get(search_key)
        if attribute_details:
            return json.loads(attribute_details)

        else:
            return AttributeCache.keyNotFoundLogic(search_key=search_key,
                                                   cache_key="attribute.short-term.cache",
                                                   connection=connection,
                                                   content_type=dict)

    @staticmethod
    def getInternalAttributeId(connection: Redis,
                               externalId: any,
                               source: int,
                               matchType: str = 'id'):
        search_key = f"externalAttribute{matchType.capitalize()}.{externalId}.{source}"
        attribute_id = connection.get(search_key)
        if attribute_id:
            return int(attribute_id)

        else:
            return AttributeCache.keyNotFoundLogic(search_key=search_key,
                                                   cache_key="attribute.short-term.cache",
                                                   connection=connection,
                                                   content_type=int)

    @staticmethod
    def getAttributeValueUnitDetails(connection: Redis,
                                     attributeValueUnitId: int,
                                     language: str):
        search_key = f"attributeValueUnitId.{attributeValueUnitId}.{language}"
        attributeValueUnit_details = connection.get(search_key)
        if attributeValueUnit_details:
            return json.loads(attributeValueUnit_details)

        else:
            return AttributeCache.keyNotFoundLogic(search_key=search_key,
                                                   cache_key="attributeValueUnit.short-term.cache",
                                                   connection=connection,
                                                   content_type=dict)

    @staticmethod
    def getInternalAttributeValueUnitId(connection: Redis,
                                        externalId: int,
                                        source: int):
        search_key = f"externalAttributeValueUnitId.{externalId}.{source}"
        attributeValueUnit_id = connection.get(search_key)
        if attributeValueUnit_id:
            return int(attributeValueUnit_id)

        else:
            return AttributeCache.keyNotFoundLogic(search_key=search_key,
                                                   cache_key="attributeValueUnit.short-term.cache",
                                                   connection=connection,
                                                   content_type=int)

    @staticmethod
    def keyNotFoundLogic(search_key: str,
                         cache_key: str,
                         connection: Redis,
                         content_type: type):
        from cacheYour.attributes.topicPackage import attributeLogger

        ## logging
        if os.environ.get('DEBUG') == 'DEBUG':
            log_message = {"topic": f"AttributeCache: key not found so "
                                    f"verify cache moment and if needed process cache",
                           "key": search_key}
            attributeLogger.createDebugLog(message=log_message)

        ## short term cache check to fix looping on new category creation
        status = connection.get(cache_key)

        if status and bool(status):
            return None

        else:
            cache = AttributeCache(connection=connection)
            if 'attributeValueUnit' in cache_key:
                cache.processAttributeValueUnitCache()
            else:
                cache.processAttributeCache()

            result = connection.get(search_key)
            if result:
                if content_type is str:
                    return result

                ## Boolean
                if content_type is bool:
                    try:
                        return bool(result)
                    finally:
                        return False

                ## Dictionary
                if content_type is dict:
                    return json.loads(result)

                ## Integer
                if content_type is int:
                    try:
                        return int(result)
                    finally:
                        return None
            else:
                return None
