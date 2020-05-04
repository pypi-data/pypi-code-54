import os
import shutil
from pathlib import Path
from typing import Generator

from pytest import fixture  # type: ignore


@fixture
def in_sandbox() -> Generator:
    sandbox_dir = (Path(".") / "sandbox").absolute()
    if sandbox_dir.exists():
        shutil.rmtree(str(sandbox_dir))

    sandbox_dir.mkdir()
    os.chdir(str(sandbox_dir))

    yield
    if sandbox_dir.exists():
        shutil.rmtree(str(sandbox_dir))
