""" Core module with cli """
import winrm
import sys
import click
import socket
from pyscan_annek import sweep
from pyscan_annek import pymail
from pyscan_annek import shelf
from datetime import datetime
from pprint import pprint

@click.group()
def main():
    """
    Pyscan is a cli tool for scanning subnets for hosts.
    It can check a Windows station hostname with pywinrm.
    It can also check service status on a Windows host.

    Example: pynet more-help --help
    """


@main.command()
@click.option("--helptext", is_flag=True, help="Print extra help")
def more_help(helptext):
    """ Various help options for usage information """
    result = "Use --help to view usage"
    if helptext:
        result = print_more_help()
    print(result)


@main.command("check-mgmt-ports", short_help="Check for open mgmt ports")
@click.argument("ip-address")
def check_mgmt_ports(ip_address):
    """ Port scan a device to check for open mgmt ports """
    ports = [22,3389, 5985]
    valid_ports = []
    for port in ports:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        result = sock.connect_ex((ip_address,port))
        if result == 0:
            print(f"Port {port} is open")
            valid_ports.append(port)
        else:
            print(F"Port {port} is not open")
        sock.close()
    return valid_ports


@main.command("get-win-hostname", short_help="Get a windows machine's hostname")
@click.argument("ip-address")
@click.argument("username")
@click.argument("password")
def get_win_hostname(ip_address, username, password):
    """ Uses pywinrm to log in to host and run hostname command """
    session = winrm.Session(ip_address, auth=(username, password), transport='ntlm')
    result = (session.run_cmd('hostname'))
    hostname = result.std_out.decode()
    print(f"Windows machine at {ip_address} has a hostname of {hostname}")
    return hostname


@main.command("check-service-status", short_help="Check service on a Windows host")
@click.argument("ip-address")
@click.argument("username")
@click.argument("password")
@click.argument("service_name")
def check_service_status(ip_address, username, password, service_name):
    """ Uses pywinrm to log in to host and run get-service cmdlet """
    session = winrm.Session(ip_address, auth=(username, password), transport='ntlm')
    command = (f'sc query {service_name}')
    print(f"Running the following on the host '{command}'")
    result = (session.run_cmd(command))
    strres = (result.std_out.decode())
    print(f"Result of command is '{strres}'")
    if 'RUNNING' in strres.split():
        print("Service is running")
        now = datetime.now()
        date_time = now.strftime("%m_%d_%Y--%H_%M_%S")
        print("date and time:",date_time)	
        shelf.shelf_add_item('services', ip_address, str(service_name + ' ' + 'Running' + ' ' + date_time))
        return 0
    else:
        print("Service is not running or is unavailable")
        return 1


@main.command("check-svc-stat-sendnotice", short_help="Check status of Win service, send email")
@click.argument("ip-address")
@click.argument("username")
@click.argument("password")
@click.argument("service_name")
@click.argument("recipient-emailaccount")
@click.argument("smtpaccount-password")
def check_svc_stat_sendnotice(ip_address, username, password, service_name, recipient_emailaccount, smtpaccount_password):
    """ Uses pywinrm to log in to host and run get-service cmdlet, sends email if service is down """
    session = winrm.Session(ip_address, auth=(username, password), transport='ntlm')
    command = (f'sc query {service_name}')
    print(f"Running the following on the host '{command}'")
    result = (session.run_cmd(command))
    strres = (result.std_out.decode())
    print(f"Result of command is '{strres}'")
    if 'RUNNING' in strres.split():
        print("Service is running")
        now = datetime.now()
        date_time = now.strftime("%m_%d_%Y--%H_%M_%S")
        print("date and time:",date_time)	
        shelf.shelf_add_item('services', ip_address, str(service_name + ' ' + 'Running' + ' ' + date_time))
        return 0
    else:
        print("Service is not running or is unavailable")
        mail = pymail.mail(service_name, 'Not-Reachable', ip_address, recipient_emailaccount, smtpaccount_password)
        return mail


@main.command("list-shelf-data", short_help="Print data in a shelf")
@click.argument("shelf_name")
def list_shelf_data(shelf_name):
    shelf.shelf_list_contents(shelf_name)


@main.command("send-notice", short_help="Send a notification via email")
@click.argument("email-address")
@click.argument("login-password")
@click.argument("hostname")
@click.argument("service-name")
@click.argument("status-message")
def send_notice(email_address, login_password, service_name, hostname, status_message):
    """ Uses the pymail module to send a notification email about a service from rimsd.filesend@rimschools.org

    Arguments:
        email-address: Recipient address,
        login-password: Password for rimsd.filesend@rimschools.org,
        service-name: Service name that is affected,
        hostname: The name of the server that is affected,
        status-message: State of the service
    """
    mail = pymail.mail(service_name, status_message, hostname, email_address, login_password)
    return mail


@main.command("get-iprange-alivehosts", short_help="Get hosts that are alive in ip range")
@click.argument("subnet")
def get_iprange_alivehosts(subnet):
    """ Get hosts that are alive in ip range ex.'192.168.10' """
    ips = sweep.sweep(subnet)
    ips.sort()
    pprint(ips)
    return ips


def print_more_help():
    """ Prints help message """
    help_text = """
    This is some extra help TODO

    """
    return help_text



if __name__ == "__main__":
    main()
