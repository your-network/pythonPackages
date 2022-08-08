import json
import os
from concurrent import futures
from google.cloud import pubsub_v1
from helpersYour.functions import splitList
import sys

# Resolve the publish future in a separate thread.
def callback(future: pubsub_v1.publisher.futures.Future) -> None:
    message_id = future.result()
    # print(message_id)

def publishTopicMessage(publisher, topic_name, data):
    topic = f"{os.environ['TOPIC_CONSTRUCT']}{topic_name}"

    future = publisher.publish(topic, json.dumps(data).encode('utf-8'), spam='eggs')

def publishTopicBatchMessages(batch_publisher: object,
                              topic_name: str,
                              batch_data: list,
                              msg_handler: object) -> None:

    topic = f"{os.environ['TOPIC_CONSTRUCT']}{topic_name}"

    publish_futures = []

    batch_list = list(splitList(batch_data, 150))

    for batch in batch_list:
        # Data must be a bytestring
        for data in batch:
            data_dump = json.dumps(data).encode('utf-8')

            msg_handler.logStruct(topic=f"publishTopicBatchMessages: size: {sys.getsizeof(data)} bytes",
                                  level="DEBUG",
                                  data=data,
                                  labels={'function': 'publishTopicBatchMessages'})

            publish_future = batch_publisher.publish(topic, data_dump)
            # Non-blocking. Allow the publisher client to batch multiple messages.
            publish_future.add_done_callback(callback)
            publish_futures.append(publish_future)

        msg_handler.logStruct(topic=f"publishTopicBatchMessages: total futures size: {sys.getsizeof(publish_futures)} bytes",
                              level="DEBUG")

        futures.wait(publish_futures, return_when=futures.ALL_COMPLETED)

        msg_handler.logStruct(
            topic=f"publishTopicBatchMessages: Queue Batch insert finished",
            data=batch,
            level="DEBUG")

    msg_handler.logStruct(
        topic=f"publishTopicBatchMessages: All messages published. Number messages: {len(batch_data)}",
        level="DEBUG")
