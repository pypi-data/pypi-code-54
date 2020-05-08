
from functools import update_wrapper
from .utils import compat


# 方法拦截装饰器
# <B> 说明： </B>
# <pre>
# 略
# </pre>
def decorator(target):
    """A signature-matching decorator factory."""
    def decorate(fn):
        spec = compat.inspect_getfullargspec(fn)
        names = tuple(spec[0]) + spec[1:3] + (fn.__name__,)
        targ_name, fn_name = compat.unique_symbols(names, "target", "fn")
        metadata = dict(target=targ_name, fn=fn_name)
        metadata.update(compat.format_argspec_plus(spec, grouped=False))
        metadata["name"] = fn.__name__

        strcode = """
def %(name)s(%(args)s:
    return %(target)s(%(fn)s, %(apply_kw)s)
""" % metadata
        code = (
            strcode
        )

        decorated = compat.exec_code_in_env(
            code, {targ_name: target, fn_name: fn}, fn.__name__
        )

        decorated.__defaults__ = getattr(fn, "im_func", fn).__defaults__
        decorated.__wrapped__ = fn
        return update_wrapper(decorated, fn)

    return update_wrapper(decorate, target)


