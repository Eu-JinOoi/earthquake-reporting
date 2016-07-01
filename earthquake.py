#!/usr/local/bin/python3
import http.client as httplib
import json, geojson
from colorz import colorz
#from colorama import init
#from termcolor import colored

#Uncomment if using colorama or termcolor
#init();

#COLOR DEFINITION
class earthquake:
	
	#properties
	magnitude	= "";
	place		= "";
	time		= 0;
	updated		= 0;
	tz		= 0;
	url		= "";
	detail		= "";
	felt		= "";
	cdi		= "";
	mmi		= "";
	alert		= "";
	status		= "";
	tsunami		= "";
	sig		= "";
	net		= "";
	code		= "";
	ids		= "";
	sources		= "";
	types		= "";
	nst		= "";
	dmin		= "";
	rms		= "";
	gap		= "";
	magType		= "";
	type		= "";
	title		= "";
	#geometry	
	geoType		= "";
	coordinates	= [];
	id		= "";
		
	def __init__(self, earthquakeData):
		
		#jsonData = json.loads(earthquakeData);
		jsonData=earthquakeData
		
		#properties
		self.magnitude		= jsonData['properties']['mag'];
		self.place		= jsonData['properties']['place'];
		self.time		= jsonData['properties']['time']; 
		self.updated		= jsonData['properties']['updated'];
		self.tz			= jsonData['properties']['tz'];
		self.url		= jsonData['properties']['url'];
		self.detail		= jsonData['properties']['detail'];
		self.felt		= jsonData['properties']['felt'];
		self.cdi		= jsonData['properties']['cdi'];
		self.mmi		= jsonData['properties']['mmi'];
		self.alert		= jsonData['properties']['alert'];
		self.status		= jsonData['properties']['status'];
		self.tsunami		= jsonData['properties']['tsunami'];
		self.sig		= jsonData['properties']['sig'];
		self.net		= jsonData['properties']['net'];
		self.code		= jsonData['properties']['code'];
		self.ids		= jsonData['properties']['ids'];
		self.sources		= jsonData['properties']['sources'];
		self.types		= jsonData['properties']['types'];
		self.nst		= jsonData['properties']['nst'];
		self.dmin		= jsonData['properties']['dmin'];
		self.rms		= jsonData['properties']['rms'];
		self.gap		= jsonData['properties']['gap'];
		self.magType		= jsonData['properties']['magType'];
		self.type		= jsonData['properties']['type'];
		self.title		= jsonData['properties']['title'];
		#geometry	
		self.geoType		= jsonData['geometry']['type'];
		self.coordinates	= jsonData['geometry']['coordinates'];
		#id
		self.id			= jsonData['id'];


		#print("Created Earthquake:",self.id);
	
	def printQuake(self):
		print(colorz.scale(self.magnitude),"--->",self.title);
		#print("{0:25} {1:4} {2:64}".format(colorz.scale(self.magnitude),"--->",self.title));
		#print("   >",self.type);
		#print("   >",colorz.scale(self.magnitude));

