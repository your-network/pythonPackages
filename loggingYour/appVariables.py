## Logging packages
import rootpath
import os
abs_path = rootpath.detect()
from loggingYour.logClient import logClient
from loggingYour.messageHandler import messageHandler
log_client = logClient(f"{abs_path}/atomic-affinity-356010-c4893c67467b.json")
google_logger = log_client.setLogger(os.environ.get('GOOGLE_LOGGER_NAME', 'YOURGoogle.default'))
google_msg_handler = messageHandler(logger=google_logger, level="WARNING", labels={})