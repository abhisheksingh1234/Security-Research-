## Author Abhishek. 
## Version 0.0 
## The code will perform network scan to detect the services in the network 
## Compute the IP address which are not in used and use it as decoy. These Decoys will be added in the ARP cache the endpoint. 
## Besides ARP cache the honey data can be in the  RDP, DNS Tables, key stores,
## honey mapped drives, honey files, VPN Links, Browser Cache, fake certificates/ private
## keys and honey passwords in lsass.exe. 
## License GPL v3

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

tpath = "/tmp"
ip_parsing_string = "Nmap scan report for "
number_arp_cache = 10

def randomMA():
    return [random.randint(0x00,0xff),
            random.randint(0x00,0xff),
            random.randint(0x00,0xff),
            random.randint(0x00,0x7f),
            random.randint(0x00,0xff),
            random.randint(0x00,0xff) ]

def MACaddr(mac):
    return ':'.join(map(lambda x: "%02x" %x, mac))


# This part of the code scans the network and generates the 
# IP Address which can be used as entry for ARP cache.

def honey_arp_cache():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8",80))
    IPAddr = (s.getsockname()[0])
    scanip = IPAddr.split('.')[:3]
    scanip.append('*')
    iprange = '.'.join(scanip)
    s.close()
    try:
        tp = tempfile.NamedTemporaryFile(dir=tpath)
    except Exception as e:
        traceback.print_exc()
    id = 0 
    scan_cmd_arp = 'nmap -sP '+ iprange +' > '+tp.name
    
    os.system(scan_cmd_arp)
    bv = [0] * 255	
    try:
        file = open(tp.name,"r")
        lines = file.readlines()
        for line in lines:
            if line.find(ip_parsing_string)!= -1:
                valid_IP = (line.split(' ')[4])
                print ("The active IP are :",valid_IP)
                try:
                    live_values =  valid_IP.split(".")[3]
                except Exception as e:
                    continue
                bv[int(live_values)] = 1
        tp.close()

                    
    except Exception as e:
        traceback.print_exc()

    try:

        for i in range(0,number_arp_cache):
            last_digit = randint(0,255)
            if bv[int(last_digit)] == 0:
                scanip = IPAddr.split(".")[:3]
                scanip.append(last_digit)
                honeyip = '.'.join(str(e) for e in scanip)
                arp_insertion_cmd = "arp -s "+ honeyip + " " +(MACaddr(randomMA()))
                print ("Adding Honey IP Address and MAC in the Arp Cache", honeyip)
                os.system(arp_insertion_cmd)
    
    except Exception as e:
        traceback.print_exc()
        



def main():
	try:
            honey_arp_cache()
	except Exception as e:
            traceback.print_exc()
	

if __name__ =="__main__":
	main()
