import logging
import traceback
from logging.handlers import TimedRotatingFileHandler
from loggingYour.formatter import JsonFormatter
from flask.logging import default_handler
import json
import os
## Google logging
from google.cloud.logging_v2.handlers import setup_logging, CloudLoggingHandler
from google.cloud.logging_v2.handlers.transports import SyncTransport
import rootpath
abs_path = rootpath.detect()
from loggingYour.logClient import logClient
log_client = logClient(f"{abs_path}/atomic-affinity-356010-c4893c67467b.json")
handler = CloudLoggingHandler(log_client, name=os.environ.get('GOOGLE_LOGGER_NAME', 'YOURGoogle.default'), transport=SyncTransport)
setup_logging(handler)

class LocalLogger:

    def __init__(self, log_path: str,
                 logger_name: str,
                 flask: bool = False):

        # create logger with 'spam_application'
        self.local_logger = logging.getLogger(logger_name)
        self.local_logger.setLevel(logging.DEBUG)

        # create file handler which logs even debug messages
        fh_handler = TimedRotatingFileHandler(filename=f"{log_path}/debug.log",
                                              when='D',
                                              interval=1,
                                              backupCount=5,
                                              encoding='utf-8',
                                              delay=False)
        fh_handler.setLevel(logging.DEBUG)
        # create file handler which logs even debug messages
        ih_handler = TimedRotatingFileHandler(filename=f"{log_path}/info.log",
                                              when='D',
                                              interval=1,
                                              backupCount=5,
                                              encoding='utf-8',
                                              delay=False)
        ih_handler.setLevel(logging.INFO)
        # create console handler with an error log level
        ch_handler = TimedRotatingFileHandler(filename=f"{log_path}/error.log",
                                              when='D',
                                              interval=1,
                                              backupCount=5,
                                              encoding='utf-8',
                                              delay=False)
        ch_handler.setLevel(logging.ERROR)
        # create console handler with a higher log level
        wh_handler = TimedRotatingFileHandler(filename=f"{log_path}/warning.log",
                                              when='D',
                                              interval=1,
                                              backupCount=5,
                                              encoding='utf-8',
                                              delay=False)
        wh_handler.setLevel(logging.WARNING)
        # create formatter and add it to the handlers
        json_formatter = JsonFormatter({"level": "levelname",
                                        "message": "message",
                                        "loggerName": "name",
                                        "processName": "processName",
                                        "processID": "process",
                                        "threadName": "threadName",
                                        "threadID": "thread",
                                        "timestamp": "asctime"})
        fh_handler.setFormatter(json_formatter)
        ch_handler.setFormatter(json_formatter)
        ih_handler.setFormatter(json_formatter)
        wh_handler.setFormatter(json_formatter)

        # flask logging if true
        if flask:
            self.local_logger.addHandler(default_handler)

        # add the handlers to the logger
        self.local_logger.addHandler(fh_handler)
        self.local_logger.addHandler(ch_handler)
        self.local_logger.addHandler(ih_handler)
        self.local_logger.addHandler(wh_handler)

    def createLog(self,
                  message: dict,
                  **kwargs):
        try:
            if message.get("level") == "WARNING":
                self.local_logger.warning(message)
            elif message.get("level") == "INFO":
                self.local_logger.info(message)
            elif message.get("level") == "ERROR":
                self.local_logger.error(message)
            else:
                self.local_logger.debug(message)
        except:
            error = traceback.format_exc()
            self.local_logger.error(f"Error Create logging: error: {str(error)}")

    def createDebugLog(self,
                       message: dict,
                       **kwargs):
        try:
            self.local_logger.debug(json.dumps(message))
            print(message)
        except:
            error = traceback.format_exc()
            self.local_logger.error(f"Error Debug logging: error: {str(error)}")

    def createInfoLog(self,
                      message: dict,
                      **kwargs):
        try:
            self.local_logger.info(json.dumps(message))
            print(message)
        except:
            error = traceback.format_exc()
            self.local_logger.error(f"Error Info logging: error: {str(error)}")

    def createErrorLog(self,
                       message: dict,
                       **kwargs):
        try:
            self.local_logger.error(json.dumps(message))
            print(message)
        except:
            error = traceback.format_exc()
            self.local_logger.error(f"Error Error logging: error: {str(error)}")

    def createWarningLog(self,
                         message: dict,
                         **kwargs):
        try:
            ## local logging
            self.local_logger.warning(json.dumps(message))
            print(message)
        except:
            error = traceback.format_exc()
            self.local_logger.error(f"Error Warning logging: error: {str(error)}")