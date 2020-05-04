import json

from google.cloud.pubsub_v1 import PublisherClient as GooglePubSubClient
from arcane.firebase import generate_token
from google.oauth2 import service_account


class Client(GooglePubSubClient):
    def __init__(self, adscale_key=None):
        credentials = service_account.Credentials.from_service_account_file(adscale_key)
        super().__init__(credentials=credentials)

    def push_to_topic(self, project: str,
                      topic_name: str,
                      parameters: dict,
                      firebase_api_key: str = None,
                      await_response: bool = False):
        """ Add the message to the given topic and if needed, generates  a token to be sent along the message
        to allow authorization"""
        if firebase_api_key:
            token = generate_token(firebase_api_key)
            message = json.dumps({'parameters': parameters, 'token': token}).encode('utf-8')
        else:
            message = json.dumps({'parameters': parameters}).encode('utf-8')

        topic_path = self.topic_path(project, topic_name)
        future = self.publish(topic_path, message)
        if await_response:
            future.result()
        return future
