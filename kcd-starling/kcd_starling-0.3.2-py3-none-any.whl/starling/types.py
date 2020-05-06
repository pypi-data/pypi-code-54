import enum
import typing
from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Union, List, Dict, Text, Any

if TYPE_CHECKING:
    pass


@dataclass
class ScrapperData:
    topic: str
    candidate: typing.Any
    message: 'MessageData'
    source: str = None
    actions: typing.Dict[str, typing.List['TaskData']] = field(default_factory=dict)
    auth_session: typing.Any = None
    error_message: str = None
    error_extra: dict = None
    is_valid: bool = True
    extra_config: dict = field(default_factory=dict)
    broadcast_variables: dict = field(default_factory=dict)


@dataclass
class TaskData:
    action: str
    fetched_data: 'FetchedData' = None
    is_done: bool = False
    criteria: typing.Dict = field(default_factory=dict)
    error: dict = field(default_factory=dict)


@dataclass()
class MessageData:
    message: dict
    created_at: str = None
    consumed_at: str = None
    scrap_started_at: str = None
    scrap_finished_at: str = None
    visibility_timeout_at: str = None


class FetchedDataType(enum.Enum):
    LIST = enum.auto()
    DICT = enum.auto()
    COMBINED = enum.auto()


@dataclass()
class FetchedData:
    data: Union[Dict[Text, Any], List[Dict[Text, Any]], Dict[Text, Union[Dict[Text, Any], List[Dict[Text, Any]]]]]
    use_plover: bool = True
    type: FetchedDataType = FetchedDataType.LIST
