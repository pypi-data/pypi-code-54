from .utils import get_environment

DEFAULT_APP_NAME = 'CELERY-RMQ'
DEFAULT_NAMESPACE = 'CELERY'

# don't use default installed_apps, send installed_apps list
# while creating instance of the CeleryAppProvider
# because default installed apps list is empty
# so task auto discover won't work

INSTALLED_APPS = [

]

# Rabbit MQ and Celery Broker Configuration for task queues
# EMAIL Sending Task queues requires task managers
# Rabbit MQ and Celery is here for task management

RABBIT_MQ_USER = get_environment('RABBIT_MQ_USER', default='admin', fail_silently=True)
RABBIT_MQ_PASSWORD = get_environment('RABBIT_MQ_PASSWORD', default='admin', fail_silently=True)
BROKER_HOST = get_environment('CRMQ_BROKER_HOST', default='localhost', fail_silently=True)
BROKER_PORT = get_environment('CRMQ_BROKER_PORT', default='5672', fail_silently=True)

DEFAULT_BROKER_URL = f'amqp://{RABBIT_MQ_USER}:{RABBIT_MQ_PASSWORD}@{BROKER_HOST}:{BROKER_PORT}/'

DEFAULT_CONFIG_SETTINGS = 'celery_rmq.settings'

# DEFAULT config for celery config from object

CELERY_ACCEPT_CONTENT = ['json']
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TASK_SERIALIZER = 'json'
