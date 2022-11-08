
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
                  response_text: str = None,
                  labels: dict = None) -> None:

        json_payload = {"topic": topic,
                        "labels": self.labels,
                        }

        if error_message:
            json_payload.update({"error_message": error_message})

        if data:
            json_payload.update({"data": data})

        if status_code:
            json_payload.update({"status_code": status_code,
                                 "response_text": str(response_text)})

        if labels:
            json_payload.update({"labels": labels})

        if level:
            self.level = level
        try:
            ## cloud logger
            self.logger.log_struct(json_payload, severity=self.level)
        except:
            print(f"")

        ## console log
        print(json_payload)