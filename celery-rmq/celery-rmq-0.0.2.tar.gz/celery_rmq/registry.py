from .errors import NotRegistered

__all__ = (
    'get_exchange',
    'get_queue',
    '_exchange_registry',
    '_queue_registry',
    'queue_exists',
    'exchange_exists'
)

_exchange_registry = {}
_queue_registry = {}


def queue_exists(name):
    return _queue_registry.get(name, None) is not None


def get_queue(name, routing_key):
    queue_name = f'{name}_{routing_key}'
    queue = _queue_registry.get(queue_name, None)
    if not queue:
        raise NotRegistered(
            """
            `%s` has not been registered in the queue registry. has it been imported?
            """.strip()
            % name
        )
    return queue


def exchange_exists(name):
    return _exchange_registry.get(name, None) is not None


def get_exchange(name):
    exchange = _exchange_registry.get(name, None)
    if not exchange:
        raise NotRegistered(
            """
            `%s` has not been registered in the exchange registry. has it been imported?
            """.strip()
            % name
        )
    return exchange
