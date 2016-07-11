#!/usr/local/bin/python3

import requests 
import json, geojson
import pprint #Pretty Print
import datetime, time
import sys, signal
import curses
#User Defined Classes
from colorz import colorz
from earthquake import earthquake

def signal_handler(signal, frame):
	#Want to clean up CTRL+C action
	curses.reset_shell_mode();
	print("\nJust because of that, the big one is going to hit now...");
	sys.exit(0);
	
def run(scr,debug,dataSet):
	curses.start_color();
	curses.use_default_colors();
	#API Doc http://earthquake.usgs.gov/earthquakes/feed/v1.0/geojson.php
	url='';
	data='';
	if(dataSet == 'hour'):
		#All Hour
		url='http://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/all_hour.geojson';
	elif(dataSet == 'day'):
		#All Day
		url='http://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/all_day.geojson';
	elif(dataSet == 'week'):
		#All Week
		url='http://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/all_week.geojson';
	elif(dataSet == 'month'):
		#All Month
		url='http://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/all_month.geojson';
	curlCount=0;
	startTime = int(time.time());
	lastTime = 0;
	interval = 300;
	while(1):
		currTime=int(time.time());
		if((currTime - lastTime) > interval):
			r = requests.get(url);
			curlCount+=1;
			lastTime=int(time.time());
			data = r.json()
			count = 0;
			
			curses.update_lines_cols();
			screenSize=scr.getmaxyx();
			scr.resize(screenSize[0],screenSize[1]);
			maxQuakes=screenSize[0]-2;
			for quake in data['features']:
				eq = earthquake(quake)	
				eq.curseQuake(scr,count+1);
				count+=1;
				if(count >=maxQuakes):
					break;
			scr.addstr(count+1,50,"Curl Requests: "+str(curlCount));
			scr.addstr(count+1,0,"Last update: " + str(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')));
			scr.refresh();
			scr.erase();

#_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-
#Our Main Program

#Handle CTRL+C
signal.signal(signal.SIGINT, signal_handler);
#Program Arguments
if 'debug' in sys.argv:
	debug = True;
else:
	debug = False;
if '>' in sys.argv:
	minValue=0;
if '?' in sys.argv:
	print ("Parameters	Value");
	print ("debug		Displays debug data");
	print ("?		Displays this menu");
	exit();	

dataSet='day';

curses.wrapper(run,debug,dataSet);
