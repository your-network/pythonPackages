def logging_error_message(topic, status_code, content, payload):
    import logging
    from datetime import datetime
    message = (f"Time: {datetime.now()}"
                  f""
                  f"Call {topic} failure."
                  f""
                  f"text: {content}, "
                  f""
                  f"data: {payload}")
    logging.error(message)
    print(message)