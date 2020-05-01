from celery_rmq.app import CeleryAppProvider
from celery_rmq.exchange import register_exchange
from celery_rmq.queue import register_queue

from .consumers.testconsumer import BasicTestConsumer

apps = ['tests.testapp']

app_provider = CeleryAppProvider(app_name='test_celery_broker', installed_apps=apps)

app = app_provider.get_app()


# adding exchanges

def register_exchanges():
    register_exchange(app_provider, "test_exchange")


def register_queues():
    register_queue(app_provider, "test_queue", "test_routing", "test_exchange")


def add_consumers():
    app_provider.add_consumer(BasicTestConsumer)


# execution of following two functions
# "register_exchanges()" and "register_queues()"
# needs to be synced
# i.e one after another.
# because queues are depended on exchanges

register_exchanges()
register_queues()

add_consumers()

app.start()
