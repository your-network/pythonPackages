def logging_error_message(topic, data, error_message):
    import logging
    logging.error(f"Read {topic} failure."
                  f" "
                  f"Error message: {error_message}"
                  f" "
                  f"Data: {data}, "
                  )
    print(f"Read {topic} failure."
            f" "
            f"Error message: {error_message}"
            f" "
            f"Data: {data}, "
        )
