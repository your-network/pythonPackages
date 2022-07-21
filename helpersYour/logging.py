def logging_error_message(log_type, topic, data, error_message, status_code):
    import logging
    logging.basicConfig(filename=f"{log_type}ApiLogs.log", level=logging.INFO)

    logging.error(f"Read {topic} failure.\n"
                  f"Error code: {status_code}, message: {error_message} \n"
                  f"Data: {data}"
                  )
    print(f"Read {topic} failure.\n"
                  f"Error code: {status_code}, message: {error_message} \n"
                  f"Data: {data}"
        )
