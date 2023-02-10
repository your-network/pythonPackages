## general packages
import rootpath
abs_path = rootpath.detect()

from loggingYour.localLogging import LocalLogger
brandLogger = LocalLogger(log_path=f"{abs_path}/logs/", logger_name="brandCachelogger")