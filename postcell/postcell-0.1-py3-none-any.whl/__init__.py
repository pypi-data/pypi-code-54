"""A Jupyter custom magic command to post cell contents to a REST server"""
__version__ = '0.0.1'

from .postcell import PostCell

def load_ipython_extension(ipython):
    print("PostCell loaded")
    ipython.register_magics(PostCell)
