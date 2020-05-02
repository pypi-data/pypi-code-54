from vetmanager.domain import UrlInterface, Url
from vetmanager.url.host import Host
from vetmanager.url.protocol import HTTPS


def url(domain) -> UrlInterface:

    return Url(HTTPS(), Host(
            billing_url="https://billing-api.vetmanager.cloud/",
            domain=domain
        ))
