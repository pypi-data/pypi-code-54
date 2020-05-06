from abc import ABC, abstractmethod


class Expectation(ABC):
    codename: str = None

    @abstractmethod
    def is_expectation_met(self, result) -> bool:
        pass
