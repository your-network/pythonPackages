import logging
import google.cloud.logging_v2
from google.cloud.logging_v2.handlers import setup_logging, CloudLoggingHandler
from google.cloud.logging_v2.handlers.transports import SyncTransport

class logClient:

    def __init__(self, service_account_info: str):
        self.client = google.cloud.logging_v2.Client.from_service_account_json(service_account_info)

    def setLogger(self, logger_name: str) -> object:
        handler = CloudLoggingHandler(self.client, name=logger_name, transport=SyncTransport)
        setup_logging(handler)
        ## set logger
        logger = google.cloud.logging_v2.Logger(logger_name, self.client)

        return logger





#
# DEFAULT = 0
# DEBUG = 100
# INFO = 200
# NOTICE = 300
# WARNING = 400
# ERROR = 500
# CRITICAL = 600
# ALERT = 700
# EMERGENCY = 800
