import json
import os
from redis import Redis


class ProductCache:
    def __init__(self, connection: Redis):
        self.connection = connection

    def process_product_cache(self, whitelist: list = []):
        from datetime import datetime
        from cacheYour.product.topicPackage import productLogger

        ## logging
        start_time = datetime.now()
        if os.environ.get('DEBUG') == 'DEBUG':
            log_message = {
                "topic": f"processProductCache: start saving product data",
                "message": {}}
            productLogger.createDebugLog(message=log_message)

        ## Whitelist
        if whitelist:
            for external_entry in whitelist:
                ProductCache.save_whitelist_entry(source_id=external_entry['SourceId'],
                                                  external_id=external_entry['ExternalId'])

        ## logging
        if os.environ.get('DEBUG') == 'DEBUG':
            log_message = {
                "topic": f"processProductCache: finished saving product data",
                "message": {"processingTime": str(datetime.now() - start_time)}}
            productLogger.createDebugLog(message=log_message)

    def save_whitelist_entry(self,
                            source_id: int,
                            external_id: str):
        self.connection.set(f"product.whitelist.{source_id}.{external_id}", "True")

    # GET
    @staticmethod
    def get_whitelist_external_id(connection: Redis,
                                  source_id: int,
                                  external_id: str):
        search_key = f"product.whitelist.{source_id}.{external_id}"

        if connection.get(search_key):
            return True
        else:
            return False
