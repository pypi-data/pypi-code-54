import functools
import importlib
import logging
import os
import sys
from datetime import datetime
from typing import Any, Optional

import aiohttp
import pytz
from fastapi import FastAPI
from loguru import logger as loguru_logger

from .config import get_settings

# from scidra.main import app


current_app: Optional[FastAPI] = None


def force_async(fn):
    """
    turns a sync function to async function using threads
    """
    from concurrent.futures import ThreadPoolExecutor
    import asyncio

    pool = ThreadPoolExecutor()

    @functools.wraps(fn)
    def wrapper(*args, **kwargs):
        future = pool.submit(fn, *args, **kwargs)
        return asyncio.wrap_future(future)  # make it awaitable

    return wrapper


def force_sync(fn):
    """
    turn an async function to sync function
    """
    import asyncio

    @functools.wraps(fn)
    def wrapper(*args, **kwargs):
        res = fn(*args, **kwargs)
        if asyncio.iscoroutine(res):
            return asyncio.get_event_loop().run_until_complete(res)
        return res

    return wrapper


def sizeof_fmt(num, suffix="B"):
    for unit in ["", "K", "M", "G", "T", "P", "E", "Z"]:
        if abs(num) < 1024.0:
            return "%3.1f%s%s" % (num, unit, suffix)
        num /= 1024.0
    return "%.1f%s%s" % (num, "Y", suffix)


def resolve_dotted_path(path: str) -> Any:
    """
    Retrieves attribute (var, function, class, etc.) from module by dotted path.
    .. code-block:: python
        from datetime.datetime import utcnow as default_utcnow
        utcnow = resolve_dotted_path('datetime.datetime.utcnow')
        assert utcnow == default_utcnow
    :param path: dotted path to the attribute in module
    :return: desired attribute or None
    """
    splitted = path.split(".")
    if len(splitted) <= 1:
        return importlib.import_module(path)
    module, attr = ".".join(splitted[:-1]), splitted[-1]
    module = importlib.import_module(module)  # type: ignore
    return getattr(module, attr)


class PropagateHandler(logging.Handler):
    def emit(self, record):
        logging.getLogger("gunicorn.error").handle(record)


def get_logger() -> Any:
    """
    Gets logger that will be used throughout this whole library.
    First it finds and imports the logger, then if it can be configured
    using loguru-compatible config, it does so.

    :return: desired logger (pre-configured if loguru)
    """
    lib_logger = loguru_logger

    # Check whether it is loguru-compatible logger
    if hasattr(lib_logger, "configure"):
        lib_logger.remove()
        is_gunicorn = "gunicorn" in os.environ.get("SERVER_SOFTWARE", "")
        is_gae = os.environ.get("GAE_APPLICATION", None) is not None

        sink = PropagateHandler() if is_gunicorn else sys.stdout
        logger_config = {
            "handlers": [
                {
                    "sink": sink,
                    "level": get_settings().LOGGING_LEVEL,
                    "format": "<level>{level: <8}</level> | "
                    "<cyan>{name}</cyan>:<cyan>{function}</cyan>:"
                    "<cyan>{line}</cyan> -"
                    " <level>{message}</level>",
                }
            ]
        }
        if is_gae:
            from google.cloud import logging as g_logging  # type: ignore

            client = g_logging.Client()
            client.setup_logging()

        lib_logger.configure(**logger_config)  # type: ignore

    return lib_logger


logger = get_logger()


async def async_get(url, auth: str = None):
    async with aiohttp.ClientSession() as session:
        headers = {}
        if auth is not None:
            headers = {"Authorization": auth}
        async with session.get(url, headers=headers) as response:
            return await response.json()


def get_current_app() -> FastAPI:
    """
    Retrieves FastAPI app instance from the path, specified in project's conf.
    :return: FastAPI app
    """
    global current_app
    if current_app is None:
        logger.info("Retrieving app from dotted path")
        current_app = resolve_dotted_path(get_settings().FASTAPI_APP)
    return current_app


async def get_remote_schema(host) -> str:
    """
    Retrieves the open api json for the given url
    :return: json schema dict
    """
    async with aiohttp.ClientSession() as session:
        async with session.get(host + "/openapi.json") as r:
            return await r.json()


def get_now() -> datetime:
    """
    Retrieves `now` function from the path, specified in project's conf.
    :return: datetime of "now"
    """
    return datetime.now(tz=get_timezone())


def get_timezone():
    """
    Retrieves timezone name from settings and tries to create tzinfo from it.
    :return: tzinfo object
    """
    return pytz.timezone(get_settings().TZ)
