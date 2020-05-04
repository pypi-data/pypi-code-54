# -* encoding: utf-8 *-
import logging
import os
from django.apps.config import AppConfig
from django.db import utils as django_db_utils
from django.db.backends.base import base as django_db_base
from django.dispatch import Signal
import time
from typing import Union, Tuple, Callable, List  # noqa. flake8 #118


MAX_RETRIES = os.getenv('DJANGO-DBRECONNECT-MAXRETRY' , 5)

_log = logging.getLogger(__name__)
default_app_config = 'django_dbconn_retry.DjangoIntegration'

pre_reconnect = Signal(providing_args=["dbwrapper"])
post_reconnect = Signal(providing_args=["dbwrapper"])


_operror_types = ()  # type: Union[Tuple[type], Tuple]
_operror_types += (django_db_utils.OperationalError,)
try:
    import psycopg2
except ImportError:
    pass
else:
    _operror_types += (psycopg2.OperationalError,)

try:
    import sqlite3
except ImportError:
    pass
else:
    _operror_types += (sqlite3.OperationalError,)

try:
    import MySQLdb
except ImportError:
    pass
else:
    _operror_types += (MySQLdb.OperationalError,)


def monkeypatch_django() -> None:
    def ensure_connection_with_retries(self: django_db_base.BaseDatabaseWrapper) -> None:
        if self.connection is not None and hasattr(self.connection, 'closed') and self.connection.closed:
            _log.debug("failed connection detected")
            self.connection = None

        if self.connection is None and not hasattr(self, '_in_connecting'):
            with self.wrap_database_errors:
                try:
                    self._in_connecting = True
                    self.connect()
                except Exception as e:
                    if isinstance(e, _operror_types):
                        if hasattr(self, "_connection_retries") and self._connection_retries >= MAX_RETRIES:
                            _log.error(f"Tried to reconnect to the database {self._connection_retries}, "
                                       f"but didn't help {str(e)}")
                            del self._in_connecting
                            post_reconnect.send(self.__class__, dbwrapper=self)
                            raise
                        else:


                            # mark the retry
                            if hasattr(self, '_connection_retries'):
                                _log.error(f"Database connection failed. Will sleep for {self._connection_retries * 10} "
                                          f"seconds and retry for the  {self._connection_retries} time")
                                self._connection_retries += 1
                                time.sleep(self._connection_retries * 10)
                            else:
                                _log.error("Database connection failed. First failure, re-attempt connection")
                                self._connection_retries = 1
                            # ensure that we retry the connection. Sometimes .closed isn't set correctly.
                            self.connection = None
                            del self._in_connecting

                            # give libraries like 12factor-vault the chance to update the credentials
                            pre_reconnect.send(self.__class__, dbwrapper=self)
                            self.ensure_connection()
                            post_reconnect.send(self.__class__, dbwrapper=self)
                    else:
                        _log.debug("Database connection failed, but not due to a known error for dbconn_retry %s",
                                   str(e))
                        del self._in_connecting
                        raise
                else:
                    # connection successful, reset the flag
                    self._connection_retries = 0
                    del self._in_connecting

    _log.debug("django_dbconn_retry: monkeypatching BaseDatabaseWrapper")
    django_db_base.BaseDatabaseWrapper.ensure_connection = ensure_connection_with_retries


class DjangoIntegration(AppConfig):
    name = "django_dbconn_retry"

    def ready(self) -> None:
        monkeypatch_django()
