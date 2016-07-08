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

def consoleLog(geoJsonData):
	print(geoJsonData['metadata']['count']);
def signal_handler(signal, frame):
	#Want to clean up CTRL+C action
	curses.reset_shell_mode();
	print();
	sys.exit(0);
def main():
	#Curses
	scr = curses.initscr();
	curses.start_color();
	#curses.noecho();
	#curses.cbreak();
	#scr.keypad(True);
	#scr.keypad(False);	
	#curses.echo();
	#curses.nocbreak;

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

#Should have args that select which feed to use. 
#API Doc http://earthquake.usgs.gov/earthquakes/feed/v1.0/geojson.php
#All Hour
#url='http://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/all_hour.geojson';
#All Day
url='http://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/all_day.geojson';
#All Week
#url='http://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/all_week.geojson';
#All Month
#url='http://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/all_month.geojson';

#Pretty Print
pp = pprint.PrettyPrinter(indent=4)

#main();
scr = curses.initscr();
while(1):
	r = requests.get(url);
	data = r.json()
	if(debug == True):
		#Pretty Print
		pp = pprint.PrettyPrinter(indent=4)
		pp.pprint(data);
	count = 0;
	
	curses.update_lines_cols();
	screenSize=scr.getmaxyx();
	scr.resize(screenSize[0],screenSize[1]);
	maxQuakes=screenSize[0]-1;

	for quake in data['features']:
		if(debug == True):
			print("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%");
			pp.pprint(quake);
		eq = earthquake(quake)	
		eq.curseQuake(scr,count);
		count+=1;
		if(count >=maxQuakes):
			break;
	scr.addstr(count,0,"Last update: " + str(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')));
	scr.refresh();
	scr.erase();
	#Time between steps
	time.sleep(60);

