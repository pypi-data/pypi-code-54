import fire
from tamplar.api import methods


fire.Fire({
    'init': methods.init,
    'deps': methods.deps,
})
