#!/usr/local/bin/python3

import requests 
import json, geojson
import pprint #Pretty Print
import datetime, time
import sys, signal
import curses
import argparse
import math
import re #regex
#User Defined Classes
from earthquake import earthquake

def signal_handler(signal, frame):
	#Want to clean up CTRL+C action
	curses.reset_shell_mode();
	print("\nJust because of that, the big one is going to hit now...");
	sys.exit(0);
	
def checkEmail(value):
	match = re.match('^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})$', value)	
	if ( match == None):
		raise argparse.ArgumentTypeError("Invalid e-mail format");
	return value;
def check_limit_value(value):
	if(int(value)<0):
		raise argparse.ArgumentTypeError("You must enter a positive number for the limit. Entering 0 is the same as not specifying an argument.");
	return int(value);
def checkMag(value):
	if(float(value)<0 or float(value)>10):
		raise argparse.ArgumentTypeError("You have specified a magnitude that is out of range. Your value should be between 0.0 and 10.0");
	return float(value);
def formatSize(size,unitPos):
	types=['bytes','KB','MB','GB','TB','PB'];
	if(size<1024):
		return (int(size),str(types[unitPos]));
	else:
		size=size/1024;	
		retSize,type=formatSize(size,unitPos+1);
		return (retSize,type);
def printScreen(scr,quakes,start,stop):
	for i in range(start,stop):
		quake = quakes[i];
		if(quake.isValidQuake() and quake.getMag() > minMag and (args.tsunami == True and quake.hasTsunami() == True or args.tsunami == False)):
			quakeArray.append(eq.curseQuake(scr,count+1));
			count+=1;
			if(count >=maxQuakes or count>=limit):
				break;
	return	
def run(scr,args):
	curses.start_color();
	curses.use_default_colors();
	#API Doc http://earthquake.usgs.gov/earthquakes/feed/v1.0/geojson.php
	url='';
	data='';
	#Process Arguments
	dataSet=args.range;

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
	else:
		#Set not specified
		return args.range;
	#Argument - limit
	limit=args.limit
	if(limit <= 0):
		limit = math.inf;
	curlCount=0;
	requestSize=0;
	startTime = int(time.time());
	lastTime = 0;
	interval = args.refresh;
	minMag = float(args.minmag);
	connectionRetries=0;
	quakeArray=[];
	while(1):
		currTime=int(time.time());
		if((currTime - lastTime) > interval):
			try:
				r = requests.get(url);
				connectionRetries=0;
				requestSize+=int(len(r.content));
				curlCount+=1;
				lastTime=int(time.time());
				data = r.json()
				count = 0;
				
				curses.update_lines_cols();
				screenSize=scr.getmaxyx();
				scr.resize(screenSize[0],screenSize[1]);
				maxQuakes=screenSize[0]-2;
				#Build the Earthquake List
				for quake in data['features']:
					eq = earthquake(quake)	
					quakeArray.append(eq);
				#for quake in 
					if(eq.isValidQuake() and eq.getMag() > minMag and (args.tsunami == True and eq.hasTsunami() == True or args.tsunami == False)):
						quakeArray.append(eq.curseQuake(scr,count+1));
						count+=1;
						if(count >=maxQuakes or count>=limit):
							break;
				scr.addstr(count+1,0,"Updated: " + str(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')));
				scr.addstr(count+1,29,"Requests: "+str(curlCount));
				totalSize, sizeType=formatSize(requestSize,0);
				scr.addstr(count+1,45,"Data: "+str(totalSize)+" "+sizeType);
			except:
				lastTime=0;
				connectionRetries+=1;
				scr.addstr(0,0,"Unable to establish a connection... ");
				scr.addstr(1,0,"Reconnecting. Attempt "+str(connectionRetries)+". ");
				time.sleep(5);
				
			scr.refresh();
			scr.erase();
			time.sleep(0.5);

#_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-
#Our Main Program

#Handle CTRL+C
signal.signal(signal.SIGINT, signal_handler);
#Process Arguments
parser = argparse.ArgumentParser(description = "Earthquake Data Parameter Parser");
parser.add_argument('--range', choices = ['hour','day','week','month'], default = "day");
parser.add_argument('--limit', type = check_limit_value, default=-1);
parser.add_argument('--refresh', type = check_limit_value, default=300);
parser.add_argument('--minmag', type=checkMag, default=0);
parser.add_argument('--tsunami', action = 'store_true');
parser.add_argument('--mailto', type = checkEmail);
args=parser.parse_args();
#print(args);
#exit();

curses.wrapper(run,args);

