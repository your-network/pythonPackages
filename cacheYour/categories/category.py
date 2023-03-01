import json
import os
from redis import Redis

class CategoryCache:
    def __init__(self, connection: Redis):
        self.connection = connection

    '''Functions around checking status of category cache'''
    def checkCategoryStatusCache(self,
                                 source_categories: dict = {}):
        from cacheYour.categories.topicPackage import categoryLogger

        status = self.connection.get(f"category.details.cache")

        if status and bool(status):
            ## logging
            if os.environ.get('DEBUG') == 'DEBUG':
                log_message = {"topic": f"checkCategoryStatusCache: category cache checked and present"}
                categoryLogger.createDebugLog(message=log_message)

            return True
        else:
            ## logging
            if os.environ.get('DEBUG') == 'DEBUG':
                log_message = {"topic": f"checkCategoryStatusCache: category cache checked and not present so process"}
                categoryLogger.createDebugLog(message=log_message)

            self.setCategoryCache(source_categories=source_categories)
            return True

    def processFeedCategory(self,
                            category: dict,
                            source_id: int) -> None:
        ## saving external name data
        if category.get('externalCategoryId'):
            self.saveExternalCategoryId(externalId=category['externalCategoryId'],
                                        purpose=1,
                                        source=source_id,
                                        categoryId=int(category['internalCategoryId']))
            return

        ## saving external id data
        if category.get('externalCategoryName'):
            self.saveExternalCategoryName(externalName=category['externalCategoryName'],
                                          purpose=1,
                                          source=source_id,
                                          categoryId=int(category['internalCategoryId']))
            return

    def processCategory(self,
                        category: dict):
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
            self.saveCategoryDetails(categoryId=category['id'],
                                     language=language,
                                     data=base)

        ## externalId
        if category.get("externalIDs"):
            for source in category["externalIDs"]:
                if category["externalIDs"].get(source):
                    for externalId in category["externalIDs"][source]:
                        self.saveExternalCategoryId(externalId=int(externalId),
                                                    source=int(source),
                                                    purpose=int(category['purpose']),
                                                    categoryId=int(category['id']))

                        ## active categories
                        self.saveExternalCategoryActive(externalId=int(externalId),
                                                        source=int(source),
                                                        active=category['public'])

    def setCategoryCache(self,
                         source_categories: dict = {}):
        from datetime import datetime
        from cacheYour.categories.topicPackage import categoryLogger
        from cacheYour.appVariables import connectionPool
        from apiYour.getApi import Category

        ## logging
        start_time = datetime.now()
        if os.environ.get('DEBUG') == 'DEBUG':
            log_message = {
                "topic": f"processCategoryCache: start saving category data",
                "message": {}}
            categoryLogger.createDebugLog(message=log_message)

        ## get all brands
        categories = Category.getAll(includeServiceCategories=True,
                                     connection=connectionPool)

        ## create one lookup for categories
        for category in categories:
            self.processCategory(category=category)

        ## process feed categories
        if source_categories:
            for source_id in source_categories.keys():
                for category in source_categories.get(source_id, []):
                    ## save data
                    self.processFeedCategory(category=category,
                                             source_id=int(source_id))

        self.connection.set(f"category.details.cache", "True", ex=172800)
        self.connection.set(f"category.details.short-term.cache", "True", ex=3000)

        ## logging
        if os.environ.get('DEBUG') == 'DEBUG':
            log_message = {
                "topic": f"processCategoryCache: finished saving category data",
                "message": {"processingTime": str(datetime.now() - start_time)}}
            categoryLogger.createDebugLog(message=log_message)

    '''Functions around external category ids lookup'''
    def saveExternalCategoryId(self,
                               externalId: any,
                               purpose: int,
                               source: int,
                               categoryId: int):
        self.connection.set(f"externalCategoryId.{externalId}.{source}.{purpose}", str(categoryId))

    def saveExternalCategoryName(self,
                                 externalName: str,
                                 purpose: int,
                                 source: int,
                                 categoryId: int):
        self.connection.set(f"externalCategoryName.{externalName}.{source}.{purpose}", str(categoryId))

    '''Functions around category details'''
    def saveCategoryDetails(self,
                            categoryId: int,
                            language: str,
                            data: dict):
        self.connection.set(f"category.{categoryId}.{language}", json.dumps(data))

    '''Functions around active status of categories'''
    def saveExternalCategoryActive(self,
                                   externalId: int,
                                  source: int,
                                  active: bool):
        self.connection.set(f"externalCategoryId.active.{externalId}.{source}", str(active))


    ## GET METHODS
    @staticmethod
    def getInternalCategory(connection: Redis,
                            external: int,
                            purpose: int,
                            source: int,
                            matchingType: str):

        search_key = f"externalCategory{matchingType.capitalize()}.{external}.{source}.{purpose}"
        category_id = connection.get(search_key)
        if category_id:
            return int(category_id)

        else:
            ## logging
            from cacheYour.categories.topicPackage import categoryLogger
            if os.environ.get('DEBUG') == 'DEBUG':
                log_message = {"topic": f"getInternalCategory: key not found so process cache",
                               "message": {"key": search_key}}
                categoryLogger.createDebugLog(message=log_message)

            ## short term cache check to fix looping on new category creation
            status = connection.get(f"category.details.short-term.cache")

            if status and bool(status):
                return {}

            else:
                ## process cache again
                category_cache = CategoryCache(connection=connection)
                category_cache.setCategoryCache()

                category_id = connection.get(search_key)
                if category_id:
                    return int(category_id)
                else:
                    return None

    @staticmethod
    def getCategoryDetails(connection: Redis,
                           categoryId: int,
                           language: str):
        from cacheYour.categories.topicPackage import categoryLogger

        search_key = f"category.{categoryId}.{language}"
        category_details = connection.get(search_key)
        if category_details:
            return json.loads(category_details)

        else:
            ## logging
            if os.environ.get('DEBUG') == 'DEBUG':
                log_message = {"topic": f"getCategoryDetails: category key not found so "
                                        f"verify cache moment and if needed process cache",
                               "message": {"key": search_key}}
                categoryLogger.createDebugLog(message=log_message)

            ## short term cache check to fix looping on new category creation
            status = connection.get(f"category.details.short-term.cache")

            if status and bool(status):
                return {}

            else:
                ## process cache again
                category_cache = CategoryCache(connection=connection)
                category_cache.setCategoryCache()

                category_details = connection.get(search_key)
                if category_details:
                    return json.loads(category_details)
                else:
                    return {}
    @staticmethod
    def getExternalCategoryActive(connection: Redis,
                                  externalId,
                                 source: int):
        from cacheYour.categories.topicPackage import categoryLogger

        search_key = f"externalCategoryId.active.{externalId}.{source}"
        category_active = connection.get(search_key)
        if category_active:
            return bool(category_active)

        else:
            ## logging
            if os.environ.get('DEBUG') == 'DEBUG':
                log_message = {"topic": f"getExternalCategoryActive: category key not found",
                               "message": {"key": search_key}}
                categoryLogger.createDebugLog(message=log_message)

            ## short term cache check to fix looping on new category creation
            status = connection.get(f"category.details.short-term.cache")

            if status and bool(status):
                return {}

            else:
                ## process cache again
                category_cache = CategoryCache(connection=connection)
                category_cache.setCategoryCache()
                category_active = connection.get(search_key)
                if category_active:
                    return bool(category_active)
                else:
                    return False
