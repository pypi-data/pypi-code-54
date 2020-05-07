import subprocess
import requests
import json
import os
from time import sleep
from pathlib import Path
from jinja2 import Template
from icmplib import ping

wg0_template = Template(
    "[Interface]\n"
    "Address = {{ app_internal_ipv4 }}/24\n"
    "PrivateKey = {{ PRIVATE_KEY }}\n"
    "DNS = 1.1.1.1, 8.8.8.8\n"

    "[Peer]\n"
    "PublicKey = {{ vpn_public_key }}\n"
    "AllowedIPs = {{ vpn_internal_ipv4 }}/32, {{ app_dest_ip_cidrs }}\n"
    "Endpoint = {{ vpn_endpoint_ip }}\n"
    "PersistentKeepalive = 15\n"
)


class TesterException(Exception):
    pass


class SDN:

    class SDNError(Exception):
        pass

    def __init__(
            self,
            stage=os.environ.get('STAGE'),
            user=os.environ.get('USER_EMAIL'),
            device_id=os.environ.get('DEVICE_ID'),
            controller_token=os.environ.get('CONTROLLER_TOKEN')
    ):
        self.online = False
        self.stage = stage
        self.user = user
        self.device_id = device_id
        self.public_ip_url = 'https://ip.noia.network/'
        self.controller_url = f"https://{self.stage}-controller-server.noia.network/api/apps/"
        self.speedtest_url = f"https://{self.stage}-controller-server.noia.network/api/auth/speedtest-report/"
        self.latency_pair_url = f"https://{self.stage}-controller-server.noia.network/api/auth/pair-latency-test-report/bulk"
        self.speedtest_pair_url = f"https://{self.stage}-controller-server.noia.network/api/auth/pair-speedtest-report/"
        self.controller_token = controller_token
        self.headers = {"Content-type": "application/json", "Authorization": f"{self.controller_token}"}
        self.vpn_id = self.get_vpn_server_id()

    def connect_sdn(self, ip):
        print(f"CONNECTING TO SDN {[ip]}")
        self.disconnect_sdn()
        self.connect_to_controller(ip)
        self.start_wg()
        print(f"MTU - {os.environ.get('MTU', 'default')}")
        if os.environ.get('MTU'):
            self.set_wg_mtu(os.environ['MTU'])
        print(f"CONNECTED TO SDN {[ip]}")
        self.online = True

    def disconnect_sdn(self):
        self.disconnect_from_controller()
        self.stop_wg()
        self.online = False

    def register_app(self):
        self.disconnect_sdn()
        self.connect_sdn(["72.250.28.64/32", "8.8.8.8/32"])
        self.disconnect_sdn()

    def get_vpn_conf(self):
        connect_url = f"{self.controller_url}{self.device_id}/conf?show-routes=NO"
        resp = requests.post(connect_url, headers=self.headers)
        resp.raise_for_status()
        if resp.status_code == 200:
            config = resp.json()
        else:
            raise self.SDNError(resp.json())
        return config

    def connect_to_controller(self, ips):
        connect_url = f"{self.controller_url}connect?reconnect=YES&wait-conf=NO"
        payload = {
            "app_device_id": self.device_id,
            "app_public_key": self.get_public_key(),
            "app_public_ip": self.get_public_ip(),
            "app_dest_ip_cidrs": ips,
            "app_server_vpn_id": self.vpn_id
        }
        resp = requests.post(connect_url, data=json.dumps(payload), headers=self.headers, timeout=120)
        if resp.status_code == 200:
            data = resp.json()
        else:
            try:
                error = resp.json()
            except json.decoder.JSONDecodeError:
                error = resp.status_code
            raise self.SDNError(error)

        while True:
            print("WAITING FOR CONFIG")
            data = self.get_vpn_conf()
            if data['config']:
                break
            sleep(1)
        data = data['config']['params']
        rendered = wg0_template.render(
            app_internal_ipv4=data['app_internal_ipv4'], vpn_public_key=data['vpn_public_key'],
            vpn_internal_ipv4=data['vpn_internal_ipv4'], app_dest_ip_cidrs=', '.join(data['app_dest_ip_cidrs']),
            vpn_endpoint_ip=data['vpn_endpoint_ip'], PRIVATE_KEY=self.get_private_key()
        )
        file = open("/etc/wireguard/wg0.conf", "w")
        file.write(rendered)
        file.close()

    def disconnect_from_controller(self):
        connect_url = f"{self.controller_url}disconnect"
        payload = {"app_device_id": self.device_id}
        resp = requests.post(connect_url, data=json.dumps(payload), headers=self.headers)
        try:
            resp.raise_for_status()
        except requests.exceptions.HTTPError:
            print("LOGOUT FAILED")

    def get_vpn_server_id(self):
        connect_url = f"{self.controller_url}vpn-servers"
        payload = {"app_device_id": self.device_id}

        resp = requests.get(connect_url, data=json.dumps(payload), headers=self.headers)
        resp.raise_for_status()
        if resp.status_code == 200:
            data = resp.json()
        else:
            raise self.SDNError(resp.json())

        latency_best = 5000
        if len(data) < 1:
            raise self.SDNError('NO VPN SERVER')
        else:
            vpn_server_id = data[0]['server_id']
        for server in data:
            latency = ping(server['server_ip'], count=4)
            if latency_best > latency.avg_rtt:
                latency_best = latency.avg_rtt
                vpn_server_id = server['server_id']
        return vpn_server_id

    def send_results_controller(self, results):
        payload = {
            "app_device_id": self.device_id,
            "speedtest_via": results['via'],
            "speedtest_src_ipv4": self.get_public_ip(),
            "speedtest_dst_ipv4": results['dst_ipv4'],
            "speedtest_http_latency": results.get('http_latency', 9999),
            "speedtest_icmp_latency": results.get('icmp_latency', 9999),
            "speedtest_download": results['download'],
            "speedtest_upload": results['upload'],
            "speedtest_execution_time": results['execution_time'],
            "speedtest_country": results['country'],
            "speedtest_city": results['city'],
            "speedtest_host": results['host'],
            "speedtest_traceroute": json.dumps(results.get('traceroute'))
        }
        resp = requests.post(self.speedtest_url, data=json.dumps(payload), headers=self.headers)
        if resp.status_code == 204:
            return
        else:
            raise self.SDNError(resp.json())

    def send_latency_results_controller(self, results):
        payload = []
        public_ip = self.get_public_ip()
        for result in results:
            server = {
                "app_device_id": self.device_id,
                "pair_latency_test_name": result['game'],
                "pair_latency_test_icmp_sdn": result['icmp_sdn'],
                "pair_latency_test_icmp_public": result['icmp_public'],
                "pair_latency_test_jitter_sdn": result['jitter_sdn'],
                "pair_latency_test_jitter_public": result['jitter_public'],
                "pair_latency_test_src_ipv4": public_ip,
                "pair_latency_test_dst_ipv4": result['ip'],
                "pair_latency_test_dst_host": result['hostname'],
                "pair_latency_test_dst_location": result['location'],
                "pair_latency_test_src_host": result['hostname'],
                "additionalProp1": {}
            }
            payload.append(server)
        resp = requests.post(self.latency_pair_url, data=json.dumps(payload), headers=self.headers)
        if resp.status_code == 204:
            print(resp.status_code)
            return
        else:
            raise self.SDNError(resp.json())

    def send_paired_results_controller(self, tester, results):

        payload = {
            "app_device_id": self.device_id,
            "pair_speedtest_http_latency_sdn": results['SDN']['http_latency'],
            "pair_speedtest_icmp_latency_sdn": results['SDN']['icmp_latency'],
            "pair_speedtest_download_sdn": results['SDN']['download_mbps'],
            "pair_speedtest_upload_sdn": results['SDN']['upload_mbps'],
            "pair_speedtest_http_latency_public": results['PUBLIC']['http_latency'],
            "pair_speedtest_icmp_latency_public": results['PUBLIC']['icmp_latency'],
            "pair_speedtest_download_public": results['PUBLIC']['download_mbps'],
            "pair_speedtest_upload_public": results['PUBLIC']['upload_mbps'],
            "pair_speedtest_src_ipv4": self.get_public_ip(),
            "pair_speedtest_src_host": tester.host,
            "pair_speedtest_dst_id": results['speedtest_id'],
            "pair_speedtest_dst_ipv4": results['ip'],
            "pair_speedtest_dst_host": results['host'],
            "pair_speedtest_dst_country": results['country'],
            "pair_speedtest_dst_city": results['city'],
            "pair_speedtest_type": tester.speedtest_type,
            "additionalProp1": {}
        }
        resp = requests.post(self.speedtest_pair_url, data=json.dumps(payload), headers=self.headers)
        if resp.status_code == 204:
            return
        else:
            try:
                error = resp.json()
            except json.decoder.JSONDecodeError:
                error = resp.status_code
            raise self.SDNError(error)

    def start_wg(self):
        subprocess.run('wg-quick down wg0'.split(), encoding='utf-8', stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        result = subprocess.run('wg-quick up wg0'.split(), encoding='utf-8', stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE)

    def stop_wg(self):
        subprocess.run('wg-quick down wg0'.split(), encoding='utf-8', stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    def set_wg_mtu(self, mtu):
        subprocess.run(f'ip link set dev wg0 mtu {mtu}'.split(), encoding='utf-8', stdout=subprocess.PIPE,
                       stderr=subprocess.PIPE)

    def get_public_key(self):
        return Path(os.environ.get('WG_PUBLIC_KEY', os.environ['WG_PRIVATE_KEY'])).read_text().strip()

    def get_private_key(self):
        return Path(os.environ.get('WG_PRIVATE_KEY', os.environ['WG_PUBLIC_KEY'])).read_text().strip()

    def get_public_ip(self):
        resp = requests.get(self.public_ip_url)
        return resp.json()
