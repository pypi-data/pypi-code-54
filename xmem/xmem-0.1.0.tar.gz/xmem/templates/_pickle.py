import pickle

from ..template import MemoryTemplate


class PickleTemplate(MemoryTemplate):
    """
    Memory template using pickle storage
    """

    def save(self, data: dict):
        with self.location.open('wb') as f:
            pickle.dump(data, f)

    def load(self) -> dict:
        with self.location.open('rb') as f:
            return pickle.load(f)
