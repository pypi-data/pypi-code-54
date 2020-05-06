"""
    Python Version: >= 3.6
    Author: Marciano Barros
    Email: marciano.barros@pestana.com
    Maintainer: Marciano Barros
    Copyright: Marciano Barros
    License: MIT
    Version: 1.0.4
    Status: Production/Stable,
"""
from typing import Union
import time as timemod
from datetime import timedelta, time
import socket
import base64
from struct import unpack
import re
import datetime
import logging
from logging.handlers import RotatingFileHandler
try:
    import texttable
except ImportError:
    raise ImportError('Please install texttable module and try again => pip install texttable')

# Python DB API Globals
apilevel = "2.0"
# 0	Threads may not share the module.
# 1	Threads may share the module, but not connections.
# 2	Threads may share the module and connections.
# 3	Threads may share the module, connections and cursors.
# Sharing in the above context means that two threads may use a resource without wrapping it using a mutex semaphore
# to implement resource locking. Note that you cannot always make external resources thread safe by managing access
# using a mutex: the resource may rely on global variables or other external sources that are beyond your control.
threadsafety = 1
# String constant stating the type of parameter marker formatting expected by the interface. Possible values are
# paramstyle - Meaning
# qmark	- Question mark style, e.g. ...WHERE name=?
# named	- Named style, e.g. ...WHERE name=:name
# format - ANSI C printf format codes, e.g. ...WHERE name=%s
# pyformat - Python extended format codes, e.g. ...WHERE name=%(name)s
paramstyle = "named"

# Error Classes
# StandardError
# |__Warning
# |__Error
#    |__InterfaceError
#    |__DatabaseError
#       |__DataError
#       |__OperationalError
#       |__IntegrityError
#       |__InternalError
#       |__ProgrammingError
#       |__NotSupportedError


class Warning(Exception):
    """
    Exception raised for important warnings like data truncations while inserting, etc
    """
    pass


class Error(Exception):
    """
    Exception that is the base class of all other error exceptions.
    You can use this to catch all errors with one single except statement
    Warnings are not considered errors and thus should not use this class as base
    """
    pass


class InterfaceError(Error):
    """
    Exception raised for errors that are related to the database interface rather than the database itself
    """
    pass


class DatabaseError(Error):
    """
    Exception raised for errors that are related to the database
    """
    pass


class DataError(DatabaseError):
    """
    Exception raised for errors that are due to problems with the processed data like division by zero, numeric value
    out of range, etc
    """
    pass


class OperationalError(DatabaseError):
    """
    Exception raised for errors that are related to the database's operation and not necessarily under the control of
    the programmer, e.g. an unexpected disconnect occurs, the data source name is not found, a transaction could not
    be processed, a memory allocation error occurred during processing, etc
    """
    pass


class IntegrityError(DatabaseError):
    """
    Exception raised when the relational integrity of the database is affected, e.g. a foreign key check fails.
    """
    pass


class InternalError(DatabaseError):
    """
    Exception raised when the database encounters an internal error, e.g. the cursor is not valid anymore,
    the transaction is out of sync, etc
    """
    pass


class ProgrammingError(DatabaseError):
    """
    Exception raised for programming errors, e.g. table not found or already exists, syntax error in the SQL statement,
    wrong number of parameters specified, etc
    """
    pass


class NotSupportedError(DatabaseError):
    """
    Exception raised in case a method or database API was used which is not supported by the database, e.g.
    requesting a .rollback() on a connection that does not support transaction or has transactions turned off
    """
    pass


def get_date(year=1900, month=1, day=1) -> datetime.datetime:
    """
    This function constructs an object holding a date value.

    :param year: int
    :param month: int
    :param day: int

    :return: datetime.datetime
    """
    return datetime.datetime(year=year, month=month, day=day)


def get_time(hour=0, minute=0, second=0, microsecond=0) -> datetime.datetime:
    """
    This function constructs an object holding a time value.

    :param hour: int
    :param minute: int
    :param second: int
    :param microsecond: int

    :return: datetime.datetime
    """
    return datetime.datetime(year=1900, month=1, day=1, hour=hour, minute=minute, second=second,
                             microsecond=microsecond)


def get_time_stamp(year=1900, month=1, day=1, hour=0, minute=0, second=0, microsecond=0) -> datetime.datetime:
    """
    This function constructs an object holding a time stamp value.

    :param year: int
    :param month: int
    :param day: int
    :param hour: int
    :param minute: int
    :param second: int
    :param microsecond: int

    :return: datetime.datetime
    """
    return datetime.datetime(year=year, month=month, day=day, hour=hour, minute=minute, second=second,
                             microsecond=microsecond)


def get_date_from_ticks(ticks: object) -> datetime.datetime:
    """
    This function constructs an object holding a date value from the given ticks value
    number of seconds since the epoch; see the documentation of the standard Python time module for details).

    :param ticks: float

    :return: datetime.datetime
    """
    return get_date(*timemod.localtime(ticks)[:3])


def get_time_from_ticks(ticks) -> datetime.datetime:
    """
    This function constructs an object holding a time value from the given ticks value
    (number of seconds since the epoch; see the documentation of the standard Python time module for details).

    :param ticks: float

    :return: datetime.datetime
    """
    return get_time(*timemod.localtime(ticks)[3:6])


def get_time_stamp_from_ticks(ticks) -> datetime.datetime:
    """
    This function constructs an object holding a time stamp value from the given ticks value
    (number of seconds since the epoch; see the documentation of the standard Python time module for details).

    :param ticks: float

    :return: datetime.datetime
    """
    return get_time_stamp(*timemod.localtime(ticks)[:6])


def get_4d_to_python_types() -> dict:
    """
    Creates a dict of 4D SQL vars to Python types

    :return: dict
    """
    return {'VK_BOOLEAN': bool,
            'VK_BYTE': str,
            'VK_WORD': str,
            'VK_LONG': int,
            'VK_LONG8': int,
            'VK_REAL': float,
            'VK_FLOAT': float,
            'VK_TIME': time,
            'VK_TIMESTAMP': datetime.datetime,
            'VK_DURATION': datetime.timedelta,
            'VK_TEXT': str,
            'VK_STRING': str,
            'VK_BLOB': bytes,
            'VK_IMAGE': bytes,
            'VK_UNKNOWN': None}


# 4D constants
FOURD_OK = 0
FOURD_ERROR = 1


class _python4DEventHook(object):
    """
    Event handler
    """

    # Private variables
    _handlers = []

    def __init__(self):
        self._handlers = []

    def __iadd__(self, handler: object) -> object:
        """
        Appends an event handler

        :param handler: Object (function)
        :return: Self
        """
        self._handlers.append(handler)
        return self

    def __isub__(self, handler: object) -> object:
        """
        Removes an event handler

        :param handler: Object (function)
        :return: Self
        """
        self._handlers.remove(handler)
        return self

    def fire(self, args: object, **kwargs: object) -> None:
        """
        Runs all the event handlers

        :param args: Object
        :param kwargs: Object
        :return: None
        """
        for handler in self._handlers:
            handler(*args, **kwargs)


