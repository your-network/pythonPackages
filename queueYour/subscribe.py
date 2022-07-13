import os
from google.cloud import pubsub_v1

def callback(message):
    print(message.data)
    message.ack()

def subscribeTopicMessages(subscriber, topic_name, subscription_name):
    topic = f"{os.environ['YOUR_API_TOKEN']}{topic_name}"
    subscription = f"{os.environ['SUB_CONSTRUCT']}{subscription_name}"

    subscriber.create_subscription(
        name=subscription,
        topic=topic
    )

    future = subscriber.subscribe(subscription_name, callback)

    return future
