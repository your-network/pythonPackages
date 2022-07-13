import json
import os

def publishTopicMessage(publisher, topic_name, data):
    topic = f"{os.environ['TOPIC_CONSTRUCT']}{topic_name}"

    future = publisher.publish(topic, json.dumps(data), spam='eggs')

    print(f"result: {future.result()}")