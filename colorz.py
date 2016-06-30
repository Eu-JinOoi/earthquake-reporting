#!/usr/local/bin/python3
import http.client as httplib
import json
import requests
import socket


#COLOR DEFINITION
class colorz:
	HEADER = '\033[95m'
	OKBLUE = '\033[94m'
	OKGREEN = '\033[92m'
	WARNING = '\033[93m'
	FAIL = '\033[91m'
	ENDC = '\033[0m'
	BOLD = '\033[1m'
	UNDERLINE = '\033[4m'
	
	def pretty(text,color):
		if(color=='red'):
			return colorz.BOLD+colorz.FAIL+text+colorz.ENDC
		elif (color=='green'):
			return colorz.OKGREEN + text + colorz.ENDC;
		elif (color=='yellow'):
			return colorz.WARNING + text + colorz.ENDC;
		else:
			return text;