class _python4DCursor(object):
    """
    It consists of pure application logic, which interacts with the database.
    It includes all the information to represent data to the end user.
    """

    # Private variables
    _debug_header_messages = False
    _connection = None
    _socket = None
    _session_id = ''
    _authenticated = False
    _protocol_version = '12.0'
    _preferred_image_types = 'png'
    _reply_with_b64 = 'Y'
    _use_b64 = False
    _encoding = 'UTF-8'
    _cmd_id = 0
    _statement_dict = {}
    _statement_cmd_id = 0
    _output_mode = 'release'  # [RELEASE | DEBUG]
    _page_size = 100
    _updated_row = -1
    _rows = []
    _4d_to_python_types = get_4d_to_python_types()
    _error_code = 0
    _error_description = ''
    _cursor_closed = True
    _in_transaction = False
    # <	little-endian - MAC OS X RVLB
    # >	big-endian - Windows BLVR
    _fmt = '<'
    # vk_string should be always UTF-16LE as per docs, but if cant decode
    # try the fallback's
    _vk_string_encodings = ['UTF-16LE', 'UTF-8', 'MAC-ROMAN']
    _view = None
    _logger = None

    def __init__(self, connection: object):
        """
        Constructor

        :param connection: python4DBI

        :return: None
        :raises: ProgramingError
        """

        if not isinstance(connection, python4DBI):
            _error_msg = 'Can not continue please check the connection argument!'
            raise ProgrammingError(_error_msg)
        else:
            self._logger = connection.get_logger()
            if self._logger.level == logging.DEBUG:
                self._debug_header_messages = True

        if connection.connected() is False:
            _error_msg = 'Can not continue not connected to 4D SQL server!'
            self._logger.error(_error_msg)
            raise ProgrammingError(_error_msg)

        self._view = _python4DBIView
        self._connection = connection
        self._socket = connection.get_socket()

        # Log in to the to 4D SQL
        self._db_login()

    def __del__(self) -> None:
        """
        Destructor

        :return: None
        """
        self.close()

    def __next__(self) -> list:
        """
        Return the next result row

        :return: list
        :raises: StopIteration
        """
        result = self.fetch_one()
        if result is None:
            raise StopIteration
        return result

    def __iter__(self):
        """
        Used on python iterators

        :return: self
        """
        return self

    def __enter__(self):
        """
        Used on python 'with X() as x:' statement

        :return: self
        """
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        """
        Used on python 'with X() as x:' statement

        :param exc_type: type
        :param exc_val: value
        :param exc_tb: traceback

        :return: None
        """
        self.close()

    def _db_login(self) -> None:
        """
        Login to 4D SQL server

        :return: None
        :raises: InterfaceError
        """
        if self._connection.connected() is False:
            _error_msg = 'Can not login, not connect to 4D SQL server!'
            self._logger.error(_error_msg)
            raise InterfaceError(_error_msg)

        # Prepare the message
        if self._use_b64 is False:
            _msg = '%d LOGIN \r\n' \
                   'USER-NAME:%s\r\n' \
                   'USER-PASSWORD:%s\r\n' \
                   'PREFERRED-IMAGE-TYPES:%s\r\n' \
                   'REPLY-WITH-BASE64-TEXT:%s\r\n' \
                   'PROTOCOL-VERSION:%s\r\n\r\n' \
                   % (self._command_id,
                      self._connection.get_user(),
                      self._connection.get_password(),
                      self._preferred_image_types,
                      self._reply_with_b64,
                      self._protocol_version)
        else:
            _username = self._b64encode(string=self._connection.get_user())
            _password = self._b64encode(string=self._connection.get_password())
            _msg = '%d LOGIN \r\n' \
                   'USER-NAME-BASE64:%s\r\n' \
                   'USER-PASSWORD-BASE64:%s\r\n' \
                   'PREFERRED-IMAGE-TYPES:%s\r\n' \
                   'REPLY-WITH-BASE64-TEXT:%s\r\n' \
                   'PROTOCOL-VERSION:%s\r\n\r\n' \
                   % (self._command_id,
                      _username,
                      _password,
                      self._preferred_image_types,
                      self._reply_with_b64,
                      self._protocol_version)

        self._send_socket_data(msg=_msg)
        _data = self._receive_header()
        _data_dict = self._parse_header(data=_data)
        if self._error_code:
            _error_msg = 'Can not login to 4D SQL server : {} - {}'.format(
                self._error_code, self._error_description)
            self._logger.critical(_error_msg)
            raise InterfaceError(_error_msg)

        if 'Session-ID' in _data_dict:
            self._session_id = _data_dict['Session-ID']
        else:
            _error_msg = 'Can not find Session-ID!'
            self._logger.critical(_error_msg)
            raise InterfaceError(_error_msg)

        self._authenticated = True
        self._cursor_closed = False

        if self._debug_header_messages:
            self._print_header(msg=_msg, data=_data)

    def _db_logout(self) -> None:
        """
        Logout from 4D SQL server

        :return: None
        :raises: InterfaceError
        """
        if self._connection.connected() is False:
            _error_msg = 'Can not logout, not connect to 4D SQL server!'
            self._logger.error(_error_msg)
            raise InterfaceError(_error_msg)

        if self._authenticated is False:
            _error_msg = 'Can not logout, not authenticated to 4D SQL server!'
            self._logger.error(_error_msg)
            raise InterfaceError(_error_msg)

        # Prepare the message
        _msg = '%d LOGOUT\r\n\r\n' % self._command_id

        self._send_socket_data(msg=_msg)
        _data = self._receive_header()
        _ = self._parse_header(data=_data)
        if self._error_code:
            _error_msg = 'Can not logout from 4D SQL server : {} - {}'.format(
                self._error_code, self._error_description)
            self._logger.critical(_error_msg)
            raise InterfaceError(_error_msg)

        self._authenticated = False

        if self._debug_header_messages:
            self._print_header(msg=_msg, data=_data)

    def _db_quit(self) -> None:
        """
        Closes the current session from 4D SQL server

        :return: None
        :raises: InterfaceError
        """
        if self._connection.connected() is False:
            _error_msg = 'Can not quit, not connect to 4D SQL server!'
            self._logger.error(_error_msg)
            raise InterfaceError(_error_msg)

        if self._authenticated is True:
            self._db_logout()

        # Prepare the message
        _msg = '%d QUIT\r\n\r\n' % self._command_id

        self._send_socket_data(msg=_msg)
        _data = self._receive_header()
        _ = self._parse_header(data=_data)
        if self._error_code:
            _error_msg = 'Can not quit from 4D SQL server : {} - {}'.format(
                self._error_code, self._error_description)
            self._logger.critical(_error_msg)
            raise InterfaceError(_error_msg)

        self._cursor_closed = True

        if self._debug_header_messages:
            self._print_header(msg=_msg, data=_data)

    def close(self) -> None:
        """
        Close the current 4D SQL server cursor

        :return: None
        """
        if self._connection.connected() is True and self._cursor_closed is False:
            if 'Statement-ID' in self._statement_dict:
                self._close_statement()
            self._db_logout()
            self._db_quit()

    def _prepare_statement(self, query: str) -> None:
        """
        Uses the 4D SQL server engine to validate a statement

        :param query: str

        :return: None
        :raises: ProgrammingError, InterfaceError
        """
        if self._connection.connected() is False:
            _error_msg = 'Can not prepare the statement, not connect to 4D SQL server!'
            self._logger.error(_error_msg)
            raise InterfaceError(_error_msg)

        if self._authenticated is False:
            _error_msg = 'Can not prepare the statement, not authenticated to 4D SQL server!'
            self._logger.error(_error_msg)
            raise InterfaceError(_error_msg)

        if not isinstance(query, str):
            _error_msg = 'Can not prepare the statement, please check the query argument!'
            self._logger.error(_error_msg)
            raise ProgrammingError(_error_msg)

        if self._use_b64 is False:
            _msg = '%d PREPARE-STATEMENT\r\n' \
                   'STATEMENT:%s\r\n\r\n' \
                   % (self._command_id, query)
        else:
            _query = self._b64encode(string=query)
            _msg = '%d PREPARE-STATEMENT\r\n' \
                   'STATEMENT-BASE64:%s\r\n\r\n' \
                   % (self._command_id, _query)

        self._send_socket_data(msg=_msg)
        _data = self._receive_header()
        _ = self._parse_header(data=_data)
        if self._error_code:
            _error_msg = 'Can not prepare the statement => \'{}\' : {} - {}'.format(
                query, self._error_code, self._error_description)
            self._logger.critical(_error_msg)
            raise ProgrammingError(_error_msg)

        if self._debug_header_messages:
            self._print_header(msg=_msg, data=_data)

    def prepare_statement(self, query: str) -> int:
        """
        Checks if the statement is valid should always be execute before an execute statement
        returns FOURD_OK or FOURD_ERROR

        :param query: str

        :return: int
        :raises: ProgrammingError
        """
        if not isinstance(query, str):
            _error_msg = 'Can not continue please check the query argument!'
            self._logger.error(_error_msg)
            raise ProgrammingError(_error_msg)
        else:
            query = query.strip()

        try:
            self._prepare_statement(query=query)
        except Exception:
            return FOURD_ERROR

        return FOURD_OK

    def _execute_statement(self, query: str, page_size=_page_size) -> None:
        """
        Executes a statement on 4D SQL server

        :param query: str
        :param page_size: int

        :return: None
        :raises: ProgrammingError, InterfaceError
        """
        if self._connection.connected() is False:
            _error_msg = 'Can not execute the statement, not connect to 4D SQL server!'
            self._logger.error(_error_msg)
            raise InterfaceError(_error_msg)

        if self._authenticated is False:
            _error_msg = 'Can not execute the statement, not authenticated to 4D SQL server!'
            self._logger.error(_error_msg)
            raise InterfaceError(_error_msg)

        if not isinstance(query, str):
            _error_msg = 'Can not continue please check the query argument!'
            self._logger.error(_error_msg)
            raise ProgrammingError(_error_msg)

        if not isinstance(page_size, int):
            _error_msg = 'Can not continue please check the page_size argument!'
            self._logger.error(_error_msg)
            raise ProgrammingError(_error_msg)

        # START TRANSACTION, COMMIT, ROLLBACK, => Update-Count

        # The user can call the start transaction from execute
        if query.upper() == 'START TRANSACTION':
            if self._in_transaction is True:
                _error_msg = 'Already in a transaction!'
                self._logger.error(_error_msg)
                ProgrammingError(_error_msg)
            else:
                self._in_transaction = True

        # The user can call the commit or rollback from execute
        if query.upper() == 'COMMIT' or query.upper() == 'ROLLBACK':
            if self._in_transaction is False:
                _error_msg = 'You are not currently on a transaction!'
                self._logger.error(_error_msg)
                ProgrammingError(_error_msg)
            else:
                self._in_transaction = False

        # If a previous statement was opened close it
        # must be changed if multiple statements is implemented
        _internal_statements = ['START TRANSACTION', 'COMMIT', 'ROLLBACK'],
        if query.upper() not in _internal_statements:
            self._close_statement()

        # Always prepare a statement before execution
        self._prepare_statement(query=query)

        # Save the command of the current statement
        # can be used if multiple statements execution
        # is implemented.
        self._statement_cmd_id = self._command_id

        if self._use_b64 is False:
            _msg = '%d EXECUTE-STATEMENT\r\n' \
                   'STATEMENT:%s\r\n' \
                   'OUTPUT-MODE:%s\r\n' \
                   'FIRST-PAGE-SIZE:%i\r\n' \
                   'PREFERRED-IMAGE-TYPES:%s\r\n\r\n' \
                   % (self._statement_cmd_id,
                      query,
                      self._output_mode,
                      page_size,
                      self._preferred_image_types)
        else:
            _query = self._b64encode(string=query)
            _msg = '%d EXECUTE-STATEMENT\r\n' \
                   'STATEMENT-BASE64:%s\r\n' \
                   'OUTPUT-MODE:%s\r\n' \
                   'FIRST-PAGE-SIZE:%i\r\n' \
                   'PREFERRED-IMAGE-TYPES:%s\r\n\r\n' \
                   % (self._statement_cmd_id,
                      _query,
                      self._output_mode,
                      page_size,
                      self._preferred_image_types)

        self._send_socket_data(msg=_msg)
        _data = self._receive_header()
        _data_dict = self._parse_header(data=_data)
        if self._error_code:
            _error_msg = 'Can not execute the statement => \'{}\' : {} - {}'.format(
                query, self._error_code, self._error_description)
            self._logger.critical(_error_msg)
            raise ProgrammingError(_error_msg)

        self._build_statement_dict(data_dict=_data_dict)
        self._statement_dict = _data_dict
        self._statement_dict['Description'] = self._describe()

        if 'Result-Type' in _data_dict:
            if 'Update-Count' in _data_dict['Result-Type']:
                self._updated_row = self._receive_update_count()
                self._statement_dict['First-Row'] = 1
                self._statement_dict['Last-Row'] = self._statement_dict['Row-Count-Sent']
                self._rows = [[self._updated_row]]
            elif 'Result-Set' in _data_dict['Result-Type']:
                self._statement_dict['First-Row'] = 1
                self._statement_dict['Last-Row'] += self._statement_dict['Row-Count-Sent']
                self._rows = []
                self._parse_rows(self._statement_dict['Row-Count-Sent'])
            else:
                _error_msg = 'Result type not supported!'
                self._logger.critical(_error_msg)
                raise DatabaseError(_error_msg)

        if self._debug_header_messages:
            # print(self._statement_dict)
            self._logger.debug(self._statement_dict)
            self._print_header(msg=_msg, data=_data)

    def _close_statement(self) -> None:
        """
        Closes an open 4D SQL server statement

        :return: None
        :raises: ProgrammingError, InterfaceError
        """
        if self._connection.connected() is False:
            _error_msg = 'Can not close the statement, not connect to 4D SQL server!'
            self._logger.error(_error_msg)
            raise InterfaceError(_error_msg)

        if self._authenticated is False:
            _error_msg = 'Can not close the statement, not authenticated to 4D SQL server!'
            self._logger.error(_error_msg)
            raise InterfaceError(_error_msg)

        if 'Statement-ID' in self._statement_dict:

            # Prepare the message
            _msg = '%d CLOSE-STATEMENT\r\n' \
                   'STATEMENT-ID:%d\r\n\r\n' \
                   % (self._command_id,
                      self._statement_dict['Statement-ID'])

            self._send_socket_data(msg=_msg)
            _data = self._receive_header()
            _ = self._parse_header(data=_data)
            if self._error_code:
                _error_msg = 'Can not close the statement from 4D SQL server : {} - {}'.format(
                    self._error_code, self._error_description)
                self._logger.critical(_error_msg)
                raise InterfaceError(_error_msg)

            if self._debug_header_messages:
                self._print_header(msg=_msg, data=_data)

        self._statement_dict = {}
        self._updated_row = -1
        self._rows = []

    def _fetch_result(self, first_row: int, last_row: int) -> None:
        """
        Fetch a new result page for the current statement

        :param first_row: int
        :param last_row: int

        :return: None
        :raises: ProgrammingError, InterfaceError
        """
        if self._connection.connected() is False:
            _error_msg = 'Can not fetch result, not connect to 4D SQL server!'
            self._logger.error(_error_msg)
            raise InterfaceError(_error_msg)

        if self._authenticated is False:
            _error_msg = 'Can not fetch result, not authenticated to 4D SQL server!'
            self._logger.error(_error_msg)
            raise InterfaceError(_error_msg)

        if not isinstance(first_row, int):
            _error_msg = 'Can not continue please check the first_row argument!'
            self._logger.error(_error_msg)
            raise ProgrammingError(_error_msg)

        if not isinstance(last_row, int):
            _error_msg = 'Can not continue please check the last_row argument!'
            self._logger.error(_error_msg)
            raise ProgrammingError(_error_msg)

        if 'Statement-ID' not in self._statement_dict:
            _error_msg = 'Can not fetch result, an opened statement to 4D SQL server was not found!'
            self._logger.error(_error_msg)
            raise InterfaceError(_error_msg)

        # Prepare the message
        _msg = '%d FETCH-RESULT\r\n' \
               'STATEMENT-ID:%d\r\n' \
               'COMMAND-INDEX:%d\r\n' \
               'FIRST-ROW-INDEX:%d\r\n' \
               'LAST-ROW-INDEX:%d\r\n' \
               'OUTPUT-MODE:%s\r\n\r\n' \
               % (self._command_id,
                  self._statement_dict['Statement-ID'],
                  self._statement_dict['Command-Count'] - 1,
                  first_row,
                  last_row,
                  self._output_mode)

        self._send_socket_data(msg=_msg)
        _data = self._receive_header()
        _ = self._parse_header(data=_data)
        if self._error_code:
            _error_msg = 'Can not execute the fetch result => \'{}\' : {} - {}'.format(
                self._statement_dict['Statement-ID'], self._error_code, self._error_description)
            self._logger.critical(_error_msg)
            raise ProgrammingError(_error_msg)

        _n_rows = last_row - first_row + 1
        self._parse_rows(_n_rows)

        if self._debug_header_messages:
            self._print_header(msg=_msg, data=_data)

    @staticmethod
    def _clean_list(data_list: list) -> None:
        """
        Remove empty spaces and null str from a pythons list
        ['',OBJ, OBJ,' '] => [OBJ,OBJ]

        :param data_list: list

        :return: None
        """
        if data_list:
            while '' in data_list:
                data_list.remove('')
            while ' ' in data_list:
                data_list.remove(' ')

    def _replace_nth(self, source: str, search: str, replace: str, pos: int) -> str:
        """
        Find the Nth occurrence of a string, and replace it with another.

        :param source: str
        :param search: str
        :param replace: str
        :param pos: int

        :return: str
        :raises: ProgrammingError
        """
        if not isinstance(source, str):
            _error_msg = 'Can not continue please check the source argument!'
            self._logger.error(_error_msg)
            raise ProgrammingError(_error_msg)

        if not isinstance(search, str):
            _error_msg = 'Can not continue please check the search argument!'
            self._logger.error(_error_msg)
            raise ProgrammingError(_error_msg)

        if not isinstance(replace, str):
            _error_msg = 'Can not continue please check the replace argument!'
            self._logger.error(_error_msg)
            raise ProgrammingError(_error_msg)

        if not isinstance(pos, int):
            _error_msg = 'Can not continue please check the pos argument!'
            self._logger.error(_error_msg)
            raise ProgrammingError(_error_msg)

        i = -1
        for _ in range(pos):
            i = source.find(search, i + len(search))
            # Return an unmodified string if there are not n occurrences of value
            if i == -1:
                return source

        return '{}{}{}'.format(source[:i], replace, source[i + len(search):])

    def _replace_first_from(self, source: str, search: str, replace: str, pos: int) -> str:
        """
        Find the first occurrence of a string from start @ pos, and replace it with another.

        :param source: str
        :param search: str
        :param replace: str
        :param pos: int

        :return: str
        :raises: ProgrammingError
        """
        if not isinstance(source, str):
            _error_msg = 'Can not continue please check the source argument!'
            self._logger.error(_error_msg)
            raise ProgrammingError(_error_msg)

        if not isinstance(search, str):
            _error_msg = 'Can not continue please check the search argument!'
            self._logger.error(_error_msg)
            raise ProgrammingError(_error_msg)

        if not isinstance(replace, str):
            _error_msg = 'Can not continue please check the replace argument!'
            self._logger.error(_error_msg)
            raise ProgrammingError(_error_msg)

        if not isinstance(pos, int):
            _error_msg = 'Can not continue please check the pos argument!'
            self._logger.error(_error_msg)
            raise ProgrammingError(_error_msg)

        i = source.find(search, pos)
        # Return an unmodified string if there are not n occurrences of value
        if i == -1:
            return source

        return '{}{}{}'.format(source[:i], replace, source[i + len(search):])

    def _b64encode(self, string: str) -> str:
        """
        Converts a string to BASE64

        :param string: str

        :return: str
        :raises: ProgrammingError
        """
        if not isinstance(string, str):
            _error_msg = 'Can not continue please check the string argument!'
            self._logger.error(_error_msg)
            raise ProgrammingError(_error_msg)

        if string:
            _string = string.encode(self._encoding)
            _string = base64.b64encode(_string).decode(self._encoding)
            return _string

        return string

    def _4d_to_python_type(self, param_type: str) -> object:
        """
        Returns the equivalent python type from 4D SQL server VK's

        :param param_type: str

        :return: object
        :raises: ProgrammingError
        """
        if not isinstance(param_type, str):
            _error_msg = 'Can not continue please check the param_type argument!'
            self._logger.error(_error_msg)
            raise ProgrammingError(_error_msg)

        return self._4d_to_python_types[param_type]

    def _python_to_4d_type(self, param_type: object) -> str:
        """
        Returns the equivalent 4D SQL VK's type from python type

        :param param_type: object

        :return: str
        :raises: ProgrammingError
        """
        if not isinstance(param_type, object):
            _error_msg = 'Can not continue please check the param_type argument!'
            self._logger.error(_error_msg)
            raise ProgrammingError(_error_msg)

        if param_type:
            if param_type == bool:
                return 'VK_BOOLEAN'
            if param_type == int:
                return 'VK_LONG8'
            if param_type == float:
                return 'VK_REAL'
            if param_type == str:
                return 'VK_STRING'

        _error_msg = 'Type: ' + str(param_type) + ' not supported in query!'
        self._logger.critical(_error_msg)
        raise ProgrammingError(_error_msg)

    def _send_socket_data(self, msg: str) -> None:
        """
        Sends data to socket

        :param msg: str

        :return: None
        :raises: ProgrammingError
        """
        if not isinstance(msg, str):
            _error_msg = 'Can not continue please check the msg argument!'
            self._logger.error(_error_msg)
            raise ProgrammingError(_error_msg)

        self._socket.send(msg.encode(self._encoding))

    def _receive_socket_data(self, n: int) -> bytearray:
        """
        Receives data from socket

        :param n: int

        :return: bytearray
        """
        return bytearray(self._socket.recv(n))

    def _receive_header(self) -> bytearray:
        """
        Receives an header from 4D SQL server socket buffer

        :return: bytearray
        """
        _data = bytearray()
        _end_of_header = b'\r\n\r\n'
        while _end_of_header not in _data:
            _data = _data + bytearray(self._socket.recv(1))
        return _data

    def _parse_header(self, data: bytearray) -> dict:
        """
        Parse an 4D SQL server header
        Keys expected to be found are
        Error - for an error
        OK - for a correct response

        :param data: bytearray

        :return: dict
        :raises: ProgrammingError, DatabaseError
        """
        if not isinstance(data, bytearray):
            _error_msg = 'Can not continue please check the data argument!'
            self._logger.error(_error_msg)
            raise ProgrammingError(_error_msg)

        if data:
            _data_string = data.decode(self._encoding)
            _data_list = _data_string.split('\r\n')
            _data_dict = self._create_header_dict(data_list=_data_list)
            if 'ERROR' in _data_string.upper():
                if 'Error-Code' in _data_dict.keys():
                    self._error_code = int(_data_dict['Error-Code'])
                    if 'Error-Description' in _data_dict.keys():
                        self._error_description = _data_dict['Error-Description']
                    else:
                        self._error_description = ''
                else:
                    _error_msg = str(_data_dict)
                    self._logger.critical(_error_msg)
                    raise DatabaseError(_error_msg)
            else:
                if not ('OK' in _data_string):
                    _error_msg = 'Can not parse header unknown error : ' + _data_string
                    self._logger.critical(_error_msg)
                    raise DatabaseError(_error_msg)
                else:
                    return _data_dict

    def _create_header_dict(self, data_list: list) -> dict:
        """
        Creates a python dict from an 4D SQL server header list

        :param data_list: list

        :return: dict
        :raises: ProgrammingError
        """
        if not isinstance(data_list, list):
            _error_msg = 'Can not continue please check the data_list argument!'
            self._logger.error(_error_msg)
            raise ProgrammingError(_error_msg)

        _data_dict = {}
        if data_list:
            for _el in data_list:
                if ':' in _el:
                    _temp_list = _el.split(':')
                    _data_dict[_temp_list[0]] = _temp_list[1].strip()
        return _data_dict

    def _print_header(self, msg: str, data: bytearray) -> None:
        """
        Prints the content of a 4D SQL server header message

        :param msg: str
        :param data: bytearray

        :return: None
        :raises: ProgrammingError
        """
        if not isinstance(msg, str):
            _error_msg = 'Can not continue please check the msg argument!'
            self._logger.error(_error_msg)
            raise ProgrammingError(_error_msg)

        if not isinstance(data, bytearray):
            _error_msg = 'Can not continue please check the data argument!'
            self._logger.error(_error_msg)
            raise ProgrammingError(_error_msg)

        if msg and data:
            _msg = msg.replace('\r\n\r\n', '')
            _msg = 'MSG SENT: \n' + _msg + '\n'
            self._logger.debug('\n' + _msg)
            # print('MSG SENT: \n' + _msg)

            _msg = data.decode(self._encoding)
            _msg = _msg.replace('\r\n\r\n', '')
            _msg = 'HEADER RECEIVED: \n' + _msg + '\n'
            self._logger.debug('\n' + _msg)
            # print(_msg)

    def _build_statement_dict(self, data_dict: dict) -> None:
        """
        Creates a python dict from an 4D SQL server statement header
        should only be used on EXECUTE-STATEMENT or FETCH-RESULT

        :param data_dict: dict

        :return:None
        :raises: ProgrammingError
        """
        if not isinstance(data_dict, dict):
            _error_msg = 'Can not continue please check the data_dict argument!'
            self._logger.error(_error_msg)
            raise ProgrammingError(_error_msg)

        if data_dict:
            _col_names = base64.b64decode(data_dict['Column-Aliases-Base64']).decode(self._encoding)
            _col_names = _col_names.replace('[', '').replace(']', '')
            _col_names = _col_names.split(' ')
            self._clean_list(_col_names)
            data_dict['Column-Aliases'] = _col_names
            data_dict.pop('Column-Aliases-Base64')
            _col_types = data_dict['Column-Types'].split(' ')
            self._clean_list(data_list=_col_types)
            data_dict['Column-Types'] = _col_types
            _col_updateability = data_dict['Column-Updateability'].split(' ')
            self._clean_list(data_list=_col_updateability)
            data_dict['Column-Updateability'] = _col_updateability
            data_dict['Column-Count'] = int(data_dict['Column-Count'])
            data_dict['Command-Count'] = int(data_dict['Command-Count'])
            data_dict['Statement-ID'] = int(data_dict['Statement-ID'])
            data_dict['Row-Count'] = int(data_dict['Row-Count'])
            data_dict['Row-Count-Sent'] = int(data_dict['Row-Count-Sent'])
            _result_type = data_dict['Result-Type'].split(' ')
            self._clean_list(data_list=_result_type)
            data_dict['Result-Type'] = _result_type
            data_dict['First-Row'] = 0
            data_dict['Last-Row'] = 0

    def _describe(self) -> list:
        """
        Builds the col result descriptions
        [(name,py_type),...(n,n]
        should only be used on EXECUTE-STATEMENT

        :return: list
        """
        _description = []
        if 'Column-Aliases' in self._statement_dict and 'Column-Types' in self._statement_dict:
            _col_names = self._statement_dict['Column-Aliases']
            _col_types = self._statement_dict['Column-Types']
            for i in range(0, len(_col_types)):
                _col_description = (_col_names[i], self._4d_to_python_type(_col_types[i]))
                _description.append(_col_description)
        return _description

    @property
    def _command_id(self) -> int:
        """
        Increments the command ID used by 4D DB SQL server engine to identify the commands idx
        LOGIN, LOGOUT, QUIT, EXECUTE-STATEMENT, FETCH-RESULT
        START-TRANSACTION, COMMIT, ROLLBACK

        :return: int
        """
        self._cmd_id = self._cmd_id + 1
        return self._cmd_id

    @property
    def row_number(self) -> Union[int, None]:
        """
        This read-only attribute provides the current 0-based index of the cursor in the result set
        or None if the index cannot be determined

        :return: int or None
        """
        if 'Statement-ID' in self._statement_dict:
            return self._statement_dict['Last-Row']
        return None

    @property
    def description(self) -> list:
        """
        A Cursor object's description attribute returns information about each of the result columns of a query.

        :return: list
        """
        if 'Statement-ID' in self._statement_dict:
            return self._statement_dict['Description']
        return []

    def _receive_char(self) -> str:
        """
        Unpacks a str object from the 4D SQl server socket buffer

        :return: str
        """
        return unpack(self._fmt + 'c', self._receive_socket_data(1))[0]

    def _receive_signed_char(self) -> int:
        """
        Unpacks an int object from the 4D SQl server socket buffer

        :return: int
        """
        return unpack(self._fmt + 'b', self._receive_socket_data(1))[0]

    def _receive_unsigned_char(self) -> int:
        """
        Unpacks an int object from the 4D SQl server socket buffer

        :return: int
        """
        return unpack(self._fmt + 'B', self._receive_socket_data(1))[0]

    def _receive_bool(self) -> int:
        """
        Unpacks an int object from the 4D SQl server socket buffer

        :return: int
        """
        return unpack(self._fmt + '?', self._receive_socket_data(1))[0]

    def _receive_short(self) -> int:
        """
        Unpacks an int object from the 4D SQl server socket buffer

        :return: int
        """
        return unpack(self._fmt + 'h', self._receive_socket_data(2))[0]

    def _receive_unsigned_short(self) -> int:
        """
        Unpacks an int object from the 4D SQl server socket buffer

        :return: int
        """
        return unpack(self._fmt + 'H', self._receive_socket_data(2))[0]

    def _receive_int(self) -> int:
        """
        Unpacks an int object from the 4D SQl server socket buffer

        :return: int
        """
        return unpack(self._fmt + 'i', self._receive_socket_data(4))[0]

    def _receive_unsigned_int(self) -> int:
        """
        Unpacks an int object from the 4D SQl server socket buffer

        :return: int
        """
        return unpack(self._fmt + 'I', self._receive_socket_data(4))[0]

    def _receive_long(self) -> int:
        """
        Unpacks an int object from the 4D SQl server socket buffer

        :return: int
        """
        return unpack(self._fmt + 'l', self._receive_socket_data(4))[0]

    def _receive_unsigned_long(self) -> int:
        """
        Unpacks an int object from the 4D SQl server socket buffer

        :return: int
        """
        return unpack(self._fmt + 'L', self._receive_socket_data(4))[0]

    def _receive_long_long(self) -> int:
        """
        Unpacks an int object from the 4D SQl server socket buffer

        :return: int
        """
        return unpack(self._fmt + 'q', self._receive_socket_data(8))[0]

    def _receive_unsigned_long_long(self) -> int:
        """
        Unpacks an int object from the 4D SQl server socket buffer

        :return: int
        """
        return unpack(self._fmt + 'Q', self._receive_socket_data(8))[0]

    def _receive_double(self) -> float:
        """
        Unpacks a float object from the 4D SQl server socket buffer

        :return: float
        """
        return unpack(self._fmt + 'd', self._receive_socket_data(8))[0]

    def _receive_sign(self) -> int:
        """
        Receives an int object from the 4D SQl server socket buffer

        :return: int
        """
        return self._receive_signed_char()

    def _receive_update_count(self) -> int:
        """
        Receives an int object from the 4D SQl server socket buffer

        :return: int
        """
        return self._receive_vk_long8()

    def _receive_status_code(self) -> int:
        """
        Receives a char object from the 4D SQl server socket buffer

        0 => Null value
        1 => Value
        2 => Error during during read of data stream
        Other => Status code not supported

        :return: int
        """
        temp = ord(self._receive_char().decode())

        # '0' or 'O' 0 => Null value
        if temp == 48 or temp == 79:
            temp = 0

        # '1' => Value
        if temp == 49:
            temp = 1

        # '2' => Error during during read of data stream
        if temp == 50:
            temp = 2

        return temp

    def _receive_row_id(self) -> int:
        """
        Receives an int object from the 4D SQl server socket buffer

        :return: int
        """
        return self._receive_int()

    def _receive_vk_boolean(self) -> bool:
        """
        Receives an int object from the 4D SQl server socket buffer

        :return: bool
        """
        return bool(self._receive_short())

    def _receive_vk_byte(self) -> int:
        """
        Receives an int object from the 4D SQl server socket buffer

        :return: int
        """
        return self._receive_short()

    def _receive_vk_word(self) -> int:
        """
        Receives an int object from the 4D SQl server socket buffer

        :return: int
        """
        return self._receive_short()

    def _receive_vk_long(self) -> int:
        """
        Receives an int object from the 4D SQl server socket buffer

        :return: int
        """
        return self._receive_long()

    def _receive_vk_long8(self) -> int:
        """
        Receives an int object from the 4D SQl server socket buffer

        :return: int
        """
        return self._receive_long_long()

    def _receive_vk_real(self) -> float:
        """
        Receives a float object from the 4D SQl server socket buffer

        :return: float
        """
        return self._receive_double()

    def _receive_vk_float(self) -> float:
        """
        Receives a float object from the 4D SQl server

        :return: float
        """
        _exp = self._receive_long()
        _sign = self._receive_sign()
        _data_len = self._receive_long()
        _the_data = self._receive_socket_data(_data_len)
        _num = "0."
        for _el in _the_data:
            _num = _num + str(_el)
        _num = float(_num) * _sign * pow(10, _exp)
        return _num

    def _receive_vk_timestamp(self) -> Union[datetime.datetime, None]:
        """
        Receives a datetime.datetime object from the 4D SQl server socket buffer

        :return: datetime.datetime or None
        """
        _year = self._receive_unsigned_short()
        _month = self._receive_unsigned_char()
        _day = self._receive_unsigned_char()
        _milliseconds = self._receive_unsigned_long()
        _milliseconds = timedelta(milliseconds=_milliseconds)
        if _year == 0 or _month == 0 or _day == 0:
            return None
        try:
            _date = datetime.datetime(year=_year, month=_month, day=_day)
            _date_time = _date + _milliseconds
            return _date_time
        except Exception:
            return None

    def _receive_vk_time(self) -> time:
        """
        Receives a time object from the 4D SQl server socket buffer

        :return: time
        """
        _duration = self._receive_vk_duration()
        if _duration:
            _date = datetime.datetime(year=1, month=1, day=1)
            _date_time = _date + _duration
            _time = _date_time.time()
            return _time
        else:
            return time(0, 0, 0)

    def _receive_vk_duration(self) -> timedelta:
        """
        Receives a timedelta object from the 4D SQl socket buffer

        :return: timedelta
        """
        _milliseconds = self._receive_unsigned_long_long()
        return timedelta(milliseconds=_milliseconds)

    def _receive_vk_string(self) -> str:
        """
        Receives a string object from the 4D SQl socket buffer

        :return: str
        """
        _len = abs(self._receive_int())
        _string = self._receive_socket_data(_len * 2)
        _exception = None

        # Try to decode
        # vk_string should be always UTF-16LE as per docs, but if cant decode
        # try the fallback's
        _temp_string = ''
        for _encoding in self._vk_string_encodings:

            _decode_with_error = False
            try:
                _temp_string = _string.decode(_encoding)
            except Exception as e:
                # Register the first exception
                if _exception is None:
                    _exception = e
                _temp_string = ''
                _decode_with_error = True

            # Decoded with success
            if _decode_with_error is False:
                break

        # If can not decode raise the first exception since the
        # default encoding should be always UTF-16LE
        if _exception:
            raise _exception

        _string = _temp_string

        return _string

    def _receive_vk_text(self) -> str:
        """
        Receives a string object from the 4D SQl server socket buffer

        :return: str
        """
        return self._receive_vk_string()

    def _receive_vk_blob(self) -> bytes:
        """
        Receives a bytes object from the 4D SQl server socket buffer

        :return: bytes
        """
        _data_len = self._receive_unsigned_long()
        return self._receive_socket_data(_data_len)

    def _receive_vk_image(self) -> bytes:
        """
        Receives an image bytes object from the 4D SQl server socket buffer

        :return: bytes
        """
        _data_len = self._receive_unsigned_long()
        return self._receive_socket_data(_data_len)

    @staticmethod
    def _receive_vk_unknown() -> None:
        """
        Receives a null value

        :return: None
        """
        return None

    def _parse_rows(self, n: int) -> None:
        """
        Should always be executed after an execute statement of type result-set
        Receives the page size (n) data

        :param n: int

        :return: None
        :raises: IntegrityError
        """
        _num_of_rows = n
        _num_of_cols = self._statement_dict['Column-Count']

        for _row_idx in range(0, _num_of_rows):

            if 'Y' in self._statement_dict['Column-Updateability']:
                _status_code = self._receive_status_code()

                if _status_code == 0:
                    _ = None  # row ID is null - Not being used
                elif _status_code == 1:
                    _ = self._receive_row_id()  # row ID - Not being used
                elif _status_code == 2:
                    _error_code = self._fetch_col_value('VK_LONG8')
                    _error_msg = 'Error {}: reading the stream data!'.format(_error_code)
                    self._logger.critical(_error_msg)
                    raise IntegrityError(_error_msg)
                else:
                    _error_msg = 'Status code ' + str(_status_code) + ' not supported in data at row ' \
                                 + str(_row_idx) + '!'
                    self._logger.critical(_error_msg)
                    raise IntegrityError(_error_msg)

            _row = []
            for _col_idx in range(0, _num_of_cols):
                _status_code = self._receive_status_code()
                _col_name = self._statement_dict['Column-Aliases'][_col_idx]
                _col_value = None

                if _status_code == 0:
                    _col_value = None
                elif _status_code == 1:
                    _col_type = self._statement_dict['Column-Types'][_col_idx]
                    _col_value = self._fetch_col_value(_col_type)
                elif _status_code == 2:
                    _error_code = self._fetch_col_value('VK_LONG8')
                    _error_msg = 'Error {}: reading the stream data!'.format(_error_code)
                    self._logger.critical(_error_msg)
                    raise IntegrityError(_error_msg)
                else:
                    _error_msg = 'Status code ' + str(_status_code) + ' not supported in data at row ' + str(
                        _row_idx) + 'column ' + _col_name + ' !'
                    self._logger.critical(_error_msg)
                    raise IntegrityError(_error_msg)
                _row.append(_col_value)

            self._rows.append(_row)

    def _fetch_col_value(self, col_type: str) -> object:
        """
        Helper of _parse_rows returns the VK python object type

        :param col_type: str

        :return: object
        """

        if col_type:
            if col_type == 'VK_BOOLEAN':
                return self._receive_vk_boolean()
            if col_type == 'VK_BYTE':
                return self._receive_vk_byte()
            if col_type == 'VK_WORD':
                return self._receive_vk_word()
            if col_type == 'VK_LONG':
                return self._receive_vk_long()
            if col_type == 'VK_LONG8':
                return self._receive_vk_long8()
            if col_type == 'VK_REAL':
                return self._receive_vk_real()
            if col_type == 'VK_FLOAT':
                return self._receive_vk_float()
            if col_type == 'VK_TIME':
                return self._receive_vk_timestamp()
            if col_type == 'VK_TIMESTAMP':
                return self._receive_vk_timestamp()
            if col_type == 'VK_DURATION':
                return self._receive_vk_time()
            if col_type == 'VK_TEXT':
                return self._receive_vk_text()
            if col_type == 'VK_STRING':
                return self._receive_vk_string()
            if col_type == 'VK_BLOB':
                return self._receive_vk_blob()
            if col_type == 'VK_IMAGE':
                return self._receive_vk_image()
            if col_type == 'VK_UNKNOWN':
                return self._receive_vk_unknown()
        return None

    @property
    def row_count(self) -> int:
        """
        This read-only attribute specifies the number of rows that the last .execute*()

        :return: int
        """
        if 'Statement-ID' in self._statement_dict:
            return self._statement_dict['Row-Count']
        return 0

    def set_input_sizes(self, size: int) -> None:
        """
        Not implemented!
        This can be used before a call to .execute*() to predefine memory areas for the operation's parameters.

        :param size:

        :return: None
        """
        pass

    def set_output_size(self, size: int) -> None:
        """
        Not implemented!
        Set a column buffer size for fetches of large columns (e.g. LONGs, BLOBs, etc.).
        the column is specified as an index into the result sequence.
        Not specifying the column will set the default size for all large columns in the cursor.

        :param size: int

        :return: None
        """
        pass

    def _parse_execute_params(self, params: dict, query: str) -> str:
        """
        Parse the query execute params

        Supports all the paramstyles
        paramstyle - Meaning
        qmark	- Question mark style, e.g. ...WHERE name=?
        named	- Named style, e.g. ...WHERE name=:name
        format - ANSI C printf format codes, e.g. ...WHERE name=%s
        pyformat - Python extended format codes, e.g. ...WHERE name=%(name)s

        :param params: dict
        :param query: str

        :return: str
        """
        # Start convert query variables to qmark
        # paramstyle - Meaning
        # qmark	- Question mark style, e.g. ...WHERE name=?
        # named	- Named style, e.g. ...WHERE name=:name
        # format - ANSI C printf format codes, e.g. ...WHERE name=%s
        # pyformat - Python extended format codes, e.g. ...WHERE name=%(name)s
        if isinstance(params, dict):
            _new_params = []

            # See if we are using pyformat parameters %(name)s
            _regex = re.compile('\%\(([^\)]+)\)s')
            for _key in re.findall(_regex, query):
                # Will raise key error if the query string argument is not in params
                _new_params.append(params[_key])

            # We didn't match anything in the query string
            # Try named named parameters instead :name
            if not _new_params:
                _regex = re.compile(':([A-Za-z0-9]+)')
                for _key in re.findall(_regex, query):
                    _new_params.append(params[_key])

            # We didn't match anything in the query string
            # Try named format parameters instead %name
            if not _new_params:
                _regex = re.compile('%([A-Za-z0-9]+)')
                for _key in re.findall(_regex, query):
                    _new_params.append(params[_key])

            query = re.sub(_regex, '?', query)
            params = _new_params

        # Replace double-quotes with single quote
        query.replace('%%', '%')

        # If any parameter is a tuple, we need to modify the query string and
        # make multiple passes through the parameters, breaking out one tuple/list
        # each time.
        while True:
            found_tuple = False
            for idx, param in enumerate(params):
                if type(param) == list or type(param) == tuple:
                    found_tuple = True
                    param_len = len(param)
                    # Need 1 based count
                    query = self._replace_nth(query, '?', '({})'.format(','.join('?' * param_len)), idx + 1)
                    params = tuple(params[:idx]) + tuple(param) + tuple(params[idx + 1:])
                    # Only handle one tuple at a time, otherwise the idx parameter is off
                    break

            if not found_tuple:
                break

        # Convert all qmark variables to values
        _last_pos = 1
        for _el in params:
            if _el is None:
                _el = '\'' + '\''
            elif isinstance(_el, str):
                _el = '\'' + _el + '\''
            elif isinstance(_el, bool):
                _el = str(_el)
            elif isinstance(_el, int) or isinstance(_el, float):
                _el = str(_el)
            elif isinstance(_el, datetime.time):
                _el = '\'' + _el.isoformat() + '\''
            elif isinstance(_el, datetime.date):
                _el = '\'' + _el.isoformat() + '\''
            elif isinstance(_el, datetime.datetime):
                _el = '\'' + _el.isoformat() + '\''
            elif isinstance(_el, tuple):
                _el = '\'' + str(_el) + '\''
            else:
                _el = '\'' + str(_el) + '\''
            query = self._replace_first_from(query, '?', _el, _last_pos)
            _last_pos = query.find(_el, _last_pos) + len(_el)

        return query

    def execute(self, query: str, params=dict(), page_size=_page_size, on_before_execute=None,
                on_executed=None, *args, **kwargs) -> None:
        """
        Prepare and execute a database operation (query or command).

        :param query: str
        :param params: dict
        :param page_size: int
        :param on_before_execute: object (function) or [object (function), object (function), ..., object (function)]
        :param on_executed: object (function) or [object (function), object (function), ..., object (function)]

        :return: None
        :raises: ProgrammingError
        """
        _on_before_execute_handler = None
        _on_executed_handler = None

        if not isinstance(query, str):
            _error_msg = 'Can not continue, please check the query argument!'
            self._logger.error(_error_msg)
            raise ProgrammingError(_error_msg)
        else:
            query = query.strip()

        if not isinstance(params, dict):
            _error_msg = 'Can not continue, please check the params argument!'
            self._logger.error(_error_msg)
            raise ProgrammingError(_error_msg)

        if not isinstance(page_size, int):
            _error_msg = 'Can not continue, please check the page_size argument!'
            self._logger.error(_error_msg)
            raise ProgrammingError(_error_msg)

        if self._connection.connected() is False:
            _error_msg = 'Can not continue, not connected to 4D SQL server!'
            self._logger.error(_error_msg)
            raise OperationalError(_error_msg)

        if self._cursor_closed:
            _error_msg = 'Can not continue, cursor already closed!'
            self._logger.error(_error_msg)
            raise ProgrammingError(_error_msg)

        if on_before_execute:
            _on_before_execute_handler = _python4DEventHook()
            if hasattr(on_before_execute, '__call__'):
                _on_before_execute_handler += on_before_execute
            else:
                if isinstance(on_before_execute, list):
                    for el in on_before_execute:
                        if hasattr(on_before_execute, '__call__'):
                            _on_before_execute_handler += el
                        else:
                            _error_msg = 'Can not continue, please check the on_before_execute argument!'
                            self._logger.error(_error_msg)
                            raise ProgrammingError(_error_msg)

        if on_executed:
            _on_executed_handler = _python4DEventHook()
            if hasattr(on_executed, '__call__'):
                _on_executed_handler += on_executed
            else:
                for el in on_executed:
                    if hasattr(on_executed, '__call__'):
                        _on_executed_handler += el
                    else:
                        _error_msg = 'Can not continue, please check the on_execute_ready argument!'
                        self._logger.error(_error_msg)
                        raise ProgrammingError(_error_msg)

        # Put query params into query string
        query = self._parse_execute_params(params=params, query=query)

        # Event handlers
        if _on_before_execute_handler:
            _on_before_execute_handler.fire(*args, **kwargs)

        self._execute_statement(query, page_size)
        if 'Statement-ID' in self._statement_dict:
            self._rows = self.fetch_many(page_size)

        # Event handlers
        if _on_executed_handler:
            _on_executed_handler.fire(*args, **kwargs)

    def fetch_one(self) -> Union[list, None]:
        """
        Fetch the next row of a query result set, returning a single sequence, or None when no more data is available.

        :return: None
        :raises: InterfaceError
        """
        if self._connection.connected() is False:
            _error_msg = 'Can not fetch, not connect to 4D SQL server!'
            self._logger.error(_error_msg)
            raise InterfaceError(_error_msg)

        if self._authenticated is False:
            _error_msg = 'Can not fetch, not authenticated to 4D SQL server!'
            self._logger.error(_error_msg)
            raise InterfaceError(_error_msg)

        if 'Statement-ID' not in self._statement_dict:
            _error_msg = 'Can not fetch, an opened statement to 4D SQL server was not found!'
            self._logger.critical(_error_msg)
            raise InterfaceError(_error_msg)

        if len(self._rows) > 0:
            return self._rows.pop(0)
        else:
            # Try to fetch the next result page
            if self._statement_dict['Last-Row'] < self._statement_dict['Row-Count']:
                _statement_page_size = self._statement_dict['Row-Count-Sent']
                self._statement_dict['First-Row'] = self._statement_dict['Last-Row']
                self._statement_dict['Last-Row'] += _statement_page_size
                if self._statement_dict['Last-Row'] > self._statement_dict['Row-Count']:
                    self._statement_dict['Last-Row'] = self._statement_dict['Row-Count']
                _statement_first_row = self._statement_dict['First-Row']
                _statement_last_row = self._statement_dict['Last-Row']
                self._fetch_result(_statement_first_row, _statement_last_row-1)
                if len(self._rows) > 0:
                    return self._rows.pop(0)

        return None

    def fetch_many(self, size: int) -> Union[list, None]:
        """
        Fetch the next set of rows of a query result, returning a sequence of sequences (e.g. a list of tuples).
        An empty sequence is returned when no more rows are available.

        :param size: int

        :return: list
        :raises: ProgrammingError, InterfaceError
        """
        if not isinstance(size, int):
            _error_msg = 'Can not continue, please check the size argument!'
            self._logger.error(_error_msg)
            raise ProgrammingError(_error_msg)

        if self._connection.connected() is False:
            _error_msg = 'Can not fetch, not connect to 4D SQL server!'
            self._logger.error(_error_msg)
            raise InterfaceError(_error_msg)

        if self._authenticated is False:
            _error_msg = 'Can not fetch many, not authenticated to 4D SQL server!'
            self._logger.error(_error_msg)
            raise InterfaceError(_error_msg)

        if 'Statement-ID' not in self._statement_dict:
            _error_msg = 'Can not fetch many, an opened statement to 4D SQL server was not found!'
            self._logger.critical(_error_msg)
            raise InterfaceError(_error_msg)

        _result_set = []
        for _ in range(size):
            # Do not use try "fetch_one" to speed up the operation
            _row = self.fetch_one()
            if _row is None:
                break
            _result_set.append(_row)

        return _result_set

    def fetch_all(self) -> Union[list, None]:
        """
        Fetch all (remaining) rows of a query result.
        Note that the cursor's array size attribute can affect the performance of this operation.

        :return: list
        :raises: InterfaceError
        """

        if self._connection.connected() is False:
            _error_msg = 'Can not fetch all, not connect to 4D SQL server!'
            self._logger.error(_error_msg)
            raise InterfaceError(_error_msg)

        if self._authenticated is False:
            _error_msg = 'Can not fetch all, not authenticated to 4D SQL server!'
            self._logger.error(_error_msg)
            raise InterfaceError(_error_msg)

        if 'Statement-ID' not in self._statement_dict:
            _error_msg = 'Can not fetch result, an opened statement to 4D SQL server was not found!'
            self._logger.critical(_error_msg)
            raise InterfaceError(_error_msg)

        _result_set = []
        while True:
            # Do not use try "fetch_one" to speed up the operation
            _row = self.fetch_one()
            if _row is None:
                break
            _result_set.append(_row)

        return _result_set

    def _start_transaction(self) -> None:
        """
        Opens a transaction

        :return: None
        :raises: ProgrammingError
        """
        if self._in_transaction is True:
            _error_msg = 'Already in a transaction!'
            self._logger.error(_error_msg)
            ProgrammingError(_error_msg)
        self._in_transaction = True
        self.execute('START TRANSACTION')

    def start_transaction(self) -> None:
        """
        Opens a transaction

        :return: None
        """
        self._start_transaction()

    def cancel_transaction(self) -> None:
        """
        Rollback an open transaction

        :return: None
        """
        self._rollback()

    def _rollback(self) -> None:
        """
        Rollback an open transaction

        :return: None
        :raises: ProgrammingError
        """
        if self._in_transaction is False:
            _error_msg = 'Not currently on a transaction!'
            self._logger.error(_error_msg)
            ProgrammingError(_error_msg)
        self._in_transaction = False
        self.execute('ROLLBACK')

    def rollback(self) -> None:
        """
        Rollback an open transaction

        :return: None
        """
        self._rollback()

    def _commit(self) -> None:
        """
        Commits an open transaction

        :return: None
        :raises: ProgrammingError
        """
        if self._in_transaction is False:
            _error_msg = 'Not currently on a transaction!'
            self._logger.error(_error_msg)
            ProgrammingError(_error_msg)
        self._in_transaction = False
        self._execute_statement('COMMIT')

    def commit(self) -> None:
        """
        Commits an open transaction

        :return: None
        """
        self._commit()

    def validate_transaction(self) -> None:
        """
        Commits an open transaction

        :return: None
        """
        self._commit()

    def send_messages_in_base_64(self, use_b64: bool) -> None:
        """
        Sets the base 64 mode

        :param use_b64: bool

        :return: None
        :raises: ProgrammingError
        """
        if not isinstance(use_b64, bool):
            _error_msg = 'Can not continue, please check the use_b64 argument!'
            self._logger.error(_error_msg)
            raise ProgrammingError(_error_msg)

        self._use_b64 = use_b64

    def set_protocol_version(self, protocol_version: str) -> None:
        """
        Sets the 4D SQL server protocol version , default to '12.0'

        :param protocol_version: str

        :return: None
        :raises: ProgrammingError
        """
        if not isinstance(protocol_version, str):
            _error_msg = 'Can not continue, please check the protocol_version argument!'
            self._logger.error(_error_msg)
            raise ProgrammingError(_error_msg)

        self._protocol_version = protocol_version

    def set_preferred_image_types(self, preferred_image_types: str) -> None:
        """
        Sets the preferred image type 'png', 'jpg'

        :param preferred_image_types: str

        :return: None
        :raises: ProgrammingError
        """
        if not isinstance(preferred_image_types, str):
            _error_msg = 'Can not continue, please check the preferred_image_types argument!'
            self._logger.error(_error_msg)
            raise ProgrammingError(_error_msg)

        self._preferred_image_types = preferred_image_types

    def set_fmt(self, fmt: str) -> None:
        """
        Sets the type of binary architecture

        :param fmt: str
            '<' little-endian for MAC OS X - RVLB
            '>'	big-endian for Windows - BLVR

        :return: None
        :raises: ProgrammingError
        """
        if not isinstance(fmt, str):
            _error_msg = 'Can not continue, please check the fmt argument!'
            self._logger.error(_error_msg)
            raise ProgrammingError(_error_msg)

        if fmt != '<':
            fmt = '>'
        self._fmt = fmt

    def print_result(self, headers: list, rows: list, max_width=0) -> None:
        """
        Prints a 4D SQL server cursor result

        :param headers: list
        :param rows: list
        :param max_width: int

        :return: None
        """
        self._view.print_result(headers, rows, max_width, logger=self._logger)


