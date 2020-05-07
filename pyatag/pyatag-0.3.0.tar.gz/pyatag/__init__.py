"""Provides connection to ATAG One Thermostat REST API."""
from .gateway import AtagOne  # noqa
from .errors import AtagException  # noqa
from .const import DEFAULT_PORT, SENSORS

# from .const import *
# from .discovery import discover_atag
