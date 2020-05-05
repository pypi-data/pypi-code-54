"""-"""

import asyncio
import os
import subprocess
import sys
import tempfile
import uuid
from dataclasses import dataclass, field
from typing import Any, List, Optional, Tuple

import atomicwrites
import psutil


@dataclass
class ProcessPipes:
    """-"""
    stdout: Any
    stderr: Any
    stdin: Any


def make_puid(pid: int, create_timestamp: int) -> str:
    """Process unique id (<pid>-<create_timestamp>)"""
    return "{}-{}".format(pid, create_timestamp)


def split_puid(puid: str) -> Tuple[int, int]:
    """Splits puid into pid and create timestamp"""
    try:
        pid: int = int(puid.split("-")[0])
        timestamp: int = int(puid.split("-")[1])
    except Exception:
        raise ValueError("Invalid puid")
    return (pid, timestamp)


@dataclass
class ProcessHandle:
    """-"""

    pid: int
    create_timestamp: int
    process: Optional[psutil.Process]

    _returncode: Optional[int] = field(default=None, init=False)

    def set_returncode(self, value: Optional[int]) -> None:
        """-"""
        _returncode = value

    @property
    def puid(self) -> str:
        """Process unique id (<pid>:<create_timestamp>)"""
        return make_puid(self.pid, self.create_timestamp)

    @property
    def run_flag_link_path(self) -> str:
        """-"""
        return get_run_flag_link_path(get_run_flag_dir(), self.puid)

    @staticmethod
    async def find(puid: str) -> Optional["ProcessHandle"]:
        """-"""
        loop = asyncio.get_running_loop()
        return await loop.run_in_executor(
            None, find_process, puid)

    @staticmethod
    async def find_by_pid(pid: int) -> Optional["ProcessHandle"]:
        """-"""
        loop = asyncio.get_running_loop()
        return await loop.run_in_executor(
            None, find_process_by_pid, pid)

    @staticmethod
    async def get_current() -> "ProcessHandle":
        """-"""
        handle = await ProcessHandle.find_by_pid(os.getpid())
        assert handle
        return handle

    async def wait(self) -> Optional[int]:
        """-"""

        if not self.process:
            return self._returncode

        loop = asyncio.get_running_loop()
        while True:
            try:
                return await loop.run_in_executor(
                    None, self.process.wait, 1)
            except psutil.TimeoutExpired:
                pass

    def _stop(self) -> None:
        """-"""

        try:
            with open(self.run_flag_link_path) as file:
                run_flag_id: str = file.read()
                if isinstance(run_flag_id, bytes):
                    run_flag_id = str(run_flag_id, "utf-8")
        except FileNotFoundError:
            return

        run_flag_path = get_run_flag_path(
            get_run_flag_dir(), run_flag_id)

        try:
            os.remove(run_flag_path)
        except FileNotFoundError:
            return

        try:
            os.remove(self.run_flag_link_path)
        except FileNotFoundError:
            return

    async def stop(self) -> None:
        """-"""

        loop = asyncio.get_running_loop()
        await loop.run_in_executor(None, self._stop)


def find_process(puid: str) -> Optional[ProcessHandle]:
    """-"""

    pid, timestamp = split_puid(puid)
    try:
        process = psutil.Process(pid)
        if int(process.create_time()) != timestamp:
            return None
        return ProcessHandle(pid, timestamp, process)
    except psutil.NoSuchProcess:
        return None


def find_process_by_pid(pid: int) -> Optional[ProcessHandle]:
    """-"""

    try:
        process = psutil.Process(pid)
        return ProcessHandle(
            process.pid,
            int(process.create_time()),
            process)
    except psutil.NoSuchProcess:
        return None


def get_run_flag_path(run_flag_dir: str, run_flag_id: str) -> str:
    """-"""
    return os.path.join(run_flag_dir, "run-flag-{}".format(run_flag_id))


def get_run_flag_link_path(run_flag_dir: str, puid: str) -> str:
    """-"""
    return os.path.join(run_flag_dir, "run-flag-link-{}".format(puid))


def get_run_flag_dir() -> str:
    """-"""
    run_flag_dir: str = os.path.join(
        tempfile.gettempdir(), "nwsubprocess")
    return run_flag_dir


async def start_subprocess(
        program: str,
        args: Optional[List[str]] = None,
        stop_timeout: float = 3,
        daemon: bool = False,
        stdout: Any = None,
        stderr: Any = None,
        stdin: Any = None) -> Tuple[ProcessHandle, ProcessPipes]:
    """-"""

    parent: Optional[ProcessHandle] = None
    if daemon:
        parent = await ProcessHandle.get_current()

    run_flag_dir: str = get_run_flag_dir()

    run_flag_id: str = str(uuid.uuid1())
    run_flag_path: str = get_run_flag_path(run_flag_dir, run_flag_id)
    python_dir = os.path.dirname(sys.executable)

    params: List[str] = [
        "-m",
        "nwsubprocess",
        run_flag_path,
        str(stop_timeout),
        parent.puid if parent else "x",
        program
    ]
    if args:
        for arg in args:
            params.append(arg)

    if os.name == "nt":
        info = subprocess.STARTUPINFO()
        info.dwFlags = subprocess.STARTF_USESHOWWINDOW
        info.wShowWindow = subprocess.SW_HIDE

        process = await asyncio.create_subprocess_exec(
            "cmd",
            "/c",
            os.path.join(python_dir, "python"),
            *params,
            stdout=stdout,
            stderr=stderr,
            stdin=stdin,
            startupinfo=info,
            creationflags=subprocess.CREATE_NEW_PROCESS_GROUP | subprocess.CREATE_NEW_CONSOLE
        )
    else:
        raise NotImplementedError()

    pipes = ProcessPipes(
        stdout=process.stdout,
        stderr=process.stderr,
        stdin=process.stdin
    )
    handle = find_process_by_pid(process.pid)
    if handle:
        os.makedirs(run_flag_dir, exist_ok=True)
        with atomicwrites.atomic_write(handle.run_flag_link_path) as file:
            file.write(run_flag_id)
        with atomicwrites.atomic_write(run_flag_path) as file:
            file.write(handle.puid)
        return handle, pipes
    else:
        assert process.returncode is not None
        await process.wait()
        handle = ProcessHandle(process.pid, -1, None)
        handle.set_returncode(process.returncode)
        return handle, pipes
