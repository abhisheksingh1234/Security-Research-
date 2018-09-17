# Author abhi
# The code detects DGA domains
# The function which calculates the shannon_entropy is available at 
# http://code.activestate.com/recipes/577476-shannon-entropy-calculation/  under MIT license. 
# If the Shannon Entropy of the domain is greater than 4.1 it marks it as a DGA or else labels it as a probable DGA. 
# This code is under MIT License. 


import math
import sys
import time
import traceback
import sys
import re
import string
import json
import math
from sets import Set
import tldextract

malicious_score = 4.1
suspicious_score = 3.3

def shannon_entropy(st):
	stList = list(st)
	alphabet = list(Set(stList))
	freqList = []
	for symbol in alphabet:
    		ctr = 0
    		for sym in stList:
        		if sym == symbol:
           			 ctr += 1
    		freqList.append(float(ctr) / len(stList))
	ent = 0.0
	for freq in freqList:
    		ent = ent + freq * math.log(freq, 2)
	ent = -ent
	return ent

def dga(URL):

	try:
	
		ext = tldextract.extract(URL)
		
	except Exception as e:
		return 0

	try:
	 	ent = shannon_entropy(ext.domain)
		
		if ent >= malicious_score :
                 	print("DGA_Domain")   
		if ent >= suspicious_score and ent <= malicious_score :
					print("Probable_DGA_Domain") 
	except Exception as e:
		return 0

	return 0

def main():
        name = str(sys.argv[0])
        URL = sys.argv[1]
	try:
        	dga(URL)
	except Exception as e:
                traceback.print_exc()		
        


if __name__ =="__main__":main()
