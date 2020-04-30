import idem_linux.corn.system.console
import getpass
import pytest
import pwd
import unittest.mock as mock


class TestConsole:
    @pytest.mark.asyncio
    async def test_load_console_user(self, c_hub):
        ret = lambda: 0
        ret.pw_uid = 999
        with mock.patch.object(getpass, "getuser", return_value="test_user"):
            with mock.patch.object(pwd, "getpwnam", return_value=ret):
                await idem_linux.corn.system.console.load_console_user(c_hub)

        assert c_hub.corn.CORN.console_username == "test_user"
        assert c_hub.corn.CORN.console_user == 999
