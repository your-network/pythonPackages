## general packages
import rootpath
abs_path = rootpath.detect()

## logging Google
from loggingYour.localLogging import LocalLogger
categoryLogger = LocalLogger(log_path=f"{abs_path}/logs/", logger_name="categoryCachelogger")
