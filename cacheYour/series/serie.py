import json
import os

def processSeriesCache():
    from datetime import datetime
    from cacheYour.series.topicPackage import seriesLogger
    from cacheYour.appVariables import connectionPool, redis
    from apiYour.getApi import Series

    ## logging
    start_time = datetime.now()
    if bool(os.environ["DEBUG"]):
        log_message = {
            "topic": f"processSeriesCache: start saving series data",
            "message": {}}
        seriesLogger.createDebugLog(message=log_message)

    ## get all brands
    series = Series.getAll(connection=connectionPool)

    ## create one lookup for categories
    for serie in series:
        base = {'id': serie['id'],
                 'categoryId': serie['categoryId'],
                 'name': serie['name'],
                 'externalIDs': serie['externalIDs']}

        ## saving data
        saveSeriesDetails(seriesId=serie['id'],
                          data=base)

        ## externalId
        if serie.get("externalIDs"):
            for source in serie["externalIDs"]:
                if serie["externalIDs"].get(source):
                    for externalId in serie["externalIDs"][source]:
                        saveExternalSeriesId(externalId=int(externalId),
                                             source=int(source),
                                             seriesId=int(serie['id']))

    redis.set(f"series.details.cache", "True", ex=172800)

    ## logging
    if bool(os.environ["DEBUG"]):
        log_message = {
            "topic": f"processSeriesCache: finished saving series data",
            "message": {"processingTime": str(datetime.now() - start_time)}}
        seriesLogger.createDebugLog(message=log_message)

def saveSeriesDetails(seriesId: int,
                      data: dict):
    from cacheYour.appVariables import redis
    redis.set(f"series.{seriesId}", json.dumps(data))

def getSeriesDetails(seriesId: int):
    from cacheYour.appVariables import redis
    search_key = f"series.{seriesId}"
    series_details = redis.get(search_key)
    if series_details:
        return json.loads(series_details)

    else:
        ## logging
        from cacheYour.series.topicPackage import seriesLogger
        if bool(os.environ["DEBUG"]):
            log_message = {"topic": f"getSeriesDetails: key not found so process cache",
                           "message": {"key": search_key}}
            seriesLogger.createDebugLog(message=log_message)

        processSeriesCache()
        series_details = redis.get(search_key)
        if series_details:
            return json.loads(series_details)
        else:
            return {}

def saveExternalSeriesId(externalId: int,
                         source: int,
                         seriesId: int):
    from cacheYour.appVariables import redis
    redis.set(f"externalSeriesId.{externalId}.{source}", str(seriesId))

def getInternalSeriesId(externalId: int,
                          source: int):
    from cacheYour.appVariables import redis
    search_key = f"externalSeriesId.{externalId}.{source}"
    series_id = redis.get(search_key)
    if series_id:
        return int(series_id)

    else:
        ## logging
        from cacheYour.series.topicPackage import seriesLogger
        if bool(os.environ["DEBUG"]):
            log_message = {"topic": f"getInternalSeriesId: key not found so process cache",
                           "message": {"key": search_key}}
            seriesLogger.createDebugLog(message=log_message)

        processSeriesCache()
        series_id = redis.get(search_key)
        if series_id:
            return int(series_id)
        else:
            return None

def checkSeriesStatusCache():
    from cacheYour.appVariables import redis

    while True:
        status = redis.get(f"series.details.cache")
        if status and bool(status):
            return True
        else:
            ## logging
            from cacheYour.series.topicPackage import seriesLogger
            if bool(os.environ["DEBUG"]):
                log_message = {"topic": f"checkSeriesStatusCache: status false so cache processing",
                               "message": {}}
                seriesLogger.createDebugLog(message=log_message)

            processSeriesCache()
            return True