import datetime
import getpass
import logging
import os
import shutil
import subprocess
import tempfile
import time
from copy import deepcopy
from pathlib import Path
from typing import Optional, Type, Dict
from types import TracebackType

import openvpn_api  # type: ignore
from . import OVPNStartupTimeoutException, OVPNStopTimeoutException

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class OpenVPNConfig:
    """Class that holds configuration for OpenVPN"""

    def __init__(
        self,
        ca: Optional[str] = None,
        cert: Optional[str] = None,
        key: Optional[str] = None,
        dh: Optional[str] = None,
        **kwargs: str,
    ):
        """Store OpenVPN configuration in semi-parsed way and allow for generating proper content OVPN expects

        :param ca: Content of ca file.
        :param cert: Content of cert file.
        :param key: Content of key file.
        :param dh: Content of dh file.
        :param kwargs: Parameter name is option in OpenVPN configuration file, and value is its parameters as one string.
        """
        self.config: Dict[str, str] = {}
        self.config.update(kwargs)
        self.ca = ca
        self.cert = cert
        self.key = key
        self.dh = dh

    def get_content(self) -> bytes:
        """Generate content of configuration file"""
        generated = "\n".join(f"{key} {value}" for key, value in self.config.items())
        generated += "\n"
        generated += "".join(self._inline(option) for option in ("ca", "cert", "key", "dh"))
        return generated.encode()

    def _inline(self, option_name: str) -> str:
        option_content = self.__getattribute__(option_name)
        if option_content:
            return f"<{option_name}>\n{option_content}\n</{option_name}>\n"
        return ""


class OpenVPNServer:
    """Class wrapping OpenVPN instance"""

    def __init__(
        self,
        config: OpenVPNConfig,
        openvpn_binary: str = "openvpn",
        runtime_base_dir: Optional[Path] = None,
        privesc_binary: Optional[str] = "sudo",
        startup_timeout: int = 2,
    ):
        """Spawn new OpenVPN instance, wait for it and allow for easy exiting

        :param config: Object with OpenVPN configuration to be used.
        :param openvpn_binary: Callable name (or path) of OpenVPN binary to be used.
        :param runtime_base_dir: Optional `Path` object of dir to store various files related to our instance. Will be created if needed.
        :param privesc_binary: Callable name (or path) of binary allowing to execute `openvpn_binary` with elevated priviledges to be used.
        :param startup_timeout: Wait up to `startup_timeout` seconds for OpenVPN instance to be ready after spawning it. Too small value can lead to orphaned OpenVPN instances.
        :raises: :class:`OVPNStartupTimeoutException`: OVPN was not ready in expected time.
        """
        self._config = config

        if runtime_base_dir is None:
            runtime_base_dir = Path(tempfile.gettempdir()) / "python-openvpn-{}".format(os.getuid())
            logger.warning(f"runtime_dir not set, defaulting to {runtime_base_dir}")
        runtime_base_dir.mkdir(mode=0o700, parents=True, exist_ok=True)
        self._runtime_dir = Path(tempfile.mkdtemp(dir=runtime_base_dir))
        logger.info(f"Using {self._runtime_dir} to store runtime objects")

        self._augment_config()

        config_handle = self._runtime_dir / "config"
        config_handle.write_bytes(self._config.get_content())
        self._start_ovpn(
            config_path=config_handle.as_posix(), openvpn_binary=openvpn_binary, privesc_binary=privesc_binary
        )

        self._mgmt = openvpn_api.VPN(socket=self._mgmt_socket.as_posix())
        if not self._stall_until_ovpn_ready(timeout=startup_timeout):
            raise OVPNStartupTimeoutException(
                f"OVPN with PID {self._proc.pid} was not ready after specified timeout ({startup_timeout}s)"
            )

    def _augment_config(self) -> None:
        # if interface name is to be randomized, set it according to our randomized runtime dir
        if self._config.config["dev"] == "tap":
            self._config.config["dev"] = f"tap_{self._runtime_dir.name[:11]}"
        elif self._config.config["dev"] == "tun":
            self._config.config["dev"] = f"tun_{self._runtime_dir.name[:11]}"

        # set OVPN management to be accessible as unix socket in our runtime dir
        self._mgmt_socket = self._runtime_dir / "ovpn.sock"
        self._config.config["management"] = f"{self._mgmt_socket} unix"

        # constrain management socket access to our system user
        self._config.config["management-client-user"] = getpass.getuser()

    def _start_ovpn(self, config_path: str, openvpn_binary: str, privesc_binary: Optional[str]) -> None:
        command = []
        if privesc_binary is not None:
            command.append(privesc_binary)
        command.extend([openvpn_binary, config_path])
        logger.debug("Spawning process %s", command)
        self._proc = subprocess.Popen(
            command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, cwd=self._runtime_dir.as_posix()
        )
        logger.debug("Process spawned, PID %s", self._proc.pid)

    def _stall_until_ovpn_ready(self, timeout: int) -> bool:
        timestamp_end = datetime.datetime.now() + datetime.timedelta(seconds=timeout)
        while datetime.datetime.now() < timestamp_end:
            self._mgmt.clear_cache()
            if self.is_running:
                try:
                    with self._mgmt.connection():
                        state = self._mgmt.state
                        if state.state_name == "CONNECTED":
                            return True
                        logger.debug(state.state_name)
                except openvpn_api.util.errors.ConnectError as e:
                    logger.debug(e)
                    stdout, _ = self._proc.communicate(timeout=0.01)
                    logger.debug(stdout.decode())
                    if b"Exiting due to fatal error" in stdout:
                        break
            time.sleep(0.1)
        return False

    def __enter__(self) -> "OpenVPNServer":
        return self

    def __exit__(
        self,
        exc_type: Optional[Type[BaseException]],
        exc_val: Optional[BaseException],
        exc_traceback: Optional[TracebackType],
    ) -> None:
        self.stop()

    def stop(self, timeout: int = 5) -> None:
        """Stop OpenVPN instance

        Politely asks OVPN instance to exit.

        :param timeout: After telling OVPN to stop wait up to `timeout` seconds for it to exit.
        :raises: :class:`OVPNStopTimeoutException`: OVPN did not exit in expected time.
        """
        if not self.is_running:
            shutil.rmtree(self._runtime_dir, ignore_errors=True)
            return
        with self._mgmt.connection():
            self._mgmt.send_sigterm()
        timestamp_end = datetime.datetime.now() + datetime.timedelta(seconds=timeout)
        while datetime.datetime.now() < timestamp_end:
            if not self.is_running:
                shutil.rmtree(self._runtime_dir, ignore_errors=True)
                return
            time.sleep(0.1)
        raise OVPNStopTimeoutException(f"OVPN was still alive after specified timeout ({timeout}s)")

    @property
    def is_running(self) -> bool:
        """Check if OpenVPN is currently running"""
        return self._mgmt_socket.exists()

    def get_config(self) -> OpenVPNConfig:
        """Get OpenVPN config of this instance"""
        return deepcopy(self._config)

    @property
    def state(self) -> str:
        """Get OpenVPN instance state

        "NOT_RUNNING" means that the instance is not currently running.
        Other values have meaning as defined in https://openvpn.net/community-resources/management-interface/
        under 'COMMAND -- state'
        """
        if not self.is_running:
            return "NOT_RUNNING"
        with self._mgmt.connection():
            return self._mgmt.state.state_name