class _python4DBIView(object):
    """
    It represents the model’s data to user.
    """

    @staticmethod
    def print_result(headers: list, rows: list, max_width=0, logger=None) -> None:
        """
        Prints a 4D SQL server cursor result

        :param headers: list
        :param rows: list
        :param max_width: int
        :param logger: logging.Logger

        :return: None
        :raises: ProgrammingError
        """
        if not isinstance(headers, list):
            _error_msg = 'Can not continue, please check the headers argument!'
            if isinstance(logger, logging.Logger):
                logger.error(_error_msg)
            raise ProgrammingError(_error_msg)

        if not isinstance(rows, list):
            _error_msg = 'Can not continue, please check the rows argument!'
            if isinstance(logger, logging.Logger):
                logger.error(_error_msg)
            raise ProgrammingError(_error_msg)

        _table = texttable.Texttable(max_width=max_width)

        # 4D SQL server header description is a list of tuples [(str, obj)]
        # convert into an headers list
        _headers = list()
        for el in headers:
            _headers.append(el[0])

        _table.add_row(_headers)

        for _el in rows:
            _table.add_row(_el)

        print(_table.draw() + "\n")


class python4DBI(object):  # NOSONAR, (ignore CamelCase convention SonarLint alert)
    """
    4D Facade
    """

    # Private variables
    _connect_args = None
    _socket = None
    _connected = False
    _cursor = None
    _logger = None

    def __init__(self, logging_level=logging.CRITICAL, logging_file=None) -> None:
        """
        Constructor

        :param logging_level: int
        :param logging_file: str
        :return: None
        :raises: OperationalError
        """

        # Logging
        # Gets or creates a logger
        self._logger = logging.getLogger(__name__)

        # Set log level
        self._logger.setLevel(logging_level)

        # Define file handler and set formatter
        _log_file_name = 'python4DBI.log'
        if isinstance(logging_file, str):
            _log_file_name = logging_file
        #  Receiving a file handler => _file_handler = logging.FileHandler(_log_file_name)
        _file_handler = RotatingFileHandler(_log_file_name, maxBytes=1024 * 1024 * 5, backupCount=5)
        _formatter = logging.Formatter('[%(levelname)s]\t[%(asctime)s]\t[%(message)s]')
        _file_handler.setFormatter(_formatter)

        # Add file handler to logger
        self._logger.addHandler(_file_handler)

        self._connect_args = {'socket_timeout': 10,
                              'user': '',
                              'password': '',
                              'host': '127.0.0.1',
                              'port': 19812}
        self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        if self._socket is None:
            _error_msg = 'Unable to initialize the socket!'
            self._logger.critical(_error_msg)
            raise OperationalError(_error_msg)

    def __del__(self) -> None:
        """
        Destructor

        :return: None
        """
        self.close()

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        """
        Used on python 'with X() as x:' statement

        :param exc_type: type
        :param exc_val: value
        :param exc_tb: traceback

        :return: None
        """
        self.close()

    def connect(self, **kwargs) -> None:
        """
        Opens a socket connection to the 4D SQL Server

        :param kwargs:
            Keyword arguments:
            socket_timeout : int -- default 10
            dsn : str -- default ''
            host : str -- default '127.0.0.1'
            port : int -- default 19812
            user : str -- default ''
            password : str -- default ''

        :return: None
        :raises: ProgrammingError, InterfaceError

        dsn - data source name example host=localhost;port:19812;user:theUser;password:thePassword
        """
        if self._connected:
            _error_msg = 'Socket already connected to the 4D SQL Server!'
            self._logger.error(_error_msg)
            raise ProgrammingError(_error_msg)

        for _arg in kwargs:

            if _arg == 'socket_timeout':
                if not isinstance(kwargs[_arg], int):
                    _error_msg = 'Can not continue, please check the socket_timeout argument!'
                    self._logger.error(_error_msg)
                    raise ProgrammingError(_error_msg)
                self._connect_args['socket_timeout'] = kwargs[_arg]

            if _arg == 'dsn':
                if not isinstance(kwargs[_arg], str):
                    _error_msg = 'Can not continue, please check the dsn argument!'
                    self._logger.error(_error_msg)
                    raise ProgrammingError(_error_msg)
                # Make an argument dict based off of the arguments passed
                # if a dsn is given, we need to split it up
                _dsn = kwargs[_arg]
                _dsn_parts = _dsn.split(';')
                for _part in _dsn_parts:
                    _part = _part.strip()
                    _part_parts = _part.split('=')
                    if _part_parts[0] not in ['host', 'port', 'user', 'password']:
                        _error_msg = 'Unrecognized parameter: {}'.format(_part_parts[0])
                        self._logger.error(_error_msg)
                        raise ProgrammingError(_error_msg)
                    self._connect_args[_part_parts[0].strip()] = _part_parts[1].strip()

            if _arg == 'host':
                if not isinstance(kwargs[_arg], str):
                    _error_msg = 'Can not continue, please check the host argument!'
                    self._logger.error(_error_msg)
                    raise ProgrammingError(_error_msg)
                self._connect_args['host'] = kwargs[_arg]

            if _arg == 'port':
                if not isinstance(kwargs[_arg], int):
                    _error_msg = 'Can not continue, please check the port argument!'
                    self._logger.error(_error_msg)
                    raise ProgrammingError(_error_msg)
                self._connect_args['port'] = kwargs[_arg]

            if _arg == 'user':
                if not isinstance(kwargs[_arg], str):
                    _error_msg = 'Can not continue, please check the user argument!'
                    self._logger.error(_error_msg)
                    raise ProgrammingError(_error_msg)
                self._connect_args['user'] = kwargs[_arg]

            if _arg == 'password':
                if not isinstance(kwargs[_arg], str):
                    _error_msg = 'Can not continue, please check the password argument!'
                    self._logger.error(_error_msg)
                    raise ProgrammingError(_error_msg)
                self._connect_args['password'] = kwargs[_arg]

        # Set the socket timeout
        self._socket.settimeout(self._connect_args['socket_timeout'])

        try:
            self._socket.connect((self._connect_args['host'], self._connect_args['port']))
        except socket.error:
            _error_msg = 'Socket error: %s', socket.error
            self._logger.critical(_error_msg)
            raise InterfaceError(_error_msg)

        self._connected = True

    def close(self) -> None:
        """
        Closes the current 4D SQL server socket connection

        :return: None
        """
        if self._connected:
            if self._cursor:
                self._cursor.close()
            self._socket.close()
            self._connected = False

    def cursor(self) -> _python4DCursor:
        """
        Returns a 4D SQL server cursor object

        :return: _python4DCursor
        :raises: ProgrammingError
        """
        if self._connected is False:
            _error_msg = 'Socket not connected to the 4D SQL server!'
            self._logger.error(_error_msg)
            raise ProgrammingError(_error_msg)
        if not self._cursor:
            self._cursor = _python4DCursor(self)
        return self._cursor

    def connected(self) -> bool:
        """
        Returns true if the socket is connected to the 4D SQL server and false otherwise

        :return: bool
        """
        return self._connected

    def get_socket(self) -> socket:
        """
        Returns the current socket object

        :return: socket
        """
        return self._socket

    def get_socket_timeout(self) -> int:
        """
        Returns the current socket timeout

        :return: int
        """
        return self._connect_args['socket_timeout']

    def get_host(self) -> str:
        """
        Returns the current to 4D SQL server host

        :return: str
        """
        return self._connect_args['host']

    def get_port(self) -> int:
        """
        Returns the current to 4D SQL server port

        :return: int
        """
        return self._connect_args['port']

    def get_user(self) -> str:
        """
        Returns the current to 4D SQL server user

        :return: str
        """
        return self._connect_args['user']

    def get_password(self) -> str:
        """
        Returns the current to 4D SQL server password

        :return: str
        """
        return self._connect_args['password']

    def get_logger(self) -> logging.Logger:
        """
        Returns the logger object

        :return: logging.Logger
        """
        return self._logger
