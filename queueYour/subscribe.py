import os
from google.cloud import pubsub_v1

from google.cloud import pubsub_v1
from google.api_core.exceptions import DeadlineExceeded


class PubSubHandler:

    def __init__(self, subscription_name):
        self.subscription_path = f"{os.environ['SUB_CONSTRUCT']}{subscription_name}"

    def pull_messages(self,number_of_messages):
        try:
            response = self.subscriber.pull(self.subscriber_path, max_messages=number_of_messages)
            received_messages = response.received_messages
        except DeadlineExceeded as e:
            received_messages = []
            print('No messages caused error')
        return received_messages



def callback(message):
    # print(message.data)
    message.ack()

def ack_messages(subscriber, message_ids):
    if len(message_ids) > 0:
        subscriber.acknowledge(message_ids)
        return True

def subscribeTopicMessages(subscriber, subscription_name):
    subscription_path = f"{os.environ['SUB_CONSTRUCT']}{subscription_name}"

    future = subscriber.subscribe(subscription_path, callback=callback)

    return future

