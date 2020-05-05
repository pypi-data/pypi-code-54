import fire
from tamplar import api


def cmd():
    fire.Fire({
        'init': api.init,
        'deps': api.deps,
    })
