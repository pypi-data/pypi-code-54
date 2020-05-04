from pathlib import Path


class MemoryTemplate:
    location: Path

    def save(self, data: dict):
        """
        write the given dictionary to :location:

        :param data: item to save
        """
        raise NotImplementedError

    def load(self) -> dict:
        """
        :return: content read from disk
        """
        raise NotImplementedError
