import logging
import google.cloud.logging
from google.cloud.logging.handlers import CloudLoggingHandler

class LoggingAuth:

    def __init__(self, service_account_info: str):
        self.client = google.cloud.logging.Client.from_service_account_json(service_account_info)

    def setLoggingHandler(self, logger_name: str, level: str) -> None:
        self.gcloud_logging_handler = CloudLoggingHandler(
            self.client, name=logger_name
        )

        self.stream_handler = logging.StreamHandler()
        self.stream_handler.setLevel(level)

    def setLogger(self, logger_name: str, level: str) -> object:
        logger = self.client.logger(logger_name)
        logger.setLevel(level)
        ## set handler
        logger.addHandler(self.gcloud_logging_handler)
        logger.addHandler(self.stream_handler)

        return logger
