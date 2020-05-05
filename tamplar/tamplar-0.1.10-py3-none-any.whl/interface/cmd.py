import fire
from tamplar.api import methods


def cmd():
    fire.Fire({
        'init': methods.init,
        'deps': methods.deps,
    })
