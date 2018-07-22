## Author Abhishek
## Version 1.0
## The code will perform network scan detect the services in the network.
## Compute the IP address which are not used, will be used as decoy to populate the ARP cache the endpoint.
## Besides ARP cache the honey data can be in the  RDP, DNS Tables, key stores,
## honey mapped drives, honey files, VPN Links, Browser Cache, fake certificates/ private
## keys and honey passwords in lsass.exe.
## The code will have to be executed as a privileged user.
## Code is under GPL v3 Licence

import math
import sys
import re
import string
import os
import socket
import tempfile
import traceback
import subprocess
from random import randint
import random


ip_parsing_string = "Nmap scan report for "
## This is the number of Honey entries in the ARP Cache
number_arp_cache = 10

def randomMA():
    honey_mac_address = list()
    i  = 0
    while i < 6 :
        hexnumber = str(hex(random.randint(0x00,0xff))[2:])
        honey_mac_address.append(hexnumber)
        i = i + 1
    mac_address = '-'.join(str(e) for e in honey_mac_address)
    return mac_address

# This part of the code scans the network and generates the 
# IP Address which can be used as entry for ARP cache.

def add_honey_arp_cache():
    global tp
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    IPAddr = (s.getsockname()[0])
    scanip = IPAddr.split('.')[:3]
    scanip.append('*')
    iprange = '.'.join(scanip)
    s.close()
    scan_cmd = ['nmap']
    scan_cmd.append('-sP')
    scan_cmd.append(iprange)
    tp = tempfile.TemporaryFile(mode='w')
    id = 0
    try:
        errfile = open('NUL','w')
        with open(tp.name,'w') as outfile:
            sp = subprocess.Popen(scan_cmd,stdout=outfile,stderr=errfile)
        outfile.close()
        errfile.close()
        id = sp.pid
        sp.wait()
        outfile.close()
    except Exception as e:
        traceback.print_exc()
        tp.close()
        if id!=0:
            kill_task = "kill -9" +str(id)
            os.system(kill_task)
    bv = [0] * 255
    try:
        file = open(tp.name, "r+")
        lines = file.readlines()
        for line in lines:
            if line.find(ip_parsing_string) != -1:
                valid_IP = (line.split(' ')[4])
                try:
                    live_values = valid_IP.split(".")[3]
                except Exception as e:
                    continue
                bv[int(live_values)] = 1
        tp.close()
    except Exception as e:
        traceback.print_exc()

    try:
        for i in range(0, number_arp_cache):
            last_digit = randint(0, 254)
            if bv[int(last_digit)] == 0:
                scanip = IPAddr.split(".")[:3]
                scanip.append(last_digit)
                honeyip = '.'.join(str(e) for e in scanip)
            random_mac = randomMA()
            response  = os.system("ping -n 1 "+ honeyip)
            if response !=0:
                arp_insertion_cmd = "arp -s " + honeyip + " " + random_mac
                print("Adding Honey IP Address and MAC in the Arp Cache", honeyip)
                os.system(arp_insertion_cmd)
    except Exception as e:
        traceback.print_exc()

def main():
    try:
        add_honey_arp_cache()
    except Exception as e:
        traceback.print_exc()

if __name__ == "__main__":
    main()
