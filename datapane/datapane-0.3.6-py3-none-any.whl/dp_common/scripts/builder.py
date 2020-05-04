"""
Wrapper to build Python bundles using sdits and wheels for distribution
Dervied from flit main wrapper code

TODO
  - fork flit and extract out the include/exclude logic and wheel building
  - can use flit_core.sdist to get non-VCS builder
  - look at flit_core.common.get_docstring_and_version_via_ast to get module info
"""
import ast
import typing as t
from pathlib import Path

from flit.build import unpacked_tarball
from flit.inifile import ConfigError, read_flit_config
from flit.sdist import SdistBuilder, SdistBuilderCore
from flit.wheel import make_wheel_in
from jinja2 import Template

from dp_common.utils import log

from .config import DatapaneCfg, extract_py_notebook

# TODO - use a dedicated entry-module? will modify stacktraces for users
ENTRY_MODULE_NAME = "__dp_main__"
INI_FILE_NAME = ".dp_flit.toml"

# TODO - add additional fields to wheel
flit_config_template = Template(
    """
[build-system]
requires = ["flit_core >=2,<4"]
build-backend = "flit_core.buildapi"

[tool.flit.metadata]
module = "{{ mod_name }}"
author = "{{ username or 'Datapane User' }}"
author-email = "user@datapane.com"
{% if repo %}home-page = "{{ repo }}"{% endif %}
requires-python = ">= 3.6.1"
requires = [
    {% for x in requirements %}"{{ x }}"{{ "," if not loop.last }}
    {% endfor %}
]

[tool.flit.sdist]
include = [
    {% for x in include %}"{{ x }}"{{ "," if not loop.last }}
    {% endfor %}
]
exclude = [
    {% for x in exclude %}"{{ x }}"{{ "," if not loop.last }}
    {% endfor %}
]
"""
)


def gen_flit_config(
    dp_config: DatapaneCfg, out_conf_file: Path, mod_is_pkg=False, username: str = None
):
    """Write a flit configuration to disk
    uses dp_config from user along with extra params known at dp-server user"""

    # TODO - test this works for sdist and whl
    mod_name = dp_config.script.parent.stem if mod_is_pkg else dp_config.script.stem
    gen_conf = flit_config_template.render(
        **dp_config.to_dict(), mod_name=mod_name, username=username
    )

    log.debug(gen_conf)
    out_conf_file.write_text(gen_conf)

    # Load the config file to make sure it gets validated
    read_flit_config(out_conf_file)


def preprocess_root_module(dp_config: DatapaneCfg, proj_dir: Path) -> Path:
    """
    pre-configure source dir for flit
    - add version if needed
    - add docstring if needed
    """

    old_mod = proj_dir / dp_config.script
    new_mod = old_mod.with_name(f"__{old_mod.stem}.py")
    # TODO - pass mod_code via classvar in dp_config
    mod_code = extract_py_notebook(old_mod) if old_mod.suffix == ".ipynb" else old_mod.read_text()

    node = ast.parse(mod_code)

    # find and add version if doesn't exist
    for child in node.body:
        try:
            if (
                isinstance(child, ast.Assign)
                and len(child.targets) == 1
                and child.targets[0].id == "__version__"
                and isinstance(child.value, ast.Str)
            ):
                add_version = False
                break
        except AttributeError:
            log.debug(f"Found unexpected ast element on line {child.lineno}")
    else:
        log.debug(f"Version not found in {old_mod} - adding")
        add_version = True

    # find and add docstring if doesn't exist
    docstring = ast.get_docstring(node)
    add_docstring = (not docstring) or not docstring.strip()

    # copy to a new initial module
    with new_mod.open("w") as f:
        if add_docstring:
            f.write('"""DP auto-generated docstring"""\n')
            log.warning(
                "Couldn't find docstring - adding automatically, any errors will be off-by-one, suggest adding to your script"
            )
        if add_version:
            # TODO - append to script once flit bug fixed
            f.write('\n__version__ = "0.0.1"\n')
            log.warning(
                "Couldn't find __version__ - adding automatically, any errors will be off-by-one, suggest adding to your script"
            )
        f.write(mod_code)

    dp_config.script = Path(new_mod.name)
    # dp_config.name = new_mod.stem
    return new_mod


def build_local_sdist(dp_config: DatapaneCfg, proj_dir: Path = None, use_git: bool = False) -> Path:
    """
    Build a local sdist-bundle on the client for uploading
    currently requires version and docstring
    """
    proj_dir = proj_dir or Path(".")
    ini_file = proj_dir / INI_FILE_NAME
    root_mod: t.Optional[Path] = None

    try:
        root_mod = preprocess_root_module(dp_config, proj_dir)
        gen_flit_config(dp_config, ini_file)

        # TODO - we can't use git support for now as we generate files in repo dir, hence making dirty
        if use_git:
            sb = SdistBuilder.from_ini_path(ini_file)
        else:
            sb = SdistBuilderCore.from_ini_path(str(ini_file))

        sdist_file = sb.build(proj_dir, gen_setup_py=False)
        log.debug(f"Generated sdist {sdist_file}")
        return Path(sdist_file)
    except ConfigError as e:
        log.error("Config error: {}".format(e))
        raise e
    finally:
        if ini_file.exists():
            ini_file.unlink()  # missing_ok=True)
        if root_mod and root_mod.exists():
            root_mod.unlink()  # missing_ok=True)


def build_wheel(
    dp_config: DatapaneCfg, sdist_file: Path, dist_dir: Path, username: str, version: int
) -> Path:
    """
    Build a wheel from an sdist-bundle
    Calls into flit internal functions to build wheel - this is undocumented/unstable
    """
    wrapper_mod_name = f"{username}_{dp_config.name}_{version}"
    dp_config.script = wrapper_mod_name / dp_config.script
    dp_config.include = []
    dp_config.exclude = []

    # NOTE - wheel building hardcoded to run in `dist` dir - may cause race condition
    ini_filename = ".dp_flit.toml"

    # dist_dir = ini_file.parent / 'dist'
    # dist_dir.mkdir(parents=True, exist_ok=True)

    init_contents = f"""
\"\"\"DP auto-generated wrapper package\"\"\"
__version__ = "{version}"
"""

    try:
        # build the wheel from the unpacked sdist.
        # This helps ensure that the sdist contains all the necessary files.
        # TODO - this is unsafe - move to using GNU tar
        with unpacked_tarball(sdist_file) as tmpdir:
            log.debug("Building wheel from unpacked sdist %s", tmpdir)
            # TODO - create new module here
            tmpdir_p = Path(tmpdir)

            # rename unzip location to new package name
            mod_dir = tmpdir_p.parent / wrapper_mod_name
            tmpdir_p.rename(mod_dir)

            # restructure files to make valid wrapper package
            (mod_dir / "__init__.py").write_text(init_contents)
            (mod_dir / "PKG-INFO").unlink()
            (mod_dir / INI_FILE_NAME).unlink()

            # generate new flit config and build wheel
            new_ini_file = mod_dir.parent / ini_filename
            gen_flit_config(dp_config, new_ini_file, mod_is_pkg=True, username=username)
            wheel_info = make_wheel_in(new_ini_file, dist_dir)

        whl_file: Path = wheel_info.file
        log.debug(f"Generated whl file at {whl_file}")
        return whl_file

    except ConfigError as e:
        log.error("Config error: {}".format(e))
        raise e
