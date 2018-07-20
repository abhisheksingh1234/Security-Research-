## The code will create fake directory map honey mapped drive to it. 
##  Author Abhi.
import math
import sys
import re
import string
from ctypes import windll
import os
import socket
import tempfile
import traceback
import subprocess
from random import randint
import random

## The parameter defines numer of honey drives which will be added at the endpoint.
number_hmapped_drives = 2

def get_drives():
    drives = []
    bitmask = windll.kernel32.GetLogicalDrives()
    for letter in string.uppercase:
        if bitmask & 1:
            drives.append(letter)
        bitmask >>= 1
    return drives

def add_honey_mapped_drives():
    drives = []
    drives = get_drives()
    count = 0
    count = number_hmapped_drives
    count = count + len(drives)
    try:
        os.system("mkdir c:\\fd")
    except Exception as e:
        pass
    ascii_drive = 65
    i = 0
    while i < count:
        cmd = "subst " + chr(ascii_drive)+":"+ " c:\\fd"
        try:
            os.system(cmd)
        except Exception as e:
            return()
        i = i + 1
        ascii_drive = ascii_drive + 1
        if ascii_drive > 122:
            return()

def main():
    try:
        add_honey_mapped_drives()
    except Exception as e:
        traceback.print_exc()

if __name__ == "__main__":
    main()
