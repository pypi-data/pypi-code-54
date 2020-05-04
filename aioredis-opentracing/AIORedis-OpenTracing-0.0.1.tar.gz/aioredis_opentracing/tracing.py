from builtins import str
from functools import wraps

import opentracing
from opentracing.ext import tags

_g_tracer = None
_g_start_span_cb = None


def init_tracing(tracer=None, start_span_cb=None):
    """
    Set our tracer for Redis. Tracer objects from the
    OpenTracing django/flask/pyramid libraries can be passed as well.

    :param tracer: the tracer object.
    """
    if start_span_cb is not None and not callable(start_span_cb):
        raise ValueError('start_span_cb is not callable')

    global _g_tracer, _g_start_span_cb
    if hasattr(tracer, '_tracer'):
        tracer = tracer._tracer

    _g_tracer = tracer
    _g_start_span_cb = start_span_cb


def trace_client(client):
    """
    Marks a client to be traced. All commands and pipelines executed
    through this client will be traced.

    :param client: the Redis client object.
    """
    _patch_client(client)


def trace_pipeline(pipe):
    """
    Marks a pipeline to be traced.

    :param client: the Redis pipeline object to be traced.
    If executed as a transaction, the commands will appear
    under a single 'MULTI' operation.
    """
    _patch_multi_exec_execute(pipe)


def _reset_tracing():
    global _g_tracer, _g_start_span_cb
    _g_tracer = _g_start_span_cb = None


def _get_tracer():
    return opentracing.tracer if _g_tracer is None else _g_tracer


def _normalize_stmt(args):
    return ' '.join([(arg.decode('utf-8') if isinstance(arg, (bytes, bytearray)) else str(arg)) for arg in args])


def _normalize_stmts(command_stack):
    commands = [_normalize_stmt(command[1:]) for command in command_stack]
    return ';'.join(commands)


def _set_base_span_tags(span, stmt):
    span.set_tag(tags.COMPONENT, 'aioredis-py')
    span.set_tag(tags.SPAN_KIND, tags.SPAN_KIND_RPC_CLIENT)
    span.set_tag(tags.DATABASE_TYPE, 'redis')
    span.set_tag(tags.DATABASE_STATEMENT, stmt)


def _patch_client(client):
    # Patch the outgoing commands.
    _patch_obj_execute(client)

    # Patch the created pipelines.
    multi_exec_method = client.multi_exec

    @wraps(multi_exec_method)
    def tracing_multi_exec():
        multi_exec = multi_exec_method()
        _patch_multi_exec_execute(multi_exec)
        return multi_exec

    client.multi_exec = tracing_multi_exec


def _patch_multi_exec_execute(multi_exec):
    tracer = _get_tracer()

    # Patch the execute() method.
    execute_method = multi_exec.execute

    @wraps(execute_method)
    async def tracing_execute(*, return_exceptions=False):
        if not multi_exec._pipeline:
            # Nothing to process/handle.
            return await execute_method(return_exceptions=return_exceptions)

        with tracer.start_active_span('MULTI') as scope:
            span = scope.span
            _set_base_span_tags(span, _normalize_stmts(multi_exec._pipeline))

            _call_start_span_cb(span)

            try:
                res = await execute_method(return_exceptions=return_exceptions)
            except Exception as exc:
                span.set_tag(tags.ERROR, True)
                span.log_kv({
                    'event': tags.ERROR,
                    'error.object': exc,
                })
                raise

        return res

    multi_exec.execute = tracing_execute


def _patch_obj_execute(redis_obj):
    tracer = _get_tracer()

    execute_command_method = redis_obj.execute

    @wraps(execute_command_method)
    def tracing_execute_command(*args, **kwargs):
        reported_args = args

        command = reported_args[0].decode('utf-8')

        with tracer.start_active_span(command) as scope:
            span = scope.span
            _set_base_span_tags(span, _normalize_stmt(reported_args))

            _call_start_span_cb(span)

            try:
                rv = execute_command_method(*args, **kwargs)
            except Exception as exc:
                span.set_tag(tags.ERROR, True)
                span.log_kv({
                    'event': tags.ERROR,
                    'error.object': exc,
                })
                raise

        return rv

    redis_obj.execute = tracing_execute_command


def _call_start_span_cb(span):
    if _g_start_span_cb is None:
        return

    try:
        _g_start_span_cb(span)
    except Exception:
        pass
