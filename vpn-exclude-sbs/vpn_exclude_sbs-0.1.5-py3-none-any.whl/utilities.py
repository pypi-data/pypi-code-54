#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
B.S.D.
Created on Wed Apr 29 10:01:43 2020

@author: Sara Ben Shabbat
"""

import re
import socket
import netifaces
import subprocess

def validate_ip(ip_address: str) -> bool:
    valid_ip_address = "^(([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\.){3}([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])$";
    
    return re.match(valid_ip_address, ip_address) is not None
    
    
def get_ip(ip_address: str) -> list:
    if(validate_ip(ip_address) == True):
        return [ip_address]
    else:
        print('Error: \'{}\' isn\'t a valid ip address.'.format(ip_address))
        return []
    
    
def validate_url(domain_name: str) -> bool:
    valid_domain_name = re.compile(
                        r'^(?:http|ftp)s?://' # http:// or https://
                        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|' #domain...
                        r'localhost|' #localhost...
                        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})' # ...or ip
                        r'(?::\d+)?' # optional port
                        r'(?:/?|[/?]\S+)$', re.IGNORECASE)
    
    return re.match(valid_domain_name, domain_name) is not None
    
    
def format_url(domain_name: str) -> str:
    return domain_name.split('/')[2]


def get_ip_from_url(domain_name: str) -> list:
    if(validate_url(domain_name) == True): 
        domain_name = format_url(domain_name)
         
        ips_lst = []
        try:
            ips_lst = socket.gethostbyname_ex(domain_name)[2]
        finally:
            return ips_lst
    else:
        print('Error: \'{}\' isn\'t a valid domain name.'.format(domain_name))
        return []
             

def get_default_gateway() -> str:
    gws = netifaces.gateways()
    return gws['default'][netifaces.AF_INET][0]


def exclude_ips(default_gw: str, ips_lst: list) -> None:
    for ip in ips_lst:
        cmd = 'route -p add ' + ip + ' mask 255.255.255.255 ' + default_gw
        process = subprocess.Popen(cmd,
                                   shell=True,
                                   stdout=subprocess.PIPE,
                                   stderr=subprocess.PIPE)
        errcode = process.returncode

        if errcode is not None:
            raise Exception('cmd {} failed, see above for details'.format(cmd))
 

