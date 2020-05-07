import click
import uuid
import sys
import os
import settings
import socket

from pprint import pprint

from lib.sdn_client import SDN
from lib.sdn_speedtest import Tester
from lib.sdn_pinger import Pinger

if not os.geteuid() == 0:
    sys.exit("\nOnly root can run this app\n")


@click.command()
@click.option('--addr', prompt='ip or url to connect', help='ip to sdn')
def connect_sdn(addr):
    """Simple SDN CLI App."""
    try:
        socket.inet_aton(addr)
    except socket.error:
        addr = socket.gethostbyname(addr)
    sdn = SDN()
    try:
        sdn.connect_sdn(addr)
    except sdn.SDNError as e:
        print(e)
        print("Error, could not connect.")
        return
    print(f"CONNECTED TO {addr}")
    while True:
        msg = input("type exit to disconnect...")
        if msg.lower() == 'exit':
            sdn.disconnect_sdn()
            return


@click.command()
def run_tests():
    """Simple SDN Tests."""
    tester = Tester()
    result = tester.get_ping_statistics()
    pprint(result)

@click.command()
def run_pinger():
    """Simple SDN Tests."""
    tester = Pinger()
    result = tester.get_ping_statistics()
    pprint(result)


@click.command()
def run_api():
    """SDN Api"""
    from lib import flask_app
    flask_app.run_api()
