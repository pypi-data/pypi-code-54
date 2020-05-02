# Copyright 2020 Louis Paternault
#
# This file is part of paste2sms.
#
# Paste2sms is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Paste2sms is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Paste2sms.  If not, see <https://www.gnu.org/licenses/>.

"""Send content of clipboard as a SMS.

This module is used by `paste2sms` to send SMS messages.
You can use those functions to send messages as well.

The main function of this module is :func:`sendsms`.

.. contents::
   :local:
   :depth: 1

Send SMS
--------

.. autofunction:: sendsms

Miscellaneous
-------------

.. data:: VERSION

   Version of `paste2sms` (as a :class:`str`).

.. autoclass:: P2SException

Configuration file
------------------

.. autofunction:: get_config_file

.. autofunction:: read_config
"""

from dataclasses import dataclass
import configparser
import importlib
import logging
import os

from xdg import BaseDirectory

VERSION = "1.1.0"

_CONFIG = "paste2sms.conf"


@dataclass
class P2SException(Exception):
    """Generic exception to be nicely catched and displayed to the user."""

    message: str
    level: int = logging.INFO


def get_config_file():
    """Search for a configuration file, and return its name."""
    for directory in BaseDirectory.xdg_config_dirs:
        filename = os.path.join(directory, _CONFIG)
        if os.path.exists(filename):
            return filename
    raise P2SException("No configuration file found.", level=logging.ERROR)


def read_config():
    """Return the configuration file (as a configparser.ConfigParser() object."""
    config = configparser.ConfigParser()
    config.read([get_config_file()])
    return config


def sendsms(content, *, config=None):
    """Send SMS using the provider given in configuration.

    If no configuration file is given, read it using :func:`read_config`.

    :param str content: Message to be sent.
    :param configparser.ConfigParser config: Configuration, as described in :ref:`configfile`.
    :raises P2SException:
       If an error occured: incomplete configuration file, error while sending the message…
    """
    if config is None:
        config = read_config()
    try:
        provider = config["general"]["provider"]
    except KeyError:
        raise P2SException(
            "No cellphone provider given in configuration file.", level=logging.ERROR
        )
    module = importlib.import_module(f".provider.{provider}", __package__)
    return module.sendsms(content, config=config[f"provider:{provider}"])
