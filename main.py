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
from earthquakeList import earthquakeList #should probably merge this class into earthquake.

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

def scheduler(scr,args):
	#Setup the screen
	curses.start_color();
	curses.use_default_colors();	
	scr.nodelay(True);
	scr.keypad(1);
	#Timing Related Variables	
	interval=args.refresh;
	currTime=int(time.time());
	lastTime = 0;
	lastScreenRefresh = 0;
	#Debug Related Variables
	upCount=0;
	downCount=0;
	#Index Variables
	topIndex = 0;
	botIndex = 0;
	maxDisplyed = 0;

	quakeData=[];

	#Long Press Functionality
	pressLoops = 0;
	pressThreshold = 30;
	pressStep = 1; #Step Size
	pressStepFF = 2; #Fast Forward Speed
	pressNoPressLoops = 0;
	pressNoPressMax = 100;

	screenSize=scr.getmaxyx();
	while (True): # Main Loop
		currTime=int(time.time());
		#Fetch Data
		if((currTime - lastTime) > interval):
			lastTime=int(time.time());
			quakeData=fetchData(args,scr);
			#Populate the Quake List
			quakeList=earthquakeList(quakeData);	
			curses.beep();
	
		scr.move(0,0);
		scr.clrtoeol();
		scr.addstr(0,0,"Top Index:"+str(topIndex));
		scr.addstr(0,13,"Bot Index:"+str(botIndex));
		scr.addstr(0,26,"DOWN Arrow Pressed ("+str(downCount)+")");
		scr.addstr(0,53,"UP Arrow Pressed ("+str(upCount)+")");
		scr.addstr(0,77,"Screen Height:"+str(screenSize[0]));

		#Check on Screen Size
		curses.update_lines_cols();
		#if(currTime - lastScreenRefresh > 2):
		screenSize=scr.getmaxyx();
		scr.resize(screenSize[0],screenSize[1]);
		#botIndex=topIndex+(screenSize[0] if screenSize[0]<args.limit and args.limit>0 else args.limit)-2;
		botIndex=topIndex+screenSize[0];# -1 so that there is one row available at the bottom


		#Key Capture Behavior	
		keyPress = scr.getch();
		scr.addstr(0,0,str(curses.KEY_EOL));
		if(keyPress == curses.KEY_DOWN):
			pressLoops += 1;
			pressNoPressLoops = 0;
			if(pressLoops >= pressThreshold):
				pressStep = pressStepFF;
			scr.erase();
			downCount+=1;
			if(botIndex >= quakeList.events()):
				curses.beep();
			else:
				topIndex += pressStep;
				botIndex += pressStep;
		elif(keyPress == curses.KEY_UP):
			pressLoops += 1;
			pressNoPressLoops = 0;
			if(pressLoops >= pressThreshold):
				pressStep = pressStepFF;
			scr.erase();
			upCount+=1;
			if(topIndex<=1):#1 so that there is 1 row buffer at the top
				topIndex=0;	
				curses.beep();
			else:
				topIndex -= pressStep;
				botIndex -= pressStep;
		elif(keyPress == ord('t') or keyPress == ord('T')):
			topIndex = 0;
			botIndex=topIndex+screenSize[0];# -1 so that there is one row available at the bottom
		elif(keyPress == ord('q') or keyPress == ord('Q')):
			return;
		elif(keyPress == -1):
			pressNoPressLoops += 1;
			if(pressNoPressLoops > pressNoPressMax):
				pressLoops = 0;
				pressStep = 1;
		#This is to make sure that the speed step won't go out of bounds
		if(botIndex > quakeList.events()):
			temp = botIndex - quakeList.events();
			topIndex -= temp;
		#Print the quake list
		topIndex = quakeList.display(scr,args,topIndex,botIndex,screenSize[0]);
		scr.addstr(screenSize[0]-1,0,"Updated: " + str(datetime.datetime.fromtimestamp(lastTime).strftime('%Y-%m-%d %H:%M:%S')));
		scr.addstr(screenSize[0]-1,30,'Events: '+str(quakeList.events()));
		scr.addstr(screenSize[0]-1,45,"Press Loops:" + str(pressLoops));
		scr.addstr(screenSize[0]-1,62,"PressStep: "+ str(pressStep));
		#Refresh the Page
		scr.refresh();
	
def fetchData(args,scr): 
	#API Doc http://earthquake.usgs.gov/earthquakes/feed/v1.0/geojson.php
	url='';
	data='';
	#Process Arguments
	dataSet=args.range;
	if(dataSet == 'hour'): #All Hour
		url='http://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/all_hour.geojson';
	elif(dataSet == 'day'): #All Day
		url='http://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/all_day.geojson';
	elif(dataSet == 'week'): #All Week
		url='http://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/all_week.geojson';
	elif(dataSet == 'month'): #All Month
		url='http://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/all_month.geojson';
	else: #Set not specified or specified incorrectly
	 	return args.range;
	#curlCount=0;
	#connectionRetries=0;
	#requestSize=0;
	try:
		r = requests.get(url);
	#	connectionRetries=0;
		#requestSize+=int(len(r.content));
	#	curlCount+=1;
		data = r.json()
	#	scr.addstr(4,0,"Received "+str(len(data))+" records from USGS.");
		return data;
	except:
		scr.addstr(4,0,"Connection to USGS failed.");
	#	connectionRetries+=1;

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
curses.wrapper(scheduler,args);

