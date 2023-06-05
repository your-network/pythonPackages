import json
import os
from redis import Redis
from cacheYour.helpers.images import imageProcessing
from cacheYour.helpers.text import process_lookup_name

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

            ## Fallback
            if base.get('name') is None:
                base.update({'name': category['name']})

            ## Images
            images = imageProcessing(data=category,
                                     type='category')
            base = {**base, **images}

            ## Attributes
            if int(category['purpose']) == 3:
                if category.get('attributes'):
                    upload_dic = {}
                    for attr in category['attributes']:
                        # Lookup
                        lookup_dic =  {'id': attr['id'],
                                       'name': attr['name'],
                                       'value': attr['value']}
                        # Meta
                        if attr.get('meta') and isinstance(attr.get('meta'), list):
                            for meta_row in attr['meta']:
                                lookup_dic.update({meta_row['key']: meta_row['value']})
                        # Update
                        upload_dic.update({f"{attr['id']}.{attr['value'].lower()}": lookup_dic})

                base.update({'attributes': upload_dic})

                print(f"Category {category['id']}, \n"
                      f"category: {category} \n"
                      f"attributes: {upload_dic}")

            ## Save
            self.saveCategoryDetails(categoryId=category['id'],
                                     language=language,
                                     data=base)
            self.saveCategoryNameDetails(categoryName=base['name'],
                                         data=base)

        ## externalId
        if category.get("externalIDs"):
            for source in category["externalIDs"]:
                if category["externalIDs"].get(source):
                    for externalId in category["externalIDs"][source]:
                        self.saveExternalCategoryId(externalId=externalId,
                                                    source=int(source),
                                                    purpose=int(category['purpose']),
                                                    categoryId=int(category['id']))

                        ## active categories
                        if int(category['purpose']) == 1:
                            self.saveExternalCategoryActive(externalId=externalId,
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
        print(f"Process number categories: {len(categories)}")

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
                                   externalId: any,
                                  source: int,
                                  active: bool):
        self.connection.set(f"externalCategoryId.active.{externalId}.{source}", str(active))

    '''Function saving category name'''
    def saveCategoryNameDetails(self,
                                categoryName: str,
                                data: dict):
        search_key = f"category.{process_lookup_name(categoryName)}"
        self.connection.set(search_key, json.dumps(data))
        # print(f"Saved category name search key: {search_key}")

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
            return CategoryCache.keyNotFoundLogic(search_key=search_key,
                                                  connection=connection,
                                                  content_type=int)

    @staticmethod
    def getCategoryDetails(connection: Redis,
                           categoryId: int,
                           language: str):
        search_key = f"category.{categoryId}.{language}"
        category_details = connection.get(search_key)
        if category_details:
            return json.loads(category_details)

        else:
            return CategoryCache.keyNotFoundLogic(search_key=search_key,
                                                  connection=connection,
                                                  content_type=dict)

    @staticmethod
    def getExternalCategoryActive(connection: Redis,
                                  externalId,
                                 source: int):
        search_key = f"externalCategoryId.active.{externalId}.{source}"
        category_active = connection.get(search_key)
        if category_active:
            return bool(category_active)

        else:
            return CategoryCache.keyNotFoundLogic(search_key=search_key,
                                                  connection=connection,
                                                  content_type=bool)

    @staticmethod
    def getCategoryNameDetails(connection: Redis,
                               categoryName: str) -> dict:
        search_key = f"category.{process_lookup_name(categoryName)}"
        category_details = connection.get(search_key)
        if category_details:
            return json.loads(category_details)
        else:
            return CategoryCache.keyNotFoundLogic(search_key=search_key,
                                                  connection=connection,
                                                  content_type=dict)

    @staticmethod
    def keyNotFoundLogic(search_key: str,
                         connection: Redis,
                         content_type: type):
        from cacheYour.categories.topicPackage import categoryLogger

        ## logging
        if os.environ.get('DEBUG') == 'DEBUG':
            log_message = {"topic": f"CategoryCache: key not found so "
                                    f"verify cache moment and if needed process cache",
                           "key": search_key}
            categoryLogger.createDebugLog(message=log_message)

        ## short term cache check to fix looping on new category creation
        status = connection.get(f"category.details.short-term.cache")

        if status and bool(status):
            return None

        else:
            ## process cache again
            category_cache = CategoryCache(connection=connection)
            category_cache.setCategoryCache()

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
