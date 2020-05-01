import kombu

from .errors import AlreadyRegistered
from .registry import _exchange_registry, exchange_exists


def register_exchange(app_provider, name, fail_silently: bool = False, _type='direct'):
    if exchange_exists(name):
        if not fail_silently:
            raise AlreadyRegistered(f'exchange with name {name} already registered')
        else:
            return

    connection = app_provider.get_connection()
    exchange = kombu.Exchange(
        name=name,
        type=_type,
        durable=True,
        channel=connection
    )

    exchange.declare()

    _exchange_registry[name] = exchange
