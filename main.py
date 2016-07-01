#!/usr/local/bin/python3

import requests 
import json, geojson
import pprint #Pretty Print
import datetime, time
import sys
#User Defined Classes
from colorz import colorz
from earthquake import earthquake

def consoleLog(geoJsonData):
	print(geoJsonData['metadata']['count']);


#Should have args that select which feed to use. 
#API Doc http://earthquake.usgs.gov/earthquakes/feed/v1.0/geojson.php
#All Hour
url='http://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/all_hour.geojson';
#All Day
#url='http://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/all_day.geojson';
#All Week
#url='http://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/all_week.geojson';
#All Month
#url='http://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/all_month.geojson';

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
	count = 0;
	print("---------------------------------------------------------------------");
	for quake in data['features']:
		if(debug == True):
			pp.pprint(quake);
		eq = earthquake(quake)	
		eq.printQuake();
		count+=1;
	#	if(count>20):
	#		break;
	print("---------------------------------------------------------------------\n");
	#Time between steps
	time.sleep(360);
#	for i in range(0,24):
#		sys.stdout.write('\r');
	
