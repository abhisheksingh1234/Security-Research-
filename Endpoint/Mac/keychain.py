## Author Abhishek. 
## Version 0.0 
## The code will perform network scan to detect the services in the network 
## Compute the IP address which are not in used and use it as decoy.
## It will generate random names & password  which will be added in the Key Chain
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
import keyring
import names

tpath = "/tmp"
ip_parsing_string = "Nmap scan report for "
number_up_cache = 10

# This part of the code scans the network and generates the 
# IP Address which can be used as entry for ARP cache.

def honey_up_cache():
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
		username = names.get_full_name()
		password = names.get_first_name()
              	keyring.set_password(honeyip,username,password)  
                #print(honeyip,username,password)
		#print(keyring.get_password(honeyip,username))
		print ("Adding Honey Entries in Key Chain")
    
    except Exception as e:
        traceback.print_exc()
        



def main():
	try:
            honey_up_cache()
	except Exception as e:
            traceback.print_exc()
	

if __name__ =="__main__":
	main()

