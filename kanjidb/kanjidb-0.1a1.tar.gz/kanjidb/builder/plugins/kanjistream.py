# -*- coding: utf-8 -*-
__all__ = ["Plugin", "loads", "load"]
import sys
import os
import functools
import re
from kanjidb.builder.plugins import PluginBase
import kanjidb.encoding


class Plugin(PluginBase):
    """This plugin read/write kanjis from/to streams.

    Given an input stream containing one unicode encoded kanji
    per line such as:

    .. code-block::

        U+4E00
        U+4E8C
        ...

    This plugin will produce a list containing:

    .. code-block::

        ["一", "二", ...]

    """

    @property
    def template_config(self):
        return {"separator": os.linesep, "encoding": kanjidb.encoding.UNICODE_PLUS}

    @property
    def required_config(self):
        config = self.template_config
        config.update({"in": ["-"], "out": "kanjis"})

        return config

    def __call__(self, **kwargs):
        kanjis = load(
            *self.plugin_config["in"],
            encoding=self.plugin_config["encoding"],
            sep=self.plugin_config["separator"]
        )

        kwargs[self.plugin_config["out"]] = kanjis

        return kwargs

    def __repr__(self):
        return "KanjiStream"


def loads(s, *, encoding=None, decode=None, sep=None):
    """Load a list of kanjis from string.

    Usage example:

    .. code-block:: python

        >> loader.loads("一二")
        ['一', '二']

    Using custom separator:

    .. code-block:: python

        >> loader.loads("一;二"), sep=";")
        ['一', '二']

    Default behaviour is that kanjis must be UTF-8 encoded, but
    this can customized:

    .. code-block:: python

        >> loader.loads("U+4E00", encoding=encoding.UNICODE_PLUS)
        ['一']

        >> loader.loads("\u4E00", encoding=encoding.UNICODE_ESCAPE)
        ['一']

    :param s: string to decode
    :param encoding: kanjis encoding
    :param decode: how to decode kanjis
    :param sep: separator between kanjis
    :return: list of decoded kanjis
    """
    decode = (
        decode
        if decode is not None
        else functools.partial(kanjidb.encoding.decode, encoding=encoding)
    )

    symbols = s if sep is None else s.split(sep)
    symbols = [re.sub("[ \t\r\n]", "", _) for _ in symbols]

    return [decode(_) for _ in symbols]


def load(*streams, encoding=None, decode=None, sep=None):
    """Load a list of kanjis from input streams.

    Usage example:

    .. code-block:: python

        load_kanjis("a.txt", "b.txt")

    Using filelike objects:

    .. code-block:: python

        load_kanjis(sys.stdin)

        with open("a.txt", "rb") as f:
            load_kanjis(f)

    Default kanjis separator is the newline character, but this can
    be customized as such:

    .. code-block:: python

        load_kanjis("a.txt", "b.txt", sep=";")

    :param streams: list of input streams to read
    :param encoding: kanjis encoding
    :param decode: how to decode kanjis
    :param sep: separator between kanjis
    :return: list of decoded kanjis
    """
    sep = sep if sep is not None else os.linesep

    def wrapper():
        for stream in streams:
            # stdin
            if stream == "-":
                stream = sys.stdin
            # Filelike object
            if hasattr(stream, "read"):
                content = stream.read()
            # Filename
            else:
                with open(stream, "rb") as f:
                    content = f.read().decode()

            yield from loads(content, encoding=encoding, decode=decode, sep=sep)

    return list(wrapper())
