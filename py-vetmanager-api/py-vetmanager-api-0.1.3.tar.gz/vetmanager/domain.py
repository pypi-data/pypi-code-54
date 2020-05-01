from interface import implements, Interface
from .url.protocol import ProtocolInterface, HTTPS
from .url.host import HostInterface, Host, CachedHost


class UrlInterface(Interface):
    pass


class Url(implements(UrlInterface)):

    __protocol: ProtocolInterface
    __host: HostInterface

    def __init__(self, protocol: ProtocolInterface, host: HostInterface):
        self.__protocol = protocol
        self.__host = host

    def __str__(self) -> str:
        return str(self.__protocol) + str(self.__host)


class FakeUrl(implements(UrlInterface)):

    def __str__(self):
        return 'https://tests.host.com'


def url(domain):
    host = CachedHost(
        Host(
            billing_url="https://billing-api.vetmanager.cloud/",
            domain=domain
        )
    )
    return str(Url(HTTPS(), host))
