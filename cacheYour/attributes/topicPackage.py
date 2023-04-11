## general packages
import os
import rootpath
abs_path = rootpath.detect()
if os.getenv('LOG_DIRECTORY'):
    path = os.getenv('LOG_DIRECTORY')
else:
    path = f"{abs_path}/logs/"

from loggingYour.localLogging import LocalLogger
attributeLogger = LocalLogger(log_path=path, logger_name="attributeCachelogger")

