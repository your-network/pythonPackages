import json
import os
from concurrent import futures
from google.cloud import pubsub_v1
from google import api_core
from helpersYour.functions import splitList
import sys

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

# Resolve the publish future in a separate thread.
def callback(future: pubsub_v1.publisher.futures.Future) -> None:
    message_id = future.result()
    # print(message_id)

def publishTopicMessage(publisher, topic_name, data):
    topic = f"{os.environ['TOPIC_CONSTRUCT']}{topic_name}"

    future = publisher.publish(topic=topic,
                               data=json.dumps(data).encode('utf-8'),
                               spam='eggs',
                               retry=custom_retry)

def publishTopicBatchMessages(batch_publisher: object,
                              topic_name: str,
                              batch_data: list,
                              msg_handler: object,
                              additional_labels: dict = None,
                              local_logger: object = None) -> None:

    topic = f"{os.environ['TOPIC_CONSTRUCT']}{topic_name}"

    ## logging
    labels = {"function": "publishTopicBatchMessages"}
    if additional_labels:
        labels.update(additional_labels)
    msg_handler.logStruct(topic=f"publishTopicBatchMessages: start batch queue upload",
                          labels=labels,
                          level="DEBUG")
    if local_logger:
        local_logger.createDebugLog(message=f"Start batch queue upload, labels: {labels}, length: {len(batch_data)}")

    publish_futures = []
    length = len(batch_data)
    for i, data in enumerate(batch_data):
        data_dump = json.dumps(data)
        data = data_dump.encode("utf-8")
        publish_future = batch_publisher.publish(topic, data)
        publish_futures.append(publish_future)

        if len(publish_futures) >= 50 or i >= length:
            ## logging
            if local_logger:
                local_logger.createDebugLog(message=f"Batch import {len(publish_futures)}, labels: {labels}, data: {publish_futures}")
            futures.wait(publish_futures, return_when=futures.ALL_COMPLETED)
            publish_futures = []

        msg_handler.logStruct(
            topic=f"publishTopicBatchMessages: Queue Batch insert finished. length message: {len(batch)}",
            labels=labels,
            level="DEBUG")

    msg_handler.logStruct(
        topic=f"publishTopicBatchMessages: All messages published. Number messages: {len(batch_data)}",
        labels=labels,
        level="DEBUG")
