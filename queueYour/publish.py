import json
import os
from concurrent import futures
from google import api_core

custom_retry = api_core.retry.Retry(
    initial=0.250,  # seconds (default: 0.1)
    maximum=90.0,  # seconds (default: 60.0)
    multiplier=1.45,  # default: 1.3
    deadline=300.0,  # seconds (default: 60.0)
    predicate=api_core.retry.if_exception_type(
        api_core.exceptions.Aborted,
        api_core.exceptions.DeadlineExceeded,
        api_core.exceptions.InternalServerError,
        api_core.exceptions.ResourceExhausted,
        api_core.exceptions.ServiceUnavailable,
        api_core.exceptions.Unknown,
        api_core.exceptions.Cancelled,
    ),
)

def publishTopicMessage(publisher, topic_name, data):
    topic = f"{os.environ['TOPIC_CONSTRUCT']}{topic_name}"

    future = publisher.publish(topic=topic,
                               data=json.dumps(data).encode('utf-8'),
                               spam='eggs',
                               retry=custom_retry)

def publishTopicBatchMessages(batch_publisher: object,
                              topic_name: str,
                              batch_data: list,
                              applicationLogger: object,
                              additional_labels: dict = None) -> None:

    topic = f"{os.environ['TOPIC_CONSTRUCT']}{topic_name}"

    ## logging
    if bool(os.environ["DEBUG"]):
        log_message = {"topic": "publishTopicBatchMessages: start batch import",
                       "message": {"numberMessages": len(batch_data)}}
        if additional_labels:
            log_message.update(additional_labels)
        applicationLogger.createDebugLog(message=log_message)

    publish_futures = []
    end_length = len(batch_data) - 1
    for i, data in enumerate(batch_data):
        data_dump = json.dumps(data)
        data = data_dump.encode("utf-8")
        publish_future = batch_publisher.publish(topic, data)
        publish_futures.append(publish_future)

        if len(publish_futures) >= 50 or i == end_length:
            ## logging
            if bool(os.environ["DEBUG"]):
                log_message = {"topic": "publishTopicBatchMessages: bath insert",
                               "message": {"batchSize": i}}
                if additional_labels:
                    log_message.update(additional_labels)
                applicationLogger.createDebugLog(message=log_message)

            futures.wait(publish_futures, return_when=futures.ALL_COMPLETED)
            publish_futures = []

    ## logging
    if bool(os.environ["DEBUG"]):
        log_message = {"topic": "publishTopicBatchMessages: All messages published",
                       "message": {"totalInserted": i}}
        if additional_labels:
            log_message.update(additional_labels)
        applicationLogger.createDebugLog(message=log_message)
