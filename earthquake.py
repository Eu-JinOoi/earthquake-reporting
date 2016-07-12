#!/usr/local/bin/python3
import http.client as httplib
import json, geojson
import datetime
import pymysql
import curses
from colorz import colorz

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
		self.alert		= jsonData['properties']['alert'];		#This field is typcially null
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

	def printQuake(self):
		if(self.magnitude!=None):
			print(
				colorz.scale(self.magnitude),
				datetime.datetime.fromtimestamp(int(str(self.time)[:-3])).strftime('%Y-%m-%d %H:%M:%S').ljust(20),
				self.formatType().ljust(5),
				self.tsunamiFormat().ljust(9),	
				self.title.ljust(128)
			);
	def curseQuake(self,scr,count):
		earthquake.registerColors();
		if(self.magnitude!=None):
			#Magnitude
			cp = self.magToColor();
			scr.addstr(count,0,"{:5}".format(str(self.magnitude)),curses.color_pair(cp));
			#Timestamp
			scr.addstr(count,6,datetime.datetime.fromtimestamp(int(str(self.time)[:-3])).strftime('%Y-%m-%d %H:%M:%S'))
			#Type
			if(self.type == 'earthquake'):
				scr.addstr(count,26,"EQ");
			elif(self.type == 'quarry blast'):
				scr.addstr(count,26,'QB', curses.color_pair(5));
			elif(self.type == 'explosion'):
				scr.addstr(count,26,'EX', curses.color_pair(5));
			else:
				scr.addstr(count,26,'UK', curses.color_pair(5));
			#Tsunami
			if(self.tsunami == 1):
				scr.addstr(count,29,"TSUNAMI",curses.color_pair(11) | curses.A_BLINK);
			else:
				scr.addstr(count,29,"~ ~ ~ ~");
			#Place
			scr.addstr(count,37,str(self.place));
	def registerColors():
		curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_GREEN);#0-3
		curses.init_pair(2, curses.COLOR_WHITE, curses.COLOR_YELLOW);#4-5
		curses.init_pair(3, curses.COLOR_WHITE, curses.COLOR_MAGENTA);#6-7
		curses.init_pair(4, curses.COLOR_WHITE, curses.COLOR_RED);#8-10
		curses.init_pair(5, curses.COLOR_YELLOW, curses.COLOR_BLACK);#8-10
		curses.init_pair(11, curses.COLOR_WHITE, curses.COLOR_RED);

	def magToColor(self):
		if(int(self.magnitude) < 3):
			return 1;
		elif(int(self.magnitude) < 6):
			return 2;
		elif(int(self.magnitude) < 8):
			return 3;
		else:
			return 4;

	def tsunamiFormat(self):
		if(self.tsunami != 0):
			return colorz.pretty("TSUNAMI","redWARN")
		else:
			return colorz.pretty("       ","default")
	def alertFormat(self):
		return colorz.pretty(self.alert,self.alert+"BG")
	def getMag(self):
		return float(self.magnitude);
	def isValidQuake(self):
		if(self.magnitude != None):
			return True;
		else:
			return False;
	def hasTsunami(self):
		if(self.tsunami != 0):
			return True;
		else:
			return False;
