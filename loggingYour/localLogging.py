import logging
from logging.handlers import TimedRotatingFileHandler

class LocalLogger:

    def __init__(self, log_path: str,
                 logger_name: str):

        # create logger with 'spam_application'
        self.local_logger = logging.getLogger(logger_name)
        self.local_logger.setLevel(logging.DEBUG)
        # create file handler which logs even debug messages
        ih_handler = TimedRotatingFileHandler(filename=f"{log_path}/info.log", when='D',
                                              interval=1, backupCount=90, encoding='utf-8', delay=False)
        ih_handler.setLevel(logging.INFO)
        # create file handler which logs even debug messages
        fh_handler = TimedRotatingFileHandler(filename=f"{log_path}/debug.log", when='D',
                                              interval=1, backupCount=90, encoding='utf-8', delay=False)
        fh_handler.setLevel(logging.DEBUG)
        # create console handler with a error log level
        ch_handler = TimedRotatingFileHandler(filename=f"{log_path}/error.log", when='D',
                                              interval=1, backupCount=90, encoding='utf-8', delay=False)
        ch_handler.setLevel(logging.ERROR)
        # create console handler with a higher log level
        wh_handler = TimedRotatingFileHandler(filename=f"{log_path}/warning.log", when='D',
                                              interval=1, backupCount=90, encoding='utf-8', delay=False)
        wh_handler.setLevel(logging.WARNING)
        # create formatter and add it to the handlers
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        fh_handler.setFormatter(formatter)
        ch_handler.setFormatter(formatter)
        ih_handler.setFormatter(formatter)
        wh_handler.setFormatter(formatter)
        # add the handlers to the logger
        self.local_logger.addHandler(fh_handler)
        self.local_logger.addHandler(ch_handler)
        self.local_logger.addHandler(ih_handler)
        self.local_logger.addHandler(wh_handler)

    def createDebugLog(self, message):
        self.local_logger.debug(message)

    def createInfoLog(self, message):
        self.local_logger.info(message)

    def createErrorLog(self, message):
        self.local_logger.error(message)

    def createWarningLog(self, message):
        self.local_logger.warning(message)