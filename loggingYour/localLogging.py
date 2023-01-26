import logging
import traceback
from logging.handlers import TimedRotatingFileHandler
from loggingYour.formatter import JsonFormatter
from flask.logging import default_handler
import json

class LocalLogger:

    def __init__(self, log_path: str,
                 logger_name: str,
                 flask: bool = False):

        # create logger with 'spam_application'
        self.local_logger = logging.getLogger(logger_name)
        self.local_logger.setLevel(logging.DEBUG)

        # create file handler which logs even debug messages
        fh_handler = TimedRotatingFileHandler(filename=f"{log_path}/debug.json",
                                              when='D',
                                              interval=1,
                                              backupCount=5,
                                              encoding='utf-8',
                                              delay=False)
        fh_handler.setLevel(logging.DEBUG)
        # create file handler which logs even debug messages
        ih_handler = TimedRotatingFileHandler(filename=f"{log_path}/info.json",
                                              when='D',
                                              interval=1,
                                              backupCount=5,
                                              encoding='utf-8',
                                              delay=False)
        ih_handler.setLevel(logging.INFO)
        # create console handler with an error log level
        ch_handler = TimedRotatingFileHandler(filename=f"{log_path}/error.json",
                                              when='D',
                                              interval=1,
                                              backupCount=5,
                                              encoding='utf-8',
                                              delay=False)
        ch_handler.setLevel(logging.ERROR)
        # create console handler with a higher log level
        wh_handler = TimedRotatingFileHandler(filename=f"{log_path}/warning.json",
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

    def createLog(self, message: dict):
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

    def createDebugLog(self, message: dict):
        try:
            self.local_logger.debug(json.dumps(message))
            print(message)
        except:
            error = traceback.format_exc()
            self.local_logger.error(f"Error Debug logging: error: {str(error)}")

    def createInfoLog(self, message: dict):
        try:
            self.local_logger.info(json.dumps(message))
            print(message)
        except:
            error = traceback.format_exc()
            self.local_logger.error(f"Error Info logging: error: {str(error)}")

    def createErrorLog(self, message: dict):
        try:
            self.local_logger.error(json.dumps(message))
            print(message)
        except:
            error = traceback.format_exc()
            self.local_logger.error(f"Error Error logging: error: {str(error)}")

    def createWarningLog(self, message: dict):
        try:
            self.local_logger.warning(json.dumps(message))
            print(message)
        except:
            error = traceback.format_exc()
            self.local_logger.error(f"Error Warning logging: error: {str(error)}")