from __future__ import annotations
import aiohttp
import base64
import construct
import dataclasses
import typing
import OpenSSL


@dataclasses.dataclass
class CTEntry:

    leaf_input: str
    extra_data: str


@dataclasses.dataclass
class CTCertificate:

    extensions: dict
    subject: dict

    def domains(self) -> typing.List[str]:
        results = set()
        if self.subject['CN']:
            results.add(self.subject['CN'].lower())
        
        alts = self.extensions.get('subjectAltName')
        if alts:
            for name in alts.split(', '):
                if name.startswith('DNS:'):
                    results.add(name[4:].lower())
        
        return list(results)

    @classmethod
    def from_ctentry(cls, entry: CTEntry) -> CTCertificate:
        mth = MerkleTreeHeader.parse(base64.b64decode(entry.leaf_input))

        # Only process signed certificates - no pre-certs
        if mth.LogEntryType != 'X509LogEntryType':
            return None

        cert = OpenSSL.crypto.load_certificate(OpenSSL.crypto.FILETYPE_ASN1, Certificate.parse(mth.Entry).CertData)

        # Extract the components we care about
        tmp = cert.get_subject()
        subject = {
            'C': tmp.countryName,
            'ST': tmp.stateOrProvinceName,
            'L': tmp.localityName,
            'O': tmp.organizationName,
            'OU': tmp.organizationalUnitName,
            'CN': tmp.commonName,
        }

        extensions = {}
        for i in range(cert.get_extension_count()):
            ext = cert.get_extension(i)
            name = ext.get_short_name()
            if name == b'UNDEF':
                continue
            
            try:
                extensions[name.decode()] = str(ext)
            except Exception:
                pass

        return cls(subject=subject, extensions=extensions)


@dataclasses.dataclass
class CTLog:

    cursor: int  # Helper property used to keep track of which parts have already been downloaded
    description: str
    key: str
    url: str
    block_size: int
    total_size: int


MerkleTreeHeader = construct.Struct(
    'Version' / construct.Byte,
    'MerkleLeafType' / construct.Byte,
    'Timestamp' / construct.Int64ub,
    'LogEntryType' / construct.Enum(construct.Int16ub, X509LogEntryType=0, PrecertLogEntryType=1),
    'Entry' / construct.GreedyBytes,
)

Certificate = construct.Struct(
    'Length' / construct.Int24ub,
    'CertData' / construct.Bytes(construct.this.Length),
)

CertificateChain = construct.Struct(
    'ChainLength' / construct.Int24ub,
    'Chain' / construct.GreedyRange(Certificate),
)

PreCertEntry = construct.Struct(
    'LeafCert' / Certificate,
    construct.Embedded(CertificateChain),
    construct.Terminated,
)


async def get_certificates(http_client: aiohttp.ClientSession, log: str, start: int, end: int) -> typing.List[CTEntry]:
    download_url = f'http://{log}/ct/v1/get-entries?start={start}&end={end}'
    async with http_client.get(download_url) as response:
        # Grab the list of entries
        data = await response.json()

        # Convert them to data classes
        entries = [CTEntry(**entry) for entry in data.get('entries', [])]

        # Convert them to certificates
        certs = []
        for entry in entries:
            cert = CTCertificate.from_ctentry(entry)
            if cert:
                certs.append(cert)
        
        return certs


async def get_ctlogs(http_client: aiohttp.ClientSession) -> typing.List[CTLog]:
    logs = []

    async with http_client.get('https://www.gstatic.com/ct/log_list/log_list.json') as response:
        ctls = await response.json()

        for log in ctls['logs']:
            item = {
                'url': log['url'],
                'key': log['key'],
                'description': log['description'],
                'cursor': 0,
            }
            if item['url'].endswith('/'):
                item['url'] = item['url'][:-1]
            
            # Grab additional metadata about the log
            item['block_size'] = await _get_log_block_size(http_client, item['url'])

            try:
                # If we're unable to get the total number of entries in the log then skip it
                item['total_size'] = await _get_log_total_size(http_client, item['url'])
            except Exception as e:
                print(f'dnsc.ctlogs.get_ctlogs(): {e}')
                continue
            
            logs.append(CTLog(**item))
    
    return logs


async def _get_log_block_size(http_client: aiohttp.ClientSession, url: str) -> int:
    try:
        async with http_client.get(f'http://{url}/ct/v1/get-entries?start=0&end=10000') as response:
            entries = await response.json()
            return len(entries['entries'])
    except Exception as e:
        print(e)
        return 1024


async def _get_log_total_size(http_client: aiohttp.ClientSession, url: str) -> int:
    async with http_client.get(f'http://{url}/ct/v1/get-sth') as response:
        info = await response.json()
        return info['tree_size']
