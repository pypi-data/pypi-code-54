import aiofiles
import logging
import os
import pathlib
import re
import sys

log = logging.getLogger(__name__)


async def load_python_version(hub):
    hub.corn.CORN.pythonversion = list(sys.version_info)


async def load_pip_versions(hub):
    """
    Get the versions of required pip packages
    """
    root_dir = pathlib.Path(
        os.path.join(os.path.dirname(__file__))
    ).parent.parent.parent
    requirements = os.path.join(root_dir, "requirements.txt")
    reqs = {}

    if os.path.isfile(requirements):
        async with aiofiles.open(requirements, "r") as _fh:
            async for line in _fh:
                split = re.split("[ <>=]", line.strip())
                name = split[0].lower()
                version = split[-1].lower()
                if name == version:
                    version = None
                reqs[name] = version
    else:
        ret = await hub.exec.cmd.run(
            [sys.executable, "-m", "pip", "show", "idem-linux"]
        )
        for line in ret.stdout.splitlines():
            if line.startswith("Requires:"):
                reqs = {x.strip(", "): "unknown" for x in line.split()[1:]}
                break
        else:
            reqs = {
                "corn": "unknown",
                "idem": "unknown",
                "pop": "unknown",
                "pop-config": "unknown",
                "rend": "unknown",
            }
    try:
        modules = {}
        ret = await hub.exec.cmd.run([sys.executable, "-m", "pip", "freeze"])
        if ret.retcode:
            raise OSError(f"Error running command: {ret.stderr.strip()}")
        for x in ret.stdout.split():
            if "==" in x:
                name, version = x.split("==")
            elif "#egg=" in x:
                version, name = x.split("#egg=")
            else:
                name = x
                version = None

            # pip is agnostic about case so we will prefer lower
            name = name.lower()
            if name in reqs or name.startswith("idem") or name.startswith("pop"):
                modules[name] = version

        hub.corn.CORN.requirement_versions = modules
    except OSError as e:  # pylint: disable=broad-exception
        log.error(f"Error running pip command: {e}")
        hub.corn.CORN.requirement_versions = reqs
