
import pathlib

from .core.app import App


def from_env():
    """
    """
    return API()


class API:
    """
    """

    def get_app(self, name=None, root=None):
        """
        """
        root = pathlib.Path(root) if root else pathlib.Path.cwd()
        name = name or root.name
        app = App(name=name, root=root)
        return app
