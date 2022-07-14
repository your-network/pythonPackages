import json
import os
from concurrent import futures
from google.cloud import pubsub_v1

# Resolve the publish future in a separate thread.
def callback(future: pubsub_v1.publisher.futures.Future) -> None:
    message_id = future.result()
    print(message_id)

def publishTopicMessage(publisher, topic_name, data):
    topic = f"{os.environ['TOPIC_CONSTRUCT']}{topic_name}"

    future = publisher.publish(topic, json.dumps(data).encode('utf-8'), spam='eggs')

def publishTopicBatchMessages(batch_publisher, topic_name, batch_data):

    topic = f"{os.environ['TOPIC_CONSTRUCT']}{topic_name}"

    publish_futures = []

    for data in batch_data:
        publish_future = batch_publisher.publish(topic, json.dumps(data).encode('utf-8'))
        publish_future.add_done_callback(callback)
        publish_futures.append(publish_future)

    futures.wait(publish_futures, return_when=futures.ALL_COMPLETED)

