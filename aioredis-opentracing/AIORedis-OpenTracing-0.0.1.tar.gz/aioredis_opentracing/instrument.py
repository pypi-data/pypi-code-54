import opentracing
from signalfx_tracing import utils
from wrapt import wrap_function_wrapper

from aioredis_opentracing import tracing

config = utils.Config(
    tracer=None,
)


def instrument(tracer=None):
    aioredis = utils.get_module('aioredis')
    if utils.is_instrumented(aioredis):
        return

    tracing.init_tracing(tracer=tracer or config.tracer or opentracing.tracer)

    def traced_client(__init__, client, args, kwargs):
        __init__(*args, **kwargs)
        tracing.trace_client(client)

    wrap_function_wrapper('aioredis', 'Redis.__init__', traced_client)
    utils.mark_instrumented(aioredis)


def uninstrument():
    """Will only prevent new clients from registering tracers."""
    aioredis = utils.get_module('aioredis')
    if not utils.is_instrumented(aioredis):
        return

    from aioredis import Redis
    utils.revert_wrapper(Redis, '__init__')
    utils.mark_uninstrumented(aioredis)
