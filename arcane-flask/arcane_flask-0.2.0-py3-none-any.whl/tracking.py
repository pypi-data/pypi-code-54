from datetime import datetime
import pytz
import uuid


from arcane.datastore import Client

from arcane import pubsub
from .flask import adscale_log
from .services import ServiceEnum


PUBSUB_ACTIVITY_TRACKING_TOPIC = 'activity-tracker'


def send_tracking_information(email: str, service: str, function_name: str, project: str, adscale_key: str) -> None:
    """ Send pubsub message to the tracking cloud function"""

    pubsub_client = pubsub.Client(adscale_key)

    users_query = Client.query(kind='users')
    users_query.add_filter('email', '=', email)
    if users_query is None:
        adscale_log(ServiceEnum.TRACKING, f'User {email} is not an Adscale User. Tracking info will not be saved.')
    else:
        timestamp = datetime.now(tz=pytz.timezone('Europe/Paris')).strftime("%Y-%m-%dT%H:%M:%SZ")
        insert_id = str(uuid.uuid4())

        pubsub_client(
            project,
            PUBSUB_ACTIVITY_TRACKING_TOPIC,
            {'user_email': email,
             'service': service,
             'timestamp': timestamp,
             'function_name': function_name,
             'insert_id': insert_id
             },
            adscale_key
        )
