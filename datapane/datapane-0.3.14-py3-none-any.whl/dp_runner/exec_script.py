import ast
import builtins
import importlib
import os
import runpy
import subprocess
import sys
from functools import partial
from types import FrameType
from typing import Optional

import datapane.api as api
from dp_common import SDict, log

from .exceptions import CodeRaisedError, CodeSyntaxError

ENVIRON_CONFIG = {"banned_builtins": {"compile", "exec", "eval"}, "default_environment": []}


def run(script: api.Script, user_config: SDict) -> SDict:
    """Run a datapane python script/module"""
    install_script(script)
    api.reset_api(params=user_config)

    user_top_mod = script.entrypoint.split(".")[0]

    try:
        res_scope = exec_mod(script.entrypoint)
        return res_scope
    except SyntaxError:
        raise CodeSyntaxError.from_exception()
    except Exception:
        raise CodeRaisedError.from_exception(partial(filter_frame_by_filename, user_top_mod))


# def run(run_config: RunnerConfig) -> List[api.BlockType]:
#     """Snippet - run a python function embedded within in the snippet config field"""
#     code = run_config.code
#     user_config: SDict = Munch.fromDict(run_config.format())
#     # call to_df locally
#     # convert to dfs if needed
#     # dp._snippet_init(config=user_config)
#
#     # NOTE(MG): currently just exec the script - do we need to load it as a module via importlib?
#     try:
#         # pass in 'snippet_name' explicitly as we depend on it below.
#         init_state: SDict = {"params": user_config, "parameters": user_config, "on_datapane": True}
#         res_scope = exec_user_script(code, init_state, snippet_name=USER_CODE_NAME)
#
#         # call render function/extract report var
#         if "render" in res_scope:
#             report = res_scope["render"]()
#         elif "report" in res_scope:
#             report = res_scope["report"]
#         else:
#             log.warning("report variable nor render function found in script")
#             report = []
#         return report
#     except SyntaxError:
#         raise CodeSyntaxError.from_exception()
#     except Exception:
#         raise CodeRaisedError.from_exception(partial(filter_frame_by_filename, USER_CODE_NAME))


################################################################################
# internal
def in_venv() -> bool:
    return hasattr(sys, "real_prefix") or sys.base_prefix != sys.prefix


def install_script(s: api.Script):
    """Install the script"""
    # TODO - use custom site-packages?
    # TODO - add local cache check here
    # import appdirs
    # import site
    # dp_site_dir = Path(appdirs.user_cache_dir(appname="datapane")) / "dp-site-packages"
    # site.addusersitepackages(str(dp_site_dir))
    # log.info(f"Added {dp_site_dir} to Python site-packages")
    whl_fn = s.download_pkg()

    # who are we?
    if in_venv() or os.getuid() == 0:
        subprocess.check_call([sys.executable, "-m", "pip", "install", str(whl_fn)])
    else:
        # normal user
        subprocess.check_call([sys.executable, "-m", "pip", "install", "--user", str(whl_fn)])
    importlib.invalidate_caches()
    log.info(f"Installed package ({whl_fn}) for script {s.id}")


def exec_mod(mod_name: str, init_state: Optional[SDict] = None) -> SDict:
    # a = ast.parse(script, snippet_name, "exec")
    # ast_validation(a)
    init_state = init_state or dict()
    globalscope = {
        # "df": single_input,
        # "params": Munch(config),
        # "__builtins__": override_builtins(__import__)
    }
    globalscope.update(init_state)

    res_scope = runpy.run_module(
        mod_name, init_globals=globalscope, run_name="__datapane__", alter_sys=False
    )

    return res_scope


def ast_validation(node):
    for n in ast.walk(node):
        # TODO: implement check for import statements
        if isinstance(n, ast.Import):
            pass
        if isinstance(n, ast.ImportFrom):
            pass


class OverriddenBuiltins(dict):
    def __getitem__(self, name):
        if name in ENVIRON_CONFIG["banned_builtins"]:
            raise RuntimeError("Illegal builtin {}".format(name))
        return super().__getitem__(name)


def override_builtins(importer):
    b = OverriddenBuiltins(builtins.__dict__)
    b["__import__"] = importer
    return b


def importer(name, *x, **y):
    rootpkg = name.split(".")[0]
    if rootpkg not in ("dp_runner",):  # TODO: module check
        return builtins.__import__(name, *x, **y)
    raise ImportError("Cannot import banned module")


def filter_frame_by_filename(filename: str, frame: FrameType) -> bool:
    return frame.f_code.co_filename == filename
