import os
from google.cloud import pubsub_v1

def callback(message):
    print(message.data)
    message.ack()

def subscribeTopicMessages(subscriber, subscription_name):
    subscription = f"{os.environ['SUB_CONSTRUCT']}{subscription_name}"

    future = subscriber.subscribe(subscription, callback)

    return future
