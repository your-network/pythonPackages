
def messageHandler(logger: object,
                    level: str,
                    topic: str,
                    data: dict = None,
                    error_message: str = None,
                    status_code: int = None,
                    response_text: str = None) -> None:

    json_payload = {"topic": topic,
                    "error_message": error_message,
                    "data": data
                    }

    if status_code:
        json_payload.update({"status_code": status_code,
                             "response_text": response_text
                             })

    ## cloud logger
    logger.log_struct(json_payload, severity=level)

    ## console log
    print(json_payload)