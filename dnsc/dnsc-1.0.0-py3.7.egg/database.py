import aiodns
import asyncpg
import dataclasses
import json
import tldextract
import typing


@dataclasses.dataclass
class DNSRecord:

    name: str
    rtype: str
    value: str
    options: dict = None

    @classmethod
    def from_response(cls, response: typing.Any, name: str = None) -> list:
        records = []
        
        if not response:
            return records

        # The response object came from a gethostbyname request
        # And we need to create the CNAME chain if there were aliases
        if hasattr(response, 'aliases') and response.aliases:
            for i, alias in enumerate(response.aliases[:-1]):
                records.append(cls(
                    name=alias.lower(),
                    rtype='CNAME',
                    value=response.aliases[i + 1],
                ))
            
            records.append(cls(
                name=response.aliases[-1].lower(),
                rtype='CNAME',
                value=response.name,
            ))
        
        if hasattr(response, 'addresses') and response.addresses:
            for addr in response.addresses:
                records.append(cls(
                    name=response.name.lower(),
                    rtype='A',
                    value=addr,
                ))
        
        # The response from dns_query is a list of records
        # Note that we need the optional "name" argument as the actual DNS
        # response doesn't tell us the original name that was requested.
        if type(response) == list and name:
            for rr in response:
                rr_type = type(rr)

                if rr_type == aiodns.pycares.ares_query_ns_result:
                    records.append(cls(
                        name=name,
                        rtype='NS',
                        value=rr.host,
                    ))
                elif rr_type == aiodns.pycares.ares_query_a_result:
                    records.append(cls(
                        name=name,
                        rtype='A',
                        value=rr.host,
                    ))
                elif rr_type == aiodns.pycares.ares_query_aaaa_result:
                    records.append(cls(
                        name=name,
                        rtype='AAAA',
                        value=rr.host,
                    ))
                elif rr_type == aiodns.pycares.ares_query_mx_result:
                    records.append(cls(
                        name=name,
                        rtype='MX',
                        value=rr.host,
                        options={
                            'priority': rr.priority,
                        },
                    ))
                elif rr_type == aiodns.pycares.ares_query_txt_result:
                    records.append(cls(
                        name=name,
                        rtype='TXT',
                        value=rr.text,
                    ))
                elif rr_type == aiodns.pycares.ares_query_soa_result:
                    records.append(cls(
                        name=name,
                        rtype='SOA',
                        value=rr.nsname,
                        options={
                            'hostmaster': rr.hostmaster,
                            'serial': rr.serial,
                            'refresh': rr.refresh,
                            'retry': rr.retry,
                            'expires': rr.expires,
                            'minttl': rr.minttl,
                        },
                    ))
                elif rr_type == aiodns.pycares.ares_query_srv_result:
                    records.append(cls(
                        name=name,
                        rtype='SRV',
                        value=f'{rr.host}:{rr.port}',
                        options={
                            'priority': rr.priority,
                            'weight': rr.weight,
                        },
                    ))
        
        return records


@dataclasses.dataclass
class DNSTarget:

    hostname: str
    domain: str


async def create_db_connection():
    return await asyncpg.connect(
        user='doadmin',
        password='cfa2uszcjhaffznc',
        database='dns',
        host='dns-db-sfo2-do-user-4596532-0.db.ondigitalocean.com',
        port=25060,
        ssl='require')


async def create_db_pool():
    return await asyncpg.create_pool(
        user='doadmin',
        password='cfa2uszcjhaffznc',
        database='dns',
        host='dns-db-sfo2-do-user-4596532-0.db.ondigitalocean.com',
        port=25060,
        ssl='require')


async def insert_dns_records(dbconn: asyncpg.Connection, records: typing.List[DNSRecord]) -> None:
    items = []

    for record in records:
        parts = tldextract.extract(record.name)
        hostname = parts.subdomain
        domain = '{}.{}'.format(parts.domain, parts.suffix)
        rtype = record.rtype
        value = record.value
        options = record.options
        if options:
            options = json.dumps(options)

        # Ensure that all values are strings
        if type(value) == bytes:
            value = value.decode('utf-8')

        items.append((hostname.lower(), domain.lower(), rtype.upper(), value, options))

    try:
        await dbconn.executemany('''
            INSERT INTO hostnames(hostname, domain, type, value, options)
                VALUES ($1, $2, $3, $4, $5)
                ON CONFLICT (hostname, domain, type, value)
                DO UPDATE SET last_seen = now();
            ''', items)
    except Exception as e:
        print(e)


async def insert_dns_targets(dbconn: asyncpg.Connection, targets: typing.List[DNSTarget]) -> None:
    items = [(target.hostname, target.domain) for target in targets]
    domain_items = {(target.domain, ) for target in targets}

    try:
        await dbconn.executemany('''
            INSERT INTO targets(hostname, domain)
                VALUES ($1, $2)
                ON CONFLICT DO NOTHING;
            ''', items)

        await dbconn.executemany(
            'INSERT INTO domains(name) VALUES(%s) ON CONFLICT DO NOTHING;',
            domain_items)

    except Exception as e:
        print(e)
