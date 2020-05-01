from gevent import monkey
import os
import sys
from locust.env import Environment
from locust_plugins.listeners import PrintListener


def _gevent_debugger_patch():
    """This is a workaround for gevent hanging during monkey patching when a debugger is attached
    Original code by ayzerar at https://github.com/Microsoft/PTVS/issues/2390"""

    if not os.getenv("VSCODE_PID") and not os.getenv("TERM_PROGRAM") == "vscode":
        # Dont patch if VS is not running (because then there probably is no debugger and
        # we would just hang, waiting for it)
        return

    monkey.patch_all()
    saved_modules = {}
    try:
        green_modules = set(
            [
                "socket",
                "ssl",
                "select",
                "urllib",
                "thread",
                "threading",
                "time",
                "logging",
                "os",
                "signal",
                "subprocess",
                "requests",
            ]
        )
        for modname in list(sys.modules.keys()):
            if modname.partition(".")[0] in green_modules:
                saved_modules[modname] = sys.modules.pop(modname)
    finally:
        sys.modules.update(saved_modules)


def run_single_user(locust_class, env=None, catch_exceptions=False):
    _gevent_debugger_patch()
    if env is None:
        env = Environment()
        PrintListener(env)
    locust_class._catch_exceptions = catch_exceptions
    locust_class(env).run()
