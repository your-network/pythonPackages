import json
import os
import rootpath
## directory
abs_path = rootpath.detect()

'''Attribute Cache'''
def processAttributeCache():
    from cacheYour.appVariables import redis
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
        print(f"attribute to process: {attr_dic}")
        processAttributeLanguages(languages=ACTIVE_LANGUAGES,
                                  attribute=attr_dic)

        ## saving external id lookup
        if attr_dic.get('externalId'):
            saveExternalAttributeId(externalId=int(attr_dic['externalId']),
                                    source=int(attr_dic['source']),
                                    attributeId=int(attr_dic['id']))

    redis.set(f"attribute.cache", "True", ex=172800)
    redis.set(f"attribute.short-term.cache", "True", ex=3000)

    ## logging
    if os.environ.get('DEBUG') == 'DEBUG':
        log_message = {
            "topic": f"saveAttributeCache: finished saving index data",
            "message": {"processingTime": str(datetime.now() - start_time)}}
        attributeLogger.createDebugLog(message=log_message)

def processAttributeLanguages(languages: list,
                              attribute: dict) -> None:
    for language in languages:
        if attribute.get('translations'):
            if attribute['translations'].get(language):
                name = attribute['translations'][language]['name']

                ## save attribute data
                data = {**attribute, **{'name': name}}
                saveAttributeDetails(attributeId=attribute['id'],
                                          language=language,
                                          data=data)
                continue

        ## fallback
        data = {**attribute, **{'name': attribute['name']}}
        saveAttributeDetails(attributeId=attribute['id'],
                             language=language,
                             data=data)

def saveAttributeDetails(attributeId: int,
                         language: str,
                         data: dict):
    from cacheYour.appVariables import redis
    key = f"attribute.{attributeId}.{language}"
    redis.set(key, json.dumps(data))

def getAttributeDetails(attributeId: int,
                        language: str):
    from cacheYour.appVariables import redis
    search_key = f"attribute.{attributeId}.{language}"
    attribute_details = redis.get(search_key)
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
        status = redis.get(f"attribute.short-term.cache")

        if status and bool(status):
            return {}

        else:
            processAttributeCache()
            attribute_details = redis.get(search_key)
            return attribute_details

def saveExternalAttributeId(externalId: int,
                            source: int,
                            attributeId: int):
    from cacheYour.appVariables import redis
    redis.set(f"externalAttributeId.{externalId}.{source}", str(attributeId))

def getInternalAttributeId(externalId: int,
                           source: int):
    from cacheYour.appVariables import redis
    search_key = f"externalAttributeId.{externalId}.{source}"
    attribute_id = redis.get(search_key)
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
        status = redis.get(f"attribute.short-term.cache")

        if status and bool(status):
            return None

        else:
            ## process cache
            processAttributeCache()
            attribute_id = redis.get(search_key)
            if attribute_id:
                return int(attribute_id)
            else:
                return None

def checkAttributeStatusCache() -> bool:
    from cacheYour.appVariables import redis
    status = redis.get(f"attribute.cache")
    if status and bool(status):
        return True
    else:
        ## logging
        from cacheYour.attributes.topicPackage import attributeLogger
        if os.environ.get('DEBUG') == 'DEBUG':
            log_message = {"topic": f"checkAttributeStatusCache: status false so process",
                           "message": {}}
            attributeLogger.createDebugLog(message=log_message)
            print(log_message)

        processAttributeCache()
        return True

'''Attribute Value Unit Cache'''
def processAttributeValueUnitCache():
    from cacheYour.appVariables import redis
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
        processAttributeValueUnitLanguages(languages=ACTIVE_LANGUAGES,
                                           attributeValueUnit=unit)

        ## saving external id lookup
        if unit.get('externalId'):
            saveExternalAttributeValueUnitId(externalId=int(unit['externalId']),
                                             source=2,
                                             attributeValueUnitId=int(unit['id']))

    redis.set(f"attributeValueUnit.cache", "True", ex=172800)
    redis.set(f"attributeValueUnit.short-term.cache", "True", ex=3000)

    ## logging
    if os.environ.get('DEBUG') == 'DEBUG':
        log_message = {
            "topic": f"saveAttributeValueUnitCache: finished saving index data",
            "message": {"processingTime": str(datetime.now() - start_time)}}
        attributeLogger.createDebugLog(message=log_message)


def processAttributeValueUnitLanguages(languages: list,
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
                saveAttributeValueUnitDetails(attributeValueUnitId=attributeValueUnit['id'],
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
                saveAttributeValueUnitDetails(attributeValueUnitId=attributeValueUnit['id'],
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
        saveAttributeValueUnitDetails(attributeValueUnitId=attributeValueUnit['id'],
                                      language=language,
                                      data=data)

def saveAttributeValueUnitDetails(attributeValueUnitId: int,
                                  language: str,
                                  data: dict):
    from cacheYour.appVariables import redis
    key = f"attributeValueUnitId.{attributeValueUnitId}.{language}"
    redis.set(key, json.dumps(data))

def getAttributeValueUnitDetails(attributeValueUnitId: int,
                                 language: str):
    from cacheYour.appVariables import redis
    search_key = f"attributeValueUnitId.{attributeValueUnitId}.{language}"
    attributeValueUnit_details = redis.get(search_key)
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
        status = redis.get(f"attributeValueUnit.short-term.cache")

        if status and bool(status):
            return {}
        else:
            ## process cache
            processAttributeValueUnitCache()
            attributeValueUnit_details = redis.get(search_key)
            return attributeValueUnit_details

def saveExternalAttributeValueUnitId(externalId: int,
                                     source: int,
                                     attributeValueUnitId: int):
    from cacheYour.appVariables import redis
    redis.set(f"externalAttributeValueUnitId.{externalId}.{source}", str(attributeValueUnitId))

def getInternalAttributeValueUnitId(externalId: int,
                                    source: int):
    from cacheYour.appVariables import redis
    search_key = f"externalAttributeValueUnitId.{externalId}.{source}"
    attributeValueUnit_id = redis.get(search_key)
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
        status = redis.get(f"attributeValueUnit.short-term.cache")

        if status and bool(status):
            return None
        else:
            ## process cache
            processAttributeValueUnitCache()
            attributeValueUnit_id = redis.get(search_key)
            if attributeValueUnit_id:
                return int(attributeValueUnit_id)
            else:
                return None

def checkAttributeValueUnitStatusCache() -> bool:
    from cacheYour.appVariables import redis
    status = redis.get(f"attributeValueUnit.cache")
    if status and bool(status):
        return True
    else:
        ## logging
        from cacheYour.attributes.topicPackage import attributeLogger
        if os.environ.get('DEBUG') == 'DEBUG':
            log_message = {"topic": f"checkattributeValueUnitStatusCache: status false so process",
                           "message": {}}
            attributeLogger.createDebugLog(message=log_message)

        processAttributeValueUnitCache()
        return True