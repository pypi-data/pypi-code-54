from aiodns import DNSResolver
from aiodns.error import DNSError


NAMESERVERS = {
    'shodan': [
        '162.243.164.140',
        '138.68.199.36',
    ],
    'google': [
        '8.8.8.8',
        '8.8.4.4',
    ],
    'cloudflare': [
        '1.1.1.1',
    ],
    'opendns': [
        '208.67.220.220',
        '208.67.222.222',
    ],
    'oracle': [
        '216.146.36.36',
        '216.146.35.35',
    ],

    # Some domains restrict access from these DNS servers which
    # incorrect responses.
    # Ex: sfgate.com
    'dns.watch': [
        '84.200.69.80',
        '84.200.70.40',
    ],
    'hurricane-electric': [
        '74.82.42.42',
    ],
    'unavailable': [
        '5.5.5.5',
    ]
}


def select_nameservers(*args) -> list:
    servers = []
    for name in args:
        servers.extend(NAMESERVERS[name])
    return servers


async def dns_query(resolver: DNSResolver, hostname: str, qtype: str) -> list:
    response = []

    try:
        response = await resolver.query(f'{hostname}.', qtype)

        # Make sure the value we're returning is a list
        if type(response) != list:
            response = [response]
    except DNSError:
        pass

    return response
