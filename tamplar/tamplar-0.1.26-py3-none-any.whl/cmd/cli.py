import fire
from tamplar.api import methods


def cli():
    fire.Fire({
        'init': methods.init,
        'deps': methods.deps,
    })
