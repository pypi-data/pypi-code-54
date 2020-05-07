from scapy.all import *
from time import time
from ipwhois import IPWhois, exceptions

conf.verb = 0


def get_asn_description(ip):
    try:
        asn = IPWhois(ip)
        asn_owner = asn.lookup_rdap(depth=1)
        return asn_owner['asn_description']
    except exceptions.ASNRegistryError:
        return "Unknown ASN"
    except exceptions.IPDefinedError:
        return "Local"


def trace(result, ttl, max_ttl, dst, payload, try_count=0):

    p = IP(ttl=ttl, dst=dst)
    st = time()
    r = sr1(p / ICMP() / payload, timeout=1)
    et = time()
    result[ttl] = {}
    result[ttl]['latency_ms'] = int((et - st) * 1000)
    result[ttl]['asn_desc'] = get_asn_description(r.src) if r else ""
    result[ttl]['asn_ip'] = r.src if r else ""
    print(ttl, result[ttl])
    if r and r.src == dst:
        return result
    if ttl == max_ttl:
        return result
    return trace(result, ttl + 1, max_ttl, dst, payload)
