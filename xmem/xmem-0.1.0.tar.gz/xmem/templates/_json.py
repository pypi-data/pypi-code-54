import json

from ..template import MemoryTemplate


class JsonTemplate(MemoryTemplate):
    """
    Memory template using json storage
    """

    def save(self, data: dict):
        with self.location.open('w') as f:
            json.dump(data, f)

    def load(self) -> dict:
        with self.location.open('r') as f:
            return json.load(f)
