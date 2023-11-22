import os
from google.cloud import pubsub_v1
from google.cloud.pubsub_v1 import PublisherClient
from google.cloud.pubsub_v1.types import (
    BatchSettings,
    LimitExceededBehavior,
    PublishFlowControl,
    PublisherOptions
)


class QueueAuth:

    def __init__(self, service_account_info, project_id):
        self.service_account_info = service_account_info
        self.project_id = project_id
        os.environ["TOPIC_CONSTRUCT"] = f"projects/{project_id}/topics/"
        os.environ["SUB_CONSTRUCT"] = f"projects/{project_id}/subscriptions/"


    def connectSubscribeQueue(self, subscriber_name):
        subscriber = pubsub_v1.SubscriberClient.from_service_account_json(self.service_account_info)
        subscription_path = subscriber.subscription_path(
            self.project_id,
            subscriber_name
        )

        return subscriber, subscription_path

    def connectPublisherQueue(self):
        publisher = pubsub_v1.PublisherClient.from_service_account_json(self.service_account_info)

        return publisher

    def connectBatchPublisherQueue(self):
        batch_settings = BatchSettings(
            max_messages=100,  # default 100
            max_bytes=1000000,  # default 1 MB
            max_latency=10,  # default 10 ms
        )
        publisher = PublisherClient.from_service_account_json(self.service_account_info,
                                                              batch_settings=batch_settings,)

        return publisher

