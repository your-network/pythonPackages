## general packages
import rootpath
abs_path = rootpath.detect()

## logging Google
from loggingYour.localLogging import LocalLogger
seriesLogger = LocalLogger(log_path=f"{abs_path}/logs/", logger_name="seriesCachelogger")
