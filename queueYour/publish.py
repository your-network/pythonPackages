import json
import os

def publishTopicMessage(publisher, topic_name, data):
    topic = f"{os.environ['YOUR_API_TOKEN']}{topic_name}"

    future = publisher.publish(topic, json.dumps(data), spam='eggs')

    print(f"result: {future.result()}")