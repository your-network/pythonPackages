import json
import os
from concurrent import futures
from google import api_core
from typing import Callable
from google.cloud import pubsub_v1

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


class pubMessageHandler():
    def __init__(self, publisher):
        self.publisher = publisher

    def get_callback(self,
                     publish_future: pubsub_v1.publisher.futures.Future,
                     data: str) -> Callable[[pubsub_v1.publisher.futures.Future], None]:

        def callback(publish_future: pubsub_v1.publisher.futures.Future) -> None:
            try:
                # Wait 60 seconds for the publish call to succeed.
                print(publish_future.result(timeout=120))
            except futures.TimeoutError:
                print(f"Publishing {data} timed out.")

        return callback

    def publish_event(self,
                      topic_name: str,
                      data: dict):
        """
        :param topic_name: topic name
        :param data: message content
        :param callback: callback function you want to execute after publish message (synchronous call if callback is None)
        :returns publish_future (if callback is not None): a future that you need to wait to ensure publishing is completed
        :returns None (if callback is None): this function will ensure the message is published, raise Exception if error occurs
        """

        topic_path = self.publisher.topic_path(os.environ['GOOGLE_PROJECT_ID'], topic_name)
        publish_future = self.publisher.publish(topic_path,
                                                data=json.dumps(data).encode('utf-8'),
                                                retry=custom_retry)

        publish_future.add_done_callback(self.get_callback(publish_future, str(json.dumps(data).encode('utf-8'))))

        return publish_future

    def batch_publish_event(self,
                            topic_name: str,
                            messages: list,
                            applicationLogger: object,
                            additional_labels: dict = {}):
        """
        :param messages <= 100
        :param topic_name: topic name
        :param messages: a list of PubSubPublisherMessage that contains all the required info about
        messages going to be published.
        :param callback: callback function that will run in each publish_future
        """

        ## logging
        if bool(os.environ["DEBUG"]):
            log_message = {"topic": "publishTopicBatchMessages: start batch import",
                           "message": {"numberMessages": len(messages)}}
            if additional_labels:
                log_message.update(additional_labels)
            applicationLogger.createDebugLog(message=log_message)
            print(log_message)

        publish_futures = []
        for message in messages:
            # When you publish a message, the client returns a future.
            topic_path = self.publisher.topic_path(os.environ['GOOGLE_PROJECT_ID'], topic_name)
            publish_future = self.publisher.publish(topic_path, json.dumps(message).encode('utf-8'))
            # Non-blocking. Publish failures are handled in the callback function.
            publish_future.add_done_callback(self.get_callback(publish_future, json.dumps(message).encode('utf-8')))
            publish_futures.append(publish_future)

        # Wait for all the publish futures to resolve before exiting.
        futures.wait(publish_futures, return_when=futures.ALL_COMPLETED)

        ## logging
        if bool(os.environ["DEBUG"]):
            log_message = {"topic": "publishTopicBatchMessages: bath inserted",
                           "message": {"batchSize": len(messages)}}
            if additional_labels:
                log_message.update(additional_labels)
            applicationLogger.createDebugLog(message=log_message)
            print(log_message)

def publishTopicMessage(publisher, topic_name, data):
    topic_path = publisher.topic_path(os.environ['GOOGLE_PROJECT_ID'], topic_name)
    future = publisher.publish(topic=topic_path,
                               data=json.dumps(data).encode('utf-8'),
                               retry=custom_retry)
    try:
        return "Success"
    except Exception as e:
        print("Error publishing: " + str(e))
        return str(e)

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
