# Code computes the similarity of the JS file from the existing signatures stored under signatures. 
# It uses Esprima for the lexical analysis of the code. Then make call to ast2xl to convert into XML. 
# The XML is compared with the stored signatures which will be under signatures 
# To invoke the script use  python similarity.py <name.js>
# To compute signatures node esprima.js <name.js> > signature.
# python ast2xl signature > signature.xml

import os
import sys
import xml.etree.cElementTree as ET
from os import listdir
import glob
import traceback
import tempfile
import subprocess
import signal
import time
import stat
import shutil
import commands
import json

sample_path = "/JS"
tpath = "/tmp"

similarity_score = 0.85

def code_similarity(filename,sample_name):

	eliminated = [{'s': 'value', '_name': 'Str'},
        	        {'s': 'value', '_name': 'Str'},
                	{'s': 'type', '_name': 'Str'},
               		{'s': 'raw', '_name': 'Str'}]

	safetyStrings = ["ast", "ast {}", "None", "type", "body", "Program",
                                "declarations", "kind", "VariableDeclaration", "name",
                                "Identifier", "var", "id", "init", "ExpressionStatement",
                                "operator", "left", "right", "AssignmentExpression",
                                "EmptyStatement", "Literal", "raw", "MemberExpression",
                                "consequent", "alternate", "IfStatement", "LogicalExpression",
                                "||", "prefix", "UnaryExpression", "!", "computed", "object",
                                "property", "value", "window", "expression", "false",
                                "VariableDeclarator", "callee", "arguments", "=",
                                "elements", "ArrayExpression", "CallExpression",
                                "arguments", "argument", "alert", "BlockStatement",
                                "BinaryExpression", "NewExpression", "BinaryExpression",
                                "+", "ReturnStatement", "appendChild", "Elem",
                                "ReturnStatement", "FunctionDeclaration", "params", "generator",
                                "defaults", "true", "regex", "ThisExpression", "<", ">",
                                "ForStatement", "FunctionExpression", "Array", "ThisExpression",
                                "UpdateExpression","length", "WhileStatement", "properties",
                                "ObjectExpression", "++", "update", "ForInStatement", "each",
                                "String", "pattern", "flags", "SequenceExpression",
                                "expressions", "Math", "round", "getElementById",
                                "ConditionalExpression", "test", ">>>", "<<<", "&&", "-=",
                                "+=", "-", ">=", "<=", "substr"]

	#filename = signature_path+filename
        #sample_name = tpath + sample_name
        
	tree1 = ET.ElementTree(file=filename)
	tree2 = ET.ElementTree(file=sample_name)

	print(filename)
	root1 = tree1.getroot()
	root2 = tree2.getroot()

	treeDict1 = {}
	treeDict2 = {}
	score = 0.0

	for elem in tree1.iter():
    		elem.attrib.pop("col_offset", None)
    		elem.attrib.pop("lineno", None)

	for elem in tree2.iter():
    		elem.attrib.pop("col_offset", None)
    		elem.attrib.pop("lineno", None)


	interator = 0

	for child in tree1.getroot().iter("*"):
    		if child.tag == "_list_element" and child.attrib.get("_name") != "Dict" and child.attrib not in eliminated:
        		treeDict1[interator] = (child.tag, child.attrib)
    			interator += 1

	interator = 0

	for child in tree2.getroot().iter("*"):
    		if child.tag == "_list_element" and child.attrib.get("_name") != "Dict" and child.attrib not in eliminated:
        		treeDict2[interator] = (child.tag, child.attrib)
        		interator += 1

	for maxD in xrange(100):
    		matches = 0

	    	for (k,v), (k2,v2) in zip(treeDict1.items(), treeDict2.items()):
        		for x in xrange(0, maxD):
            			if(v == treeDict2.get(k2+x)):
                			matches += 1
                			break
            			elif(v == treeDict2.get(k2-x)):
                			matches += 1
                			break
            			elif(v2 == treeDict1.get(k+x)):
                			matches += 1
                			break
            			elif(v2 == treeDict1.get(k-x)):
                			matches += 1
                			break

    		#print "(", maxD, ",", matches, ")", " : ", min(float(matches) / len(treeDict1),  float(matches) / len(treeDict2))
		score = score + min(float(matches) /len(treeDict1), float(matches)/len(treeDict2))
	
	print float((score)/(maxD))
	if (float((score)/(maxD)) > similarity_score):
		return 1

	return 0


def invoke_similarity(sample_name):
	try:
		status = 0
		filepath = os.getcwd()
		signature_path = "/signatures/"
		signature_path = filepath+signature_path
		for root, dirs, files in os.walk(signature_path):
			for index in range((len(files))):
				status = code_similarity(signature_path + files[index],sample_name)
				if status == 1:
					print("Code_Similarity_Found")
					return 0
			
	except Exception as e:
		traceback.print_exc()
	return 0
	

def invoke_nodejs(filename):  
	filepath = os.getcwd()
	filename = filepath+"/"+filename
	tp = tempfile.NamedTemporaryFile(dir=tpath)
	tp_signature = tempfile.NamedTemporaryFile(dir=tpath)
	node_js_cmd = ['node']
	node_js_cmd.append('esprima.js') 
	node_js_cmd.append(filename)
	id = 0
	try:
		errfile = open('/dev/null','w')
		with open(tp.name,'w') as outfile:
			sp = subprocess.Popen(node_js_cmd,stdout=outfile,stderr=errfile)
		outfile.close()
                errfile.close()
                id = sp.pid
                sp.wait()
                outfile.close()
        except Exception as e:
		traceback.print_exc()
		tp.close()
		if id!= 0:
			kill_task = "kill -9 "+str(id)
			os.system(kill_task)

	ast_2_xml_cmd = ['python']
	ast_2_xml_cmd.append('ast2xml.py')  
	ast_2_xml_cmd.append(tp.name)
	try:
		errfile = open('/dev/null','w')
                with open(tp_signature.name,'w') as outfile:
                        sp = subprocess.Popen(ast_2_xml_cmd,stdout=outfile,stderr=errfile)
                outfile.close()
                errfile.close()
                id = sp.pid
                sp.wait()
                outfile.close()
        except Exception as e:
                traceback.print_exc()
                if id!= 0:
                        kill_task = "kill -9 "+str(id)
                        os.system(kill_task)
	tp.close()
	try:
   		invoke_similarity(tp_signature.name)
	except Exception as e:
		traceback.print_exc()
		tp_signature.close()
	tp_signature.close()

def main():
        filename = sys.argv[1]
	invoke_nodejs(filename)

if __name__=="__main__":main()
