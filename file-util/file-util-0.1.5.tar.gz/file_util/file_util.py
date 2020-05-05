from pathlib import Path


class File:
    def __init__(self, path):
        self._path = path

    @property
    def path(self):
        return self._path

    @property
    def pathlib(self):
        return Path(self.path)

    @property
    def exists(self):
        return self.pathlib.exists()

    @property
    def does_not_exists(self):
        return not self.exists

    def create(self):
        self.pathlib.touch()

    def write(self, text):
        self.pathlib.write_text(text)

    def read(self):
        return self.pathlib.read_text()
