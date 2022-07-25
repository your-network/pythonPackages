import logging

import google.cloud.logging

def logging_handler(logger: object,
                    level: str,
                    topic: str,
                    data: dict,
                    error_message: str,
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

    logger.log_struct(json_payload, severity=level)


# def logging_error_message(log_type, topic, data, error_message, status_code):
#     import logging
#     logging.basicConfig(filename=f"{log_type}ApiLogs.log", level=logging.INFO)
#
#     logging.error(f"Read {topic} failure.\n"
#                   f"Error code: {status_code}, message: {error_message} \n"
#                   f"Data: {data}"
#                   )
#     print(f"Read {topic} failure.\n"
#                   f"Error code: {status_code}, message: {error_message} \n"
#                   f"Data: {data}"
#         )
#
# DEFAULT = 0
# DEBUG = 100
# INFO = 200
# NOTICE = 300
# WARNING = 400
# ERROR = 500
# CRITICAL = 600
# ALERT = 700
# EMERGENCY = 800
