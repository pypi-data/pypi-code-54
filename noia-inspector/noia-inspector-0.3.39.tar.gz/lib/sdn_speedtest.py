import socket
import json
import statistics
import speedtest
import requests
import random
import os

from time import time
from icmplib import ping

from lib.sdn_client import SDN
from lib.traceroute import trace
from lib.noia_speedtest import NoiaSpeedtest


class SpeedTestType:

    AZURE = 'AZURE'
    AMBASSADOR = 'AMBASSADOR'


class Tester:

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

    def get_destinations(self):
        url = 'https://raw.githubusercontent.com/noia-network/noia-inspector/master/settings/destinations.json'
        req = requests.get(url)
        if req.status_code == requests.codes.ok:
            try:
                return json.loads(req.content)
            except:
                pass
        print('Destinations was not found, using default destinations')
        with open('/etc/noia-inspector/destinations.json') as json_file:
            return json.load(json_file)

    def get_ping_statistics(self):
        results, ip_list = self.init_results()
        try:
            self.sdn.connect_sdn(ip_list)
        except self.sdn.SDNError as e:
            return str(e)

        for speedtest_id in results.keys():
            self.speedtest_run_controller(results, [speedtest_id], 'SDN')

        self.sdn.disconnect_sdn()

        for speedtest_id in results.keys():
            print("Testing without SDN")
            self.speedtest_run_controller(results, [speedtest_id], 'PUBLIC')

        self.finish_results_speedtest(results)
        with open('/etc/noia-inspector/results.json', 'w', encoding='utf-8') as f:
            json.dump(results, f, ensure_ascii=False, indent=4)
        return results

    def speedtest_run_controller(self, results, server_list, stage):
        for server in server_list:
            st = time()
            test_obj = {}

            try:
                s = NoiaSpeedtest()
                print('-------- Testing server number ' + str(server) + '------------------')
                s.get_servers([server])
                s.download(threads=None)
                s.upload(threads=None)
                results_dict = s.results.dict()
                et = time()
                target_host = results_dict['server']['host'].split(':')[0]
                latency = ping(target_host, count=4)
                dst_ipv4 = socket.gethostbyname(target_host)
                controller_results = {
                    'via': stage,
                    'dst_ipv4': dst_ipv4,
                    'latency': latency.avg_rtt,
                    'download': round(results_dict["download"] / 1024 / 1024, 2),
                    'upload': round(results_dict['upload'] / 1024 / 1024, 2),
                    'execution_time': int((et - st) * 1000),
                    'http_latency': int(results_dict['ping']),
                    'icmp_latency': latency.avg_rtt,
                    'country': results_dict['server']["country"],
                    'city': results_dict['server']["name"],
                    'host': results_dict['server']["host"],
                }

                if stage == 'PUBLIC' and self.speedtest_type != SpeedTestType.AZURE:
                    try:
                        print(f"Starting traceroute - {dst_ipv4}")
                        traceroute_res = trace({}, 1, 30, dst_ipv4, "ABCDEFG")
                        controller_results.update({'traceroute': traceroute_res})
                    except Exception as e:
                        controller_results.update({'traceroute': str(e)})

                # Generate data object
                test_obj['download_mbps'] = round(results_dict["download"] / 1024 / 1024, 2)
                test_obj['upload_mbps'] = round(results_dict['upload'] / 1024 / 1024, 2)
                test_obj['http_latency'] = results_dict['ping']
                test_obj['icmp_latency'] = latency.avg_rtt
                self.sdn.send_results_controller(controller_results)

            except Exception as e:
                test_obj = {"ERROR": str(e)}
            results[server][stage] = test_obj
            if stage == 'PUBLIC' and not test_obj.get('ERROR') and not results[server].get('SDN', {}).get('ERROR'):
                try:
                    self.sdn.send_paired_results_controller(self, results[server])
                except self.sdn.SDNError as e:
                    print(f"SEND PAIRED RESULTS FAILED {e}")
            elif test_obj.get('ERROR'):
                print(f"Skipping {server}, {test_obj['ERROR']}")
        return results

    def init_results(self):
        destinations = self.get_destinations()
        random.shuffle(destinations)
        res = {}
        ip_list = []
        s = NoiaSpeedtest()
        try:
            results_dict = s.get_servers(destinations)
        except speedtest.NoMatchedServers:
            print(f"Speedtest servers - Not Found")
            return res, ip_list
        for server in results_dict.values():
            server_info = server[0]
            hostname = (server_info['host'].split(':')[0])
            try:
                host_ip = socket.gethostbyname(hostname)
            except socket.gaierror:
                continue
            res[server_info['id']] = {
                'ip': host_ip,
                'speedtest_id': server_info['id'],
                'host': hostname,
                'country': server_info.get('country'),
                'city': server_info.get('name'),
                'PUBLIC': {
                    'timeout': 0, 'latency': []
                },
                'SDN': {
                    'timeout': 0, 'latency': []
                }
            }
            ip_list.append(f"{host_ip}/32")
        return res, ip_list

    def finish_results_speedtest(self, results):
        for ip in results.keys():
            results[ip]['diff_sdn'] = {}
            if not results[ip]['SDN'].get("ERROR", False) and not results[ip]['PUBLIC'].get("ERROR", False):
                results[ip]['diff_sdn']['diff_download_mbps'] = results[ip]['SDN']['download_mbps'] - results[ip]['PUBLIC']['download_mbps']
                results[ip]['diff_sdn']['diff_upload_mbps'] = results[ip]['SDN']['upload_mbps'] - results[ip]['PUBLIC']['upload_mbps']
                results[ip]['diff_sdn']['diff_icmp_latencys'] = results[ip]['SDN']['icmp_latency'] - results[ip]['PUBLIC']['icmp_latency']
                results[ip]['diff_sdn']['diff_http_latency'] = results[ip]['SDN']['http_latency'] - results[ip]['PUBLIC']['http_latency']

    def finish_results_ping(self, results):
        for ip in results.keys():
            count = len(results[ip]['PUBLIC']['latency'])
            if count > 1:
                results[ip]['PUBLIC']['avarage'] = sum(results[ip]['PUBLIC']['latency']) / count
                results[ip]['PUBLIC']['standard_deviation'] = statistics.stdev(results[ip]['PUBLIC']['latency'])
                results[ip]['PUBLIC']['max'] = max(results[ip]['PUBLIC']['latency'])
                results[ip]['PUBLIC']['min'] = min(results[ip]['PUBLIC']['latency'])

            count = len(results[ip]['SDN']['latency'])
            if count > 1:
                results[ip]['SDN']['avarage'] = sum(results[ip]['SDN']['latency'])/len(results[ip]['SDN']['latency'])
                results[ip]['SDN']['standard_deviation'] = statistics.stdev(results[ip]['SDN']['latency'])
                results[ip]['SDN']['max'] = max(results[ip]['SDN']['latency'])
                results[ip]['SDN']['min'] = min(results[ip]['SDN']['latency'])
