from abc import ABC, abstractmethod
from typing import List

from ftests.args_type_checkers import assert_isinstance
from ftests.expectation_result import ExpectationResult


class TestCase(ABC):
    codename: str = None
    name: str

    def __init__(self, name: str):
        assert_isinstance(name, str, 'Test case name must be a string.')
        self.name = name

    @abstractmethod
    def launch(self) -> List[ExpectationResult]:
        raise NotImplementedError

    @staticmethod
    @abstractmethod
    def from_dict(data_dict: dict):
        raise NotImplementedError
