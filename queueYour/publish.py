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
                              additional_labels: dict = None) -> None:

    topic = f"{os.environ['TOPIC_CONSTRUCT']}{topic_name}"

    ## logging
    labels = {"function": "publishTopicBatchMessages"}
    if additional_labels:
        labels.update(additional_labels)
    msg_handler.logStruct(topic=f"publishTopicBatchMessages: start batch queue upload",
                          labels=labels,
                          level="DEBUG")

    publish_futures = []

    batch_list = list(splitList(batch_data, 50))

    for batch in batch_list:
        size = 0
        # Data must be a bytestring
        for data in batch:
            data_dump = json.dumps(data).encode('utf-8')
            size += sys.getsizeof(data)

            publish_future = batch_publisher.publish(topic=topic,
                                                     data=data_dump,
                                                     retry=custom_retry)
            # Non-blocking. Allow the publisher client to batch multiple messages.
            publish_future.add_done_callback(callback)
            publish_futures.append(publish_future)

        futures.wait(publish_futures, return_when=futures.ALL_COMPLETED)

        msg_handler.logStruct(
            topic=f"publishTopicBatchMessages: Queue Batch insert finished. length message: {len(batch)}",
            level="DEBUG")

    msg_handler.logStruct(
        topic=f"publishTopicBatchMessages: All messages published. Number messages: {len(batch_data)}",
        level="DEBUG")
