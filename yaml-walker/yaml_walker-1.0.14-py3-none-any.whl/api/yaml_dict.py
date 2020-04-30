from yaml_walker.api import Ypath

# TODO: Implement YDict as full 'dict' implementation


class YDict:
    def __init__(self, data: dict, item=None):
        self._node: dict = data if item is None else Ypath(item)(data)

    @property
    def as_dict(self):
        return self._node

    def _get_y_query_item(self, item):
        if isinstance(item, YDict):
            temp_query = self._node
        else:
            temp_query = Ypath(item)
        return YDict(temp_query(self._node))

    def __str__(self):
        return str(self._node)

    def __getattr__(self, item):
        return self._get_y_query_item(item)

    def __getitem__(self, item):
        return self._get_y_query_item(item)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is None:
            return None
        return exc_type(exc_val, exc_tb)