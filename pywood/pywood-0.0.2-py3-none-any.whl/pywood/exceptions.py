"""Исключения."""


class AppException(Exception):
    """Базовый класс для исключений связанных с пакетом."""


class Error(AppException):
    """Базовый класс для ошибок."""


class StateError(Error):
    """Ошибки связанные с состоянием."""


class StateDoesNotExistError(StateError):
    """Такое состояние не существует."""


class EventHandled(AppException):
    """Событие обработано."""
