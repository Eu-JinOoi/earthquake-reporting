#!/usr/local/bin/python3

import requests 
import json, geojson
import pprint #Pretty Print
import datetime, time
#User Defined Classes
import colorz

def consoleLog(geoJsonData):
	print(geoJsonData['metadata']['count']);


#Should have args that select which feed to use. 
#API Doc http://earthquake.usgs.gov/earthquakes/feed/v1.0/geojson.php
#All Hour
url='http://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/all_hour.geojson';
#All Day
#url='http://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/all_day.geojson';
#r = requests.get(url);
#data = r.json()


#Pretty Print
#pp = pprint.PrettyPrinter(indent=4)
#pp.pprint(data);

debug = False;

while(1):
	r = requests.get(url);
	data = r.json()
	if(debug == True):
		#Pretty Print
		pp = pprint.PrettyPrinter(indent=4)
		pp.pprint(data);
	consoleLog(data);	
	time.sleep(5);
	
