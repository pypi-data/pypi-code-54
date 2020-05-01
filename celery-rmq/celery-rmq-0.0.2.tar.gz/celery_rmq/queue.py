import kombu

from .registry import get_exchange, _queue_registry


def register_queue(app_provider, name, routing_key, exchange_name, queue_arguments=None):
    exchange = get_exchange(exchange_name)
    connection = app_provider.get_connection()

    if not queue_arguments:
        queue_arguments = {'x-queue-type': 'classic'}

    queue = kombu.Queue(
        name=name,
        exchange=exchange,
        routing_key=routing_key,
        channel=connection,
        message_ttl=600,
        queue_arguments=queue_arguments,
        durable=True
    )

    queue.declare()

    _queue_registry[f'{name}_{routing_key}'] = queue
