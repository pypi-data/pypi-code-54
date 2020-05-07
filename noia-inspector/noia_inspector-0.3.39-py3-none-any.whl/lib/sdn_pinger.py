import concurrent.futures
import socket
import struct
import json
import requests
import os

from icmplib import multiping
from lib.sdn_client import SDN
from pyroute2 import IPRoute

ip = IPRoute()
TABLE_ID = 10


class SpeedTestType:
    AZURE = 'AZURE'
    ORACLE = 'ORACLE'
    AMBASSADOR = 'AMBASSADOR'


class Pinger:

    def __init__(
            self, device_id=os.environ['DEVICE_ID'],
            stage=os.environ['STAGE'],
            speedtest_type=SpeedTestType.AMBASSADOR
    ):
        self.sdn = SDN(device_id=device_id, stage=stage)
        # self.sdn.register_app()
        self.speedtest_type = speedtest_type
        self.host = socket.gethostname()
        self.session_uuid = device_id

    def get_ip(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        try:
            # doesn't even have to be reachable
            s.connect(('10.255.255.255', 1))
            IP = s.getsockname()[0]
        except:
            IP = '127.0.0.1'
        finally:
            s.close()
        return IP

    def get_default_gateway_linux(self):
        """Read the default gateway directly from /proc."""
        with open("/proc/net/route") as fh:
            for line in fh:
                fields = line.strip().split()
                if fields[1] != '00000000' or not int(fields[3], 16) & 2:
                    continue

                return socket.inet_ntoa(struct.pack("<L", int(fields[2], 16)))

    def get_destinations(self):
        url = 'https://raw.githubusercontent.com/noia-network/noia-inspector/master/settings/ping_destinations.json'
        req = requests.get(url)
        if req.status_code == requests.codes.ok:
            try:
                return json.loads(req.content)
            except:
                pass
        print('Destinations was not found, using default destinations')
        with open('/etc/noia-inspector/ping_destinations.json') as json_file:
            return json.load(json_file)

    def get_ping_statistics(self):
        destinations = self.get_destinations()
        destination_ips = list(map(lambda x: f"{x['ip']}/32", destinations))
        results = self.prepare_results(destinations)
        src_ips = [self.get_ip(), None]
        ip.flush_rules(table=TABLE_ID)
        ip.flush_routes(table=TABLE_ID)
        ip.rule('add', src=self.get_ip() + '/32', table=TABLE_ID)
        for dest_ip in destination_ips:
            try:
                ip.route('add', dst=dest_ip, gateway=self.get_default_gateway_linux(), table=TABLE_ID)
            except:
                pass
        self.sdn.connect_sdn(destination_ips)
        while True:
            ping_tmp_results = {}
            with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
                # Start the load operations and mark each future with its URL
                future_to_url = {executor.submit(multiping, **{
                    "addresses": list(results.keys()), "src_addr": src_ip, "max_threads": 200, "interval":  1 if src_ip else 0.9,
                    "count": 400
                }): src_ip for src_ip in src_ips}
                for future in concurrent.futures.as_completed(future_to_url):
                    url = future_to_url[future]
                    try:
                        data = future.result()
                    except Exception as exc:
                        print('%r generated an exception: %s' % (url, exc))
                    else:
                        if data and not data[0].src_addr:
                            ping_tmp_results['SDN'] = data
                        else:
                            ping_tmp_results['PUBLIC'] = data

            results = self.finalize_results(results, ping_tmp_results)
            self.send_results(results)

    def prepare_results(self, destinations):
        results = {}
        for dest in destinations:
            results[dest['ip']] = dest
        return results

    def finalize_results(self, results, ping_tmp_results):
        for i in range(0, len(results.keys())):
            results[ping_tmp_results['PUBLIC'][i].address].update({
                "icmp_public": ping_tmp_results['PUBLIC'][i].avg_rtt,
                "icmp_sdn": ping_tmp_results['SDN'][i].avg_rtt,
                "jitter_sdn": ping_tmp_results['SDN'][i].packet_loss,
                "jitter_public": ping_tmp_results['PUBLIC'][i].packet_loss,
                "hostname": socket.gethostname()
            })
            print(results[ping_tmp_results['PUBLIC'][i].address], '-', ping_tmp_results['PUBLIC'][i].address)
        return results

    def send_results(self, results):
        list_results = []
        for ip in results.keys():
            list_results.append(results[ip])
        self.sdn.send_latency_results_controller(list_results)
