
from abc import abstractmethod
class BaseParser:

    @abstractmethod
    def parse(self,filepath):
        pass
