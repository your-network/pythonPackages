import json
import os
from redis import Redis

class SerieCache:
    def __init__(self, connection: Redis):
        self.connection = connection

    def checkSeriesStatusCache(self):
        while True:
            status = self.connection.get(f"series.details.cache")
            if status and bool(status):
                return True
            else:
                ## logging
                from cacheYour.series.topicPackage import seriesLogger
                if os.environ.get('DEBUG') == 'DEBUG':
                    log_message = {"topic": f"checkSeriesStatusCache: status false so cache processing",
                                   "message": {}}
                    seriesLogger.createDebugLog(message=log_message)

                self.processSeriesCache()
                return True

    def processSeriesCache(self):
        from datetime import datetime
        from cacheYour.series.topicPackage import seriesLogger
        from cacheYour.appVariables import connectionPool
        from apiYour.getApi import Series

        ## logging
        start_time = datetime.now()
        if os.environ.get('DEBUG') == 'DEBUG':
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
            self.saveSeriesDetails(seriesId=serie['id'],
                                   data=base)

            ## externalId
            if serie.get("externalIDs"):
                for source in serie["externalIDs"]:
                    if serie["externalIDs"].get(source):
                        for externalId in serie["externalIDs"][source]:
                            self.saveExternalSeriesId(externalId=int(externalId),
                                                      source=int(source),
                                                      seriesId=int(serie['id']))

        self.connection.set(f"series.details.cache", "True", ex=172800)
        self.connection.set(f"series.details.short-term.cache", "True", ex=3000)

        ## logging
        if os.environ.get('DEBUG') == 'DEBUG':
            log_message = {
                "topic": f"processSeriesCache: finished saving series data",
                "message": {"processingTime": str(datetime.now() - start_time)}}
            seriesLogger.createDebugLog(message=log_message)

    def saveSeriesDetails(self,
                          seriesId: int,
                          data: dict):
        self.connection.set(f"series.{seriesId}", json.dumps(data))

    def saveExternalSeriesId(self,
                             externalId: int,
                             source: int,
                             seriesId: int):
        self.connection.set(f"externalSeriesId.{externalId}.{source}", str(seriesId))

    ## GET METHODS
    @staticmethod
    def getSeriesDetails(connection: Redis,
                         seriesId: int):
        search_key = f"series.{seriesId}"

        series_details = connection.get(search_key)
        if series_details:
            return json.loads(series_details)

        else:
            return SerieCache.keyNotFoundLogic(search_key=search_key,
                                               connection=connection,
                                               content_type=dict)

    @staticmethod
    def getInternalSeriesId(connection: Redis,
                            externalId: int,
                            source: int):
        search_key = f"externalSeriesId.{externalId}.{source}"
        series_id = connection.get(search_key)
        if series_id:
            return int(series_id)

        else:
            return SerieCache.keyNotFoundLogic(search_key=search_key,
                                               connection=connection,
                                               content_type=int)

    @staticmethod
    def keyNotFoundLogic(search_key: str,
                         connection: Redis,
                         content_type: type):
        from cacheYour.brands.topicPackage import brandLogger

        ## logging
        if os.environ.get('DEBUG') == 'DEBUG':
            log_message = {"topic": f"SeriesCache: key not found so "
                                    f"verify cache moment and if needed process cache",
                           "key": search_key}
            brandLogger.createDebugLog(message=log_message)

        ## short term cache check to fix looping on new category creation
        status = connection.get(f"series.details.short-term.cache")

        if status and bool(status):
            return None

        else:
            serie_cache = SerieCache(connection=connection)
            serie_cache.processSeriesCache()
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