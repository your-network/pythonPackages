import json
import os

def processFeedBrand(brand: dict,
                     source_id: int):
    ## saving external id data
    if brand.get('externalBrandId'):
        saveExternalBrandId(externalId=brand['externalBrandId'],
                            source=source_id,
                            brandId=int(brand['internalBrandId']))
    ## saving external name data
    if brand.get('externalBrandName'):
        saveExternalBrandName(externalName=brand['externalBrandName'],
                              source=source_id,
                              brandId=int(brand['internalBrandId']))

def processBrand(brand):
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
            saveBrandDetails(brandId=brand['id'],
                             language=language,
                             data=base)

    ## interal id lookup
    if brand.get("externalIDs"):
        for source in brand["externalIDs"]:
            if brand["externalIDs"].get(source):
                for externalId in brand["externalIDs"][source]:
                    saveExternalBrandId(externalId=int(externalId),
                                        source=int(source),
                                        brandId=int(brand['id']))


def setBrandCache(source_brands: dict = {}):
    from datetime import datetime
    from cacheYour.brands.topicPackage import brandLogger
    from cacheYour.appVariables import connectionPool, redis
    from apiYour.getApi import Brands

    ## logging
    start_time = datetime.now()
    if bool(os.environ["DEBUG"]):
        log_message = {
            "topic": f"processBrandCache: start saving brand data",
            "message": {}}
        brandLogger.createDebugLog(message=log_message)

    ## get all brands
    brands = Brands.getAll(resultsPerPage=1000,
                           connection=connectionPool)

    ## create one lookup for brands
    for brand in brands:
        processBrand(brand)

    ## feed matching
    if source_brands:
        for source_id in source_brands.keys():
            for brand in source_brands.get(source_id, []):
                ## save data
                processFeedBrand(brand=brand,
                                 source_id=int(source_id))

    redis.set(f"brand.details.cache", "True", ex=172800)
    redis.set(f"brand.details.short-term.cache", "True", ex=3000)

    ## logging
    if bool(os.environ["DEBUG"]):
        log_message = {
            "topic": f"processBrandCache: finished saving brand data",
            "message": {"processingTime": str(datetime.now() - start_time)}}
        brandLogger.createDebugLog(message=log_message)

def saveBrandDetails(brandId: int,
                     language: str,
                     data: dict):
    from cacheYour.appVariables import redis
    redis.set(f"brand.{brandId}.{language}", json.dumps(data))

def getBrandDetails(brandId: int,
                    language: str):
    from cacheYour.appVariables import redis
    search_key = f"brand.{brandId}.{language}"
    brand_details = redis.get(search_key)
    if brand_details:
        return json.loads(brand_details)

    else:
        ## logging
        from cacheYour.brands.topicPackage import brandLogger
        if bool(os.environ["DEBUG"]):
            log_message = {"topic": f"getBrandDetails: key not found so "
                                    f"verify cache moment and if needed process cache",
                           "message": {"key": search_key}}
            brandLogger.createDebugLog(message=log_message)

        ## short term cache check to fix looping on new creation
        status = redis.get(f"brand.details.short-term.cache")

        if status and bool(status):
            return {}

        else:
            ## process cache
            setBrandCache()
            brand_details = redis.get(search_key)
            if brand_details:
                return json.loads(brand_details)
            else:
                return {}

def saveExternalBrandId(externalId: any,
                        source: int,
                        brandId: int):
    from cacheYour.appVariables import redis
    redis.set(f"externalBrandId.{externalId}.{source}", str(brandId))

def saveExternalBrandName(externalName: str,
                          source: int,
                          brandId: int):
    from cacheYour.appVariables import redis
    redis.set(f"externalBrandName.{externalName}.{source}", str(brandId))

def getInternalBrand(external: int,
                     source: int,
                     matchingType: str):
    from cacheYour.appVariables import redis
    search_key = f"externalBrand{matchingType.capitalize()}.{external}.{source}"
    brand_id = redis.get(search_key)
    if brand_id:
        return int(brand_id)

    else:
        ## logging
        from cacheYour.brands.topicPackage import brandLogger
        if bool(os.environ["DEBUG"]):
            log_message = {"topic": f"getInternalBrand: key not found so "
                                    f"verify cache moment and if needed process cache",
                           "message": {"key": search_key}}
            brandLogger.createDebugLog(message=log_message)

        ## short term cache check to fix looping on new creation
        status = redis.get(f"brand.details.short-term.cache")

        if status and bool(status):
            return {}

        else:
            ## process cache
            setBrandCache()
            brand_id = redis.get(search_key)
            if brand_id:
                return int(brand_id)
            else:
                return None


def checkBrandStatusCache(source_brands: dict = {}):
    from cacheYour.appVariables import redis

    while True:
        status = redis.get(f"brand.details.cache")
        if status and bool(status):
            return True
        else:
            ## logging
            from cacheYour.brands.topicPackage import brandLogger
            if bool(os.environ["DEBUG"]):
                log_message = {"topic": f"checkBrandStatusCache: status false so process",
                               "message": {}}
                brandLogger.createDebugLog(message=log_message)

            setBrandCache(source_brands=source_brands)
            return True
