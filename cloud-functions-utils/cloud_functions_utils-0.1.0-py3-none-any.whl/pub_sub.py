"""
This module provides helper functions for Google Pub/Sub.
"""

import base64
import json


def decode(data):
    """
    Decodes data coming from Pub/Sub.
    """
    return json.loads(base64.b64decode(data).decode("utf-8"))


def _encode(data):
    return json.dumps(data).encode("ascii")


def publish(messages, topic=None):
    """
    Publishes messages to a Pub/Sub topic.
    """
    from google.cloud import pubsub_v1

    publisher = pubsub_v1.PublisherClient()
    topic = topic or os.environ["PUB_SUB_TOPIC"]

    futures = [publisher.publish(topic, _encode(data)) for data in messages]
    _ = [future.result() for future in futures]
