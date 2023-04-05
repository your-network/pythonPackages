## general packages
import rootpath
abs_path = rootpath.detect()

from loggingYour.localLogging import LocalLogger
attributeLogger = LocalLogger(log_path=f"{abs_path}/logs/", logger_name="attributeCachelogger")

