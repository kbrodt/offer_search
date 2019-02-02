#!D:/Python36/python.exe
# -*- coding: utf-8 -*-
import json
import requests

import sys
import codecs

import cgi 

storage = cgi.FieldStorage()
data = storage.getvalue('data')
if data is not None:
	print("Content-Type: text/html; charset=utf-8\n")
	#Create json
	with open('ranker_out.json', 'r', encoding='utf-8') as fh:
		data = json.load(fh, encoding='utf-8')
		
	sys.stdout = codecs.getwriter("utf-8")(sys.stdout.detach())

	#response = requests.get('http://localhost/tinkoff/py/ranker_out.json')
	print(data)