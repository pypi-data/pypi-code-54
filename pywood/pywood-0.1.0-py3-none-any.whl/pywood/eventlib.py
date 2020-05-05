"""Модуль определяющий стандартные реализованные события."""
from pywood.events import BaseEvent
from pywood.updates.commands import is_command, is_start_command
from pywood.updates.numbers import is_int_number
from pywood.updates.texts import is_msg_w_text_to_bot
from pywood.updates.callbacks import is_callback_query

__all__ = [
    'IncomingText',
    'IncomingCommand',
    'IncomingIntNumber',
    'IncomingUpdate',
    'IncomingStartCommand',
    'IncomingCallback'
]

class IncomingCallback(BaseEvent):
    """Входящий текст."""

    @staticmethod
    def happened(update) -> bool:
        return is_callback_query(update)

class IncomingText(BaseEvent):
    """Входящий текст."""

    @staticmethod
    def happened(update) -> bool:
        return is_msg_w_text_to_bot(update)


class IncomingUpdate(BaseEvent):
    """Любое входящее обновление."""

    @staticmethod
    def happened(update) -> bool:
        return True


class IncomingCommand(BaseEvent):
    """Входящая команда."""

    @staticmethod
    def happened(update) -> bool:
        return is_command(update)

class IncomingStartCommand(BaseEvent):
    """Входящая команда `start`."""

    @staticmethod
    def happened(update) -> bool:
        return is_start_command(update)


class IncomingIntNumber(BaseEvent):
    """Число."""

    @staticmethod
    def happened(update) -> bool:
        return is_int_number(update)
