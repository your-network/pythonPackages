import json
import os
from cacheYour.client import RedisClient

class BrandCache:
    def __init__(self, client:RedisClient):
        self.client = client

    def checkBrandStatusCache(self,
                              source_brands: dict = {}):
        while True:
            status = self.client.conn.get(f"brand.details.cache")
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
                         source_id: int):
        ## saving external id data
        if brand.get('externalBrandId'):
            self.saveExternalBrandId(externalId=brand['externalBrandId'],
                                    source=source_id,
                                    brandId=int(brand['internalBrandId']))
        ## saving external name data
        if brand.get('externalBrandName'):
            self.saveExternalBrandName(externalName=brand['externalBrandName'],
                                    source=source_id,
                                    brandId=int(brand['internalBrandId']))

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

        self.client.conn.set(f"brand.details.cache", "True", ex=172800)
        self.client.conn.set(f"brand.details.short-term.cache", "True", ex=3000)

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
        self.client.conn.set(f"brand.{brandId}.{language}", json.dumps(data))


    def saveExternalBrandId(self,
                            externalId: any,
                            source: int,
                            brandId: int):
        self.client.conn.set(f"externalBrandId.{externalId}.{source}", str(brandId))

    def saveExternalBrandName(self,
                              externalName: str,
                              source: int,
                              brandId: int):
        self.client.conn.set(f"externalBrandName.{externalName}.{source}", str(brandId))

    ## GET METHODS
    @staticmethod
    def getBrandDetails(client: RedisClient,
                        brandId: int,
                        language: str):

        search_key = f"brand.{brandId}.{language}"
        brand_details = client.conn.get(search_key)
        if brand_details:
            return json.loads(brand_details)

        else:
            ## logging
            from cacheYour.brands.topicPackage import brandLogger
            if os.environ.get('DEBUG') == 'DEBUG':
                log_message = {"topic": f"getBrandDetails: key not found so "
                                        f"verify cache moment and if needed process cache",
                               "message": {"key": search_key}}
                brandLogger.createDebugLog(message=log_message)

            ## short term cache check to fix looping on new creation
            status = client.conn.get(f"brand.details.short-term.cache")

            if status and bool(status):
                return {}

            else:
                ## process cache
                brand_cache = BrandCache(client=client)
                brand_cache.setBrandCache()
                brand_details = client.conn.get(search_key)
                if brand_details:
                    return json.loads(brand_details)
                else:
                    return {}

    @staticmethod
    def getInternalBrand(client: RedisClient,
                         external: int,
                         source: int,
                         matchingType: str):
        search_key = f"externalBrand{matchingType.capitalize()}.{external}.{source}"
        brand_id = client.conn.get(search_key)
        if brand_id:
            return int(brand_id)

        else:
            ## logging
            from cacheYour.brands.topicPackage import brandLogger
            if os.environ.get('DEBUG') == 'DEBUG':
                log_message = {"topic": f"getInternalBrand: key not found so "
                                        f"verify cache moment and if needed process cache",
                               "message": {"key": search_key}}
                brandLogger.createDebugLog(message=log_message)

            ## short term cache check to fix looping on new creation
            status = client.conn.get(f"brand.details.short-term.cache")

            if status and bool(status):
                return {}

            else:
                ## process cache
                brand_cache = BrandCache(client=client)
                brand_cache.setBrandCache()
                brand_id = client.conn.get(search_key)
                if brand_id:
                    return int(brand_id)
                else:
                    return None

