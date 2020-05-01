from __future__ import absolute_import

from celery import Celery

from .settings import DEFAULT_APP_NAME, DEFAULT_BROKER_URL, \
    INSTALLED_APPS, DEFAULT_CONFIG_SETTINGS, DEFAULT_NAMESPACE


class CeleryAppProvider:

    def __init__(self, app_name=None, namespace=None, broker_url=None,
                 installed_apps=None, task_autodiscover=True,
                 object_config=None, silent=False, force=False, **kwargs):
        if not app_name:
            app_name = DEFAULT_APP_NAME
        if not broker_url:
            broker_url = DEFAULT_BROKER_URL
        if not installed_apps:
            installed_apps = INSTALLED_APPS
        if not object_config:
            object_config = DEFAULT_CONFIG_SETTINGS
        if not namespace:
            namespace = DEFAULT_NAMESPACE
        self.app = Celery(app_name, broker=broker_url, **kwargs)
        self.app.config_from_object(object_config, silent=silent, force=force, namespace=namespace)
        if task_autodiscover:
            self.app.autodiscover_tasks(installed_apps)

    def get_connection(self, block: bool = True):
        return self.app.pool.acquire(block=block)

    def get_producer(self, block: bool = True):
        return self.app.producer_pool.acquire(block=block)

    def get_app(self):
        return self.app

    def add_tasks(self, task):
        # future plan
        pass

    def add_consumer(self, consumer):
        self.app.steps['consumer'].add(consumer)
