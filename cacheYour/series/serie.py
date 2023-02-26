import json
import os
from cacheYour.client import RedisClient

class SerieCache:
    def __init__(self, client: RedisClient):
        self.client = client

    def checkSeriesStatusCache(self):
        while True:
            status = self.client.conn.get(f"series.details.cache")
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

        self.client.conn.set(f"series.details.cache", "True", ex=172800)
        self.client.conn.set(f"series.details.short-term.cache", "True", ex=3000)

        ## logging
        if os.environ.get('DEBUG') == 'DEBUG':
            log_message = {
                "topic": f"processSeriesCache: finished saving series data",
                "message": {"processingTime": str(datetime.now() - start_time)}}
            seriesLogger.createDebugLog(message=log_message)

    def saveSeriesDetails(self,
                          seriesId: int,
                          data: dict):
        self.client.conn.set(f"series.{seriesId}", json.dumps(data))

    def saveExternalSeriesId(self,
                             externalId: int,
                             source: int,
                             seriesId: int):
        self.client.conn.set(f"externalSeriesId.{externalId}.{source}", str(seriesId))

    ## GET METHODS
    @staticmethod
    def getSeriesDetails(client: RedisClient,
                         seriesId: int):
        search_key = f"series.{seriesId}"

        series_details = client.conn.get(search_key)
        if series_details:
            return json.loads(series_details)

        else:
            ## logging
            from cacheYour.brands.topicPackage import brandLogger
            if os.environ.get('DEBUG') == 'DEBUG':
                log_message = {"topic": f"getSeriesDetails: key not found so "
                                        f"verify cache moment and if needed process cache",
                               "message": {"key": search_key}}
                brandLogger.createDebugLog(message=log_message)

            ## short term cache check to fix looping on new creation
            status = client.conn.get(f"series.details.short-term.cache")

            if status and bool(status):
                return {}
            else:
                serie_cache = SerieCache(client=client)
                serie_cache.processSeriesCache()
                series_details = client.conn.get(search_key)
                if series_details:
                    return json.loads(series_details)
                else:
                    return {}

    @staticmethod
    def getInternalSeriesId(client: RedisClient,
                            externalId: int,
                            source: int):
        search_key = f"externalSeriesId.{externalId}.{source}"
        series_id = client.conn.get(search_key)
        if series_id:
            return int(series_id)

        else:
            ## logging
            from cacheYour.brands.topicPackage import brandLogger
            if os.environ.get('DEBUG') == 'DEBUG':
                log_message = {"topic": f"getInternalSeriesId: key not found so "
                                        f"verify cache moment and if needed process cache",
                               "message": {"key": search_key}}
                brandLogger.createDebugLog(message=log_message)

            ## short term cache check to fix looping on new creation
            status = client.conn.get(f"series.details.short-term.cache")

            if status and bool(status):
                return {}

            else:
                serie_cache = SerieCache(client=client)
                serie_cache.processSeriesCache()
                series_id = client.conn.get(search_key)
                if series_id:
                    return int(series_id)
                else:
                    return None
