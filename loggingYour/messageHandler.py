
class messageHandler:
    def __init__(self, logger: object, level: str, labels: dict):
        self.logger = logger
        self.level = level
        self.labels = labels


    def logStruct(self,
                       topic: str,
                       data: dict = None,
                       level: str = None,
                       error_message: str = None,
                       status_code: int = None,
                       response_text: str = None) -> None:

        json_payload = {"topic": topic,
                        "error_message": error_message,
                        "data": data,
                        "labels": self.labels,
                        }

        if status_code:
            json_payload.update({"status_code": status_code,
                                 "response_text": response_text
                                 })
        if level:
            self.level = level

        ## cloud logger
        self.logger.log_struct(json_payload, severity=self.level)

        ## console log
        print(json_payload)