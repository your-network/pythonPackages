import json
from google.auth import jwt
import os
from google.cloud import pubsub_v1

class QueueAuth:

    def __init__(self, service_account_info, project_id):
        self.service_account_info = service_account_info
        os.environ["TOPIC_CONSTRUCT"] = f"projects/{project_id}/topics/"
        os.environ["SUB_CONSTRUCT"] = f"projects/{project_id}/subscriptions/"

    def getQueueSubscriber(self):

        audience = "https://pubsub.googleapis.com/google.pubsub.v1.Subscriber"

        credentials = jwt.Credentials.from_service_account_info(
            self.service_account_info, audience=audience
        )

        subscriber = pubsub_v1.SubscriberClient(credentials=credentials)

        return subscriber

    def getQueuePublisher(self):
        publisher_audience = "https://pubsub.googleapis.com/google.pubsub.v1.Publisher"

        credentials = jwt.Credentials.from_service_account_info(
            self.service_account_info, audience=publisher_audience
        )

        credentials_pub = credentials.with_claims(audience=publisher_audience)

        publisher = pubsub_v1.PublisherClient(credentials=credentials_pub)

        return publisher