import idem_linux.corn.net.fqdn
import pytest
import socket
import unittest.mock as mock


class TestFqdn:
    @pytest.mark.asyncio
    async def test_load_socket_info(self, c_hub):
        c_hub.exec.cmd.run.return_value = c_hub.pop.data.imap({"stdout": "test.local"})

        ret = (
            (()),
            (
                ({socket.AF_INET: 2}, {socket.SOCK_DGRAM: 2}, 17, "", ("127.0.0.1", 0)),
                ({socket.AF_INET: 2}, {socket.SOCK_STREAM: 1}, 6, "", ("127.0.0.1", 0)),
                (
                    {socket.AF_INET: 2},
                    {socket.SOCK_DGRAM: 2},
                    17,
                    "",
                    ("192.168.1.24", 0),
                ),
                (
                    {socket.AF_INET: 2},
                    {socket.SOCK_STREAM: 1},
                    6,
                    "",
                    ("192.168.1.24", 0),
                ),
            ),
            (
                (
                    {socket.AF_INET6: 30},
                    {socket.SOCK_DGRAM: 2},
                    17,
                    "",
                    ("::1", 0, 0, 0),
                ),
                (
                    {socket.AF_INET6: 30},
                    {socket.SOCK_STREAM: 1},
                    6,
                    "",
                    ("::1", 0, 0, 0),
                ),
                (
                    {socket.AF_INET6: 30},
                    {socket.SOCK_DGRAM: 2},
                    17,
                    "",
                    ("fe80::1", 0, 0, 1),
                ),
                (
                    {socket.AF_INET6: 30},
                    {socket.SOCK_STREAM: 1},
                    6,
                    "",
                    ("fe80::1", 0, 0, 1),
                ),
                (
                    {socket.AF_INET6: 30},
                    {socket.SOCK_DGRAM: 2},
                    17,
                    "",
                    ("fe80::cac:ffff:ffff:ffff", 0, 0, 4),
                ),
                (
                    {socket.AF_INET6: 30},
                    {socket.SOCK_STREAM: 1},
                    6,
                    "",
                    ("fe80::cac:ffff:ffff:ffff", 0, 0, 4),
                ),
            ),
        )
        with mock.patch.object(socket, "getfqdn", return_value="test.local"):
            with mock.patch.object(socket, "getaddrinfo", side_effect=ret):
                with mock.patch.object(socket, "gethostname", return_value="test_host"):
                    await idem_linux.corn.net.fqdn.load_socket_info(c_hub)

        assert c_hub.corn.CORN.domain == "local"
        assert c_hub.corn.CORN.fqdn == "test.local"
        assert c_hub.corn.CORN.localhost == "test_host"

        # These ones require socket to be mocked
        assert c_hub.corn.CORN.fqdn_ip4 == ("127.0.0.1", "192.168.1.24")
        assert c_hub.corn.CORN.fqdn_ip6 == (
            "::1",
            "fe80::1",
            "fe80::cac:ffff:ffff:ffff",
        )
        assert c_hub.corn.CORN.fqdns == (
            "127.0.0.1",
            "192.168.1.24",
            "::1",
            "fe80::1",
            "fe80::cac:ffff:ffff:ffff",
        )
