import threading
import time
import random
import optparse
import os
from scapy.all import *


class WifiSniffer:
    
    wlan_man = 'wlan0'
    wlan_mon = 'wlan0mon'


    @staticmethod
    def see_routes():
        print('\n\n\033[1;36m Available routes on your network: ')
        return conf.route

    @classmethod
    def monMode(cls):
        print('your wifi card will be set to monitor mode \n')
        try:
            os.system(f'airmon-ng start {cls.wlan_man}')
            print('\033[1;1m\n*** Wifi card is set to monitor mode ***\n')
        except:
            print('there was an error doing that..')

    @classmethod
    def manMode(cls):
        print('your wifi card will be set back to managed mode \n')
        try:
            os.system(f'airmon-ng stop {cls.wlan_mon}')
            print('\033[1;1m\n*** Wifi card is set managed mode ***\n')
        except:
            print('something went wrong..')

    @classmethod
    def hopper(cls):
        n = 1
        stop_hopper = False
        while not stop_hopper:
            time.sleep(.5)
            os.system(f'iwconfig {cls.wlan_mon} channel {n}')
            dig = int(random.random() * 14)
            if dig != 0 and dig != n:
                n = dig

    @staticmethod
    def seeSSID(pkg):
        ap_list = []
        if pkg.haslayer(Dot11Beacon):
            if pkg.getlayer(Dot11).addr2 not in ap_list:
                ap_list.append(pkg.getlayer(Dot11).addr2)
                ssid = pkg.getlayer(Dot11Elt).info
                if ssid == '' or pkg.getlayer(Dot11Elt).ID != 0:
                    print('\033[1;31m Hidden Network Detected')
                time.sleep(.7)
                print(f'\033[0;32m Network Detected: {ssid}')

    @staticmethod
    def findPkg(pkg):
        if pkg.haslayer(Dot11Beacon):
            time.sleep(.8)
            print('Detected 802.11 Beacon Frame')
        elif pkg.haslayer(Dot11ProbeReq):
            time.sleep(.8)
            print('Detected Probe Request Frame')
        elif pkg.haslayer(TCP):
            time.sleep(.8)
            print('Detected a TCP package')
        elif pkg.haslayer(DNS):
            time.sleep(.8)
            print('Detected DNS package')

    @staticmethod
    def sniffTCP(pkg):
        if pkg.haslayer(Raw):
            payload = pkg.getlayer(Raw).load
            if 'GET' in payload:
                if 'google' in payload:
                    r = re.findall(r'(?i)\&q=(.*?)\&'.payload)
                    if r:
                        search = r[0].split('&')[0]
                        search = search.replace('q=', '').replace('+', ' ').replace('%20', ' ')
                        print('[+] Searched for: ' + search)



class BTSniffer():

    btSocket = ''


    @staticmethod
    def check_btDevice():
        print('If there is no BT device shown, there is none.')
        os.system('hcitool dev')
        return

    @classmethod
    def set_btSocket(cls):
        bt = BluetoothHCISocket(0)
        cls.btSocket = bt
        return

    @classmethod
    def sniff_bt(cls):
        print('\n\033[1;32m Sniffing for bluetooth packages..')
        pkg = cls.btSocket.sniff()
        pkg


class BTLowEnergy(BTSniffer):

    @classmethod
    def activeScan(cls):
        print('\n')
        try:
            cls.btSocket.sr(
                HCI_Hdr()/
                HCI_Command_Hdr()/
                HCI_Cmd_LE_Set_Scan_Parameters(type=1)/
                HCI_Cmd_LE_Set_Scan_Enable(
                    enable=True,
                    filter_dups=True))
        except KeyBoardInterrupt:
            print('Active scan was interrupted\n')
        bgr_event = cls.btSocket.sniff(
                lfilter=lambda p: HCI_LE_Meta_Advertising_Reports in p)
        print('\n\nHCI Background events could get fetched: \n {}'.format(bgr_event))
        return

    @classmethod
    def deactiveScan(cls):
        print('\n\n')
        cls.btSocket.sr(
                HCI_Hdr()/
                HCI_Command_Hdr()/
                HCI_Cmd_LE_Set_Scan_Enable(
                    enable=False))


if __name__ == '__main__':

    pass
