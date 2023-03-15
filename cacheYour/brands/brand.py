import json
import os
from redis import Redis

class BrandCache:
    def __init__(self, connection: Redis):
        self.connection = connection

    def checkBrandStatusCache(self,
                              source_brands: dict = {}):
        while True:
            status = self.connection.get(f"brand.details.cache")
            if status and bool(status):
                return True
            else:
                ## logging
                from cacheYour.brands.topicPackage import brandLogger
                if os.environ.get('DEBUG') == 'DEBUG':
                    log_message = {"topic": f"checkBrandStatusCache: status false so process",
                                   "message": {}}
                    brandLogger.createDebugLog(message=log_message)

                self.setBrandCache(source_brands=source_brands)
                return True

    def processFeedBrand(self,
                         brand: dict,
                         source_id: int) -> None:
        ## saving external id data
        if brand.get('externalBrandId'):
            self.saveExternalBrandId(externalId=brand['externalBrandId'],
                                     source=source_id,
                                     brandId=int(brand['internalBrandId']))
            return

        ## saving external name data
        if brand.get('externalBrandName'):
            self.saveExternalBrandName(externalName=brand['externalBrandName'],
                                       source=source_id,
                                       brandId=int(brand['internalBrandId']))
            return

    def processBrand(self,
                     brand):
        from cacheYour.appVariables import ACTIVE_LANGUAGES

        if brand['public']:
            for language in ACTIVE_LANGUAGES:
                base = {'id': brand['id'], 'slug': brand['slug'], 'created': brand['created']}

                ## translations
                if brand.get('translations'):
                    if language in brand['translations'].keys() and brand['translations'].get(language):
                        name = brand['translations'][language]['name']
                        description = brand['translations'][language].get('description')
                        base.update({'name': name,
                                     'description': description})

                ## fallback translations
                if base.get('name') is None:
                    base.update({'name': brand['name'],
                                 'description': brand['description']})

                ## saving data
                self.saveBrandDetails(brandId=brand['id'],
                                      language=language,
                                      data=base)
                self.saveBrandNameDetails(brandName=base['name'],
                                          data=base)

        ## interal id lookup
        if brand.get("externalIDs"):
            for source in brand["externalIDs"]:
                if brand["externalIDs"].get(source):
                    for externalId in brand["externalIDs"][source]:
                        self.saveExternalBrandId(externalId=int(externalId),
                                                 source=int(source),
                                                 brandId=int(brand['id']))


    def setBrandCache(self,
                      source_brands: dict = {}):
        from datetime import datetime
        from cacheYour.brands.topicPackage import brandLogger
        from cacheYour.appVariables import connectionPool
        from apiYour.getApi import Brands

        ## logging
        start_time = datetime.now()
        if os.environ.get('DEBUG') == 'DEBUG':
            log_message = {
                "topic": f"processBrandCache: start saving brand data",
                "message": {}}
            brandLogger.createDebugLog(message=log_message)

        ## get all brands
        brands = Brands.getAll(resultsPerPage=1000,
                               connection=connectionPool)

        ## create one lookup for brands
        for brand in brands:
            self.processBrand(brand)

        ## feed matching
        if source_brands:
            for source_id in source_brands.keys():
                for brand in source_brands.get(source_id, []):
                    ## save data
                    self.processFeedBrand(brand=brand,
                                          source_id=int(source_id))

        self.connection.set(f"brand.details.cache", "True", ex=172800)
        self.connection.set(f"brand.details.short-term.cache", "True", ex=3000)

        ## logging
        if os.environ.get('DEBUG') == 'DEBUG':
            log_message = {
                "topic": f"processBrandCache: finished saving brand data",
                "message": {"processingTime": str(datetime.now() - start_time)}}
            brandLogger.createDebugLog(message=log_message)

    def saveBrandDetails(self,
                         brandId: int,
                         language: str,
                         data: dict):
        self.connection.set(f"brand.{brandId}.{language}", json.dumps(data))


    def saveExternalBrandId(self,
                            externalId: any,
                            source: int,
                            brandId: int):
        self.connection.set(f"externalBrandId.{externalId}.{source}", str(brandId))

    def saveExternalBrandName(self,
                              externalName: str,
                              source: int,
                              brandId: int):
        self.connection.set(f"externalBrandName.{externalName}.{source}", str(brandId))

    def saveBrandNameDetails(self,
                             brandName: str,
                             data: dict):
        self.connection.set(f"brand.{brandName}", json.dumps(data))

    ## GET METHODS
    @staticmethod
    def getBrandDetails(connection: Redis,
                        brandId: int,
                        language: str):

        search_key = f"brand.{brandId}.{language}"
        brand_details = connection.get(search_key)
        if brand_details:
            return json.loads(brand_details)

        else:
            return BrandCache.keyNotFoundLogic(search_key=search_key,
                                               connection=connection,
                                               content_type=dict)

    @staticmethod
    def getInternalBrand(connection: Redis,
                         external: int,
                         source: int,
                         matchingType: str):
        search_key = f"externalBrand{matchingType.capitalize()}.{external}.{source}"
        brand_id = connection.get(search_key)
        if brand_id:
            return int(brand_id)

        else:
            return BrandCache.keyNotFoundLogic(search_key=search_key,
                                               connection=connection,
                                               content_type=int)

    @staticmethod
    def keyNotFoundLogic(search_key: str,
                         connection: Redis,
                         content_type: type):
        from cacheYour.brands.topicPackage import brandLogger

        ## logging
        if os.environ.get('DEBUG') == 'DEBUG':
            log_message = {"topic": f"BrandsCache: key not found so "
                                    f"verify cache moment and if needed process cache",
                           "key": search_key}
            brandLogger.createDebugLog(message=log_message)

        ## short term cache check to fix looping on new category creation
        status = connection.get(f"brand.details.short-term.cache")

        if status and bool(status):
            return None

        else:
            brand_cache = BrandCache(connection=connection)
            brand_cache.setBrandCache()
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
