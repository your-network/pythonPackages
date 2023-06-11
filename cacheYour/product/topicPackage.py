## general packages
import os
import rootpath
abs_path = rootpath.detect()
if os.getenv('LOG_DIRECTORY'):
    path = os.getenv('LOG_DIRECTORY')
else:
    path = f"{abs_path}/logs/"

## logging Google
from loggingYour.localLogging import LocalLogger
productLogger = LocalLogger(log_path=path, logger_name="productCachelogger")
