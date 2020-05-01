#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
B.S.D.
Created on Wed Apr 29 09:57:53 2020

@author: Sara Ben Shabbat
"""

from vpn_exclude_sbs import utilities as util
import sys

def get_author_details() -> str:
    return 'Name: Sara Ben Shabbat\nE-mail: sarabenshabbat@gmail.com\nPhone: +972-55-6790404'
    

def excluding(argv) -> None:
    # When first param is '-ip', exclude the given ip, else (- when the
    # first param is '-url' exclude all the ip's of the givan domain name.)
    ips_lst = util.get_ip(argv[2]) if argv[1] == '-ip' else util.get_ip_from_url(argv[2])
    
    if(ips_lst != []):    
        default_gateway = util.get_default_gateway()
        util.exclude_ips(default_gateway, ips_lst)        


def main(argv) -> int:
    try:    
        excluding(argv)
        return 0
    except:
        return 1
 
    
if __name__ == "__main__":
    sys.exit(main(sys.argv))


