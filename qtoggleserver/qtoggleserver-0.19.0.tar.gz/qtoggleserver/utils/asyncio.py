
import asyncio
import inspect
import sys

from typing import Any, Callable, List, Optional


class ParallelCaller:
    def __init__(self, parallel: int = 1, max_queued: int = 0) -> None:
        self._queue: asyncio.Queue = asyncio.Queue(max_queued)
        self._loop_tasks: List[Optional[asyncio.Task]] = []

        # Start loop tasks
        for i in range(parallel):
            self._loop_tasks.append(asyncio.create_task(self._loop(i)))

    async def call(self, func: Callable, *args, is_async: Optional[bool] = None, **kwargs) -> Any:
        # Push call details to queue
        when_ready = asyncio.Condition()
        result = {'ret': None, 'exc_info': (None, None, None)}

        # Allow QueueFull exceptions to be propagated to caller
        self._queue.put_nowait((func, is_async, args, kwargs, when_ready, result))

        # Wait for call to be ready
        async with when_ready:
            await when_ready.wait()

        # If an exception was raised, re-raise it
        typ, val, tb = result['exc_info']
        if typ:
            raise val

        return result['ret']

    async def _loop(self, index: int) -> None:
        try:
            while True:
                func, is_async, args, kwargs, when_ready, result = await self._queue.get()

                if is_async is None:
                    is_async = inspect.iscoroutinefunction(func)

                try:
                    if is_async:
                        result['ret'] = await func(*args, **kwargs)

                    else:
                        result['ret'] = func(*args, **kwargs)

                except Exception:
                    result['exc_info'] = sys.exc_info()

                async with when_ready:
                    when_ready.notify_all()

        except asyncio.CancelledError:
            pass

    def stop(self) -> None:
        for task in self._loop_tasks:
            task.cancel()


async def await_later(delay: float, coroutine: Callable, *args, loop: asyncio.AbstractEventLoop = None) -> None:
    await asyncio.sleep(delay, loop=loop)
    await coroutine(*args)
