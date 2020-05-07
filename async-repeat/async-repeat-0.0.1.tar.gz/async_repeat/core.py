import asyncio
import functools


def repeat(times, concurrent=False, timeout=None, return_when="ALL_COMPLETED"):
    """
    A coroutine can only be awaited for 1 time.
    The purpose of this decorator is to repeat an Async Function for dedicated times.
    :param times: times to be repeated
    :param concurrent: if the coros are running concurrently
    :param timeout: effective only when `concurrent` is True. Quit the function after dedicated seconds
    :param return_when: effective only when `concurrent` is True. Three options:
        "ALL_COMPLETED" - return when all tasks are completed
        "FIRST_COMPLETED" - return when first task is done
        "FIRST_EXCEPTION" - return when first exception occurred

    usage:

        @repeat(3)
        async def foo():
            print("foo")
            await asyncio.sleep(1)
            print("bar")
            await asyncio.sleep(1)

        asyncio.run(foo())

    """
    if not isinstance(times, int):
        raise ValueError("Times should be int, get `{}` instead".format(type(times)))

    def wrapper(func):

        @functools.wraps(func)
        async def _synchronous(*args, **kwargs):
            for _ in range(times):
                await func(*args, **kwargs)

        @functools.wraps(func)
        async def _concurrent(*args, **kwargs):
            return_conds = {"ALL_COMPLETED": asyncio.ALL_COMPLETED,
                            "FIRST_COMPLETED": asyncio.FIRST_COMPLETED,
                            "FIRST_EXCEPTION": asyncio.FIRST_EXCEPTION}
            await asyncio.wait(fs=[func(*args, **kwargs) for _ in range(times)],
                               timeout=timeout, return_when=return_conds[return_when])

        if concurrent:
            return _concurrent
        else:
            return _synchronous
    return wrapper


