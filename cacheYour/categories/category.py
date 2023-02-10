import json
import os

def processFeedCategory(category: dict,
                        source_id: int):
    ## saving external id data
    if category.get('externalCategoryName'):
        saveExternalCategoryId(externalId=category['externalCategoryName'],
                               purpose=1,
                               source=source_id,
                               categoryId=int(category['internalCategoryId']))
    ## saving external name data
    if category.get('internalCategoryName'):
        saveExternalCategoryName(externalName=category['internalCategoryName'],
                                 purpose=1,
                                 source=source_id,
                                 categoryId=int(category['internalCategoryId']))


def processCategory(category: dict):
    from cacheYour.appVariables import ACTIVE_LANGUAGES

    for language in ACTIVE_LANGUAGES:
        base = {'id': category['id'],
                'slug': category['slug'],
                'ranking': category['ranking'],
                'createdDate': category['created'],
                'parentId': category['parentId'],
                'purpose': category['purpose']}

        ## translations
        if category.get('translations'):
            if language in category['translations'].keys() and category['translations'].get(language):
                base.update({'name': category['translations'][language]['name']})

        ## fallback translations
        if base.get('name') is None:
            base.update({'name': category['name']})

        ## saving data
        saveCategoryDetails(categoryId=category['id'],
                            language=language,
                            data=base)

    ## externalId
    if category.get("externalIDs"):
        for source in category["externalIDs"]:
            if category["externalIDs"].get(source):
                for externalId in category["externalIDs"][source]:
                    saveExternalCategoryId(externalId=int(externalId),
                                           source=int(source),
                                           purpose=int(category['purpose']),
                                           categoryId=int(category['id']))

                    ## active categories
                    saveExternalCategoryActive(externalId=int(externalId),
                                               source=int(source),
                                               active=category['public'])

def setCategoryCache(source_categories: dict = {}):
    from datetime import datetime
    from cacheYour.categories.topicPackage import categoryLogger
    from cacheYour.appVariables import connectionPool, redis
    from apiYour.getApi import Category

    ## logging
    start_time = datetime.now()
    if bool(os.environ["DEBUG"]):
        log_message = {
            "topic": f"processCategoryCache: start saving category data",
            "message": {}}
        categoryLogger.createDebugLog(message=log_message)

    ## get all brands
    categories = Category.getAll(includeServiceCategories=True,
                                 connection=connectionPool)

    ## create one lookup for categories
    for category in categories:
        processCategory(category=category)

    ## process feed categories
    if source_categories:
        for source_id in source_categories.keys():
            for category in source_categories.get(source_id, []):
                ## save data
                processFeedCategory(category=category,
                                    source_id=int(source_id))

    redis.set(f"category.details.cache", "True", ex=172800)
    redis.set(f"category.details.short-term.cache", "True", ex=3000)

    ## logging
    if bool(os.environ["DEBUG"]):
        log_message = {
            "topic": f"processCategoryCache: finished saving category data",
            "message": {"processingTime": str(datetime.now() - start_time)}}
        categoryLogger.createDebugLog(message=log_message)

'''Functions around external category ids lookup'''
def saveExternalCategoryId(externalId: any,
                           purpose: int,
                           source: int,
                           categoryId: int):
    from cacheYour.appVariables import redis
    redis.set(f"externalCategoryId.{externalId}.{source}.{purpose}", str(categoryId))

def saveExternalCategoryName(externalName: str,
                             purpose: int,
                             source: int,
                             categoryId: int):
    from cacheYour.appVariables import redis
    redis.set(f"externalCategoryName.{externalName}.{source}.{purpose}", str(categoryId))

def getInternalCategory(external: int,
                        purpose: int,
                        source: int,
                        matchingType: str):
    from cacheYour.appVariables import redis
    search_key = f"externalCategory{matchingType.capitalize()}.{external}.{source}.{purpose}"
    category_id = redis.get(search_key)
    if category_id:
        return int(category_id)

    else:
        ## logging
        from cacheYour.categories.topicPackage import categoryLogger
        if bool(os.environ["DEBUG"]):
            log_message = {"topic": f"getInternalCategory: key not found so process cache",
                           "message": {"key": search_key}}
            categoryLogger.createDebugLog(message=log_message)

        setCategoryCache()
        category_id = redis.get(search_key)
        if category_id:
            return int(category_id)
        else:
            return None


'''Functions around details of categories'''
def saveCategoryDetails(categoryId: int,
                        language: str,
                        data: dict):
    from cacheYour.appVariables import redis
    redis.set(f"category.{categoryId}.{language}", json.dumps(data))

def getCategoryDetails(categoryId: int,
                       language: str):
    from cacheYour.appVariables import redis
    from cacheYour.categories.topicPackage import categoryLogger

    search_key = f"category.{categoryId}.{language}"
    category_details = redis.get(search_key)
    if category_details:
        return json.loads(category_details)

    else:
        ## logging
        if bool(os.environ["DEBUG"]):
            log_message = {"topic": f"getCategoryDetails: category key not found so "
                                    f"verify cache moment and if needed process cache",
                           "message": {"key": search_key}}
            categoryLogger.createDebugLog(message=log_message)

        ## short term cache check to fix looping on new category creation
        status = redis.get(f"category.details.short-term.cache")

        if status and bool(status):
            return {}

        else:
            ## process cache again
            setCategoryCache()

            category_details = redis.get(search_key)
            if category_details:
                return json.loads(category_details)
            else:
                return {}

'''Functions around active status of categories'''
def saveExternalCategoryActive(externalId: int,
                              source: int,
                              active: bool):
    from cacheYour.appVariables import redis
    redis.set(f"externalCategoryId.active.{externalId}.{source}", str(active))

def getExternalCategoryActive(externalId,
                             source: int):
    from cacheYour.appVariables import redis
    from cacheYour.categories.topicPackage import categoryLogger

    search_key = f"externalCategoryId.active.{externalId}.{source}"
    category_active = redis.get(search_key)
    if category_active:
        return bool(category_active)

    else:
        ## logging
        if bool(os.environ["DEBUG"]):
            log_message = {"topic": f"getExternalCategoryActive: category key not found so process cache",
                           "message": {"key": search_key}}
            categoryLogger.createDebugLog(message=log_message)

        setCategoryCache()
        category_active = redis.get(search_key)
        if category_active:
            return bool(category_active)
        else:
            return False

'''Functions around checking status of category cache'''
def checkCategoryStatusCache(source_categories: dict = {}):
    from cacheYour.appVariables import redis
    from cacheYour.categories.topicPackage import categoryLogger

    status = redis.get(f"category.details.cache")

    if status and bool(status):
        ## logging
        if bool(os.environ["DEBUG"]):
            log_message = {"topic": f"checkCategoryStatusCache: category cache checked and present"}
            categoryLogger.createDebugLog(message=log_message)

        return True
    else:
        ## logging
        if bool(os.environ["DEBUG"]):
            log_message = {"topic": f"checkCategoryStatusCache: category cache checked and not present so process"}
            categoryLogger.createDebugLog(message=log_message)

        setCategoryCache(source_categories=source_categories)
        return True