#!/usr/local/bin/python3
import curses;
import time;
import math;
#Custom Classes
from earthquake import earthquake;

class earthquakeList:
	quakeArray = [];	
	idArray = [];
	invalid = True;
	def __init__(self,quakeJSON):
		if (quakeJSON == None):
			self.invalid = True;
			return;
		self.invalid = False;
		if(self.quakeArray == []):
			for quake in quakeJSON['features']:
				eq = earthquake(quake);
				self.quakeArray.append(eq);
				self.idArray.append(eq.getId());
		else:
			for quake in quakeJSON['features']:
				eq = earthquake(quake);
				if((eq.getId() in self.idArray) == False):
					self.quakeArray.insert(0,eq);	
					self.idArray.append(eq.getId());

	def events(self):
		return len(self.quakeArray);

	def display(self,scr,args,topIndex,botIndex,windowHeight):
		if(self.invalid):
			scr.addstr(1,0,"Quake Data is Invalid");
			scr.addstr(2,0,"Records:"+str(len(self.quakeArray)));
			return;
		#Argument Limit
		limit=args.limit;
		if(limit <= 0):
			limit = math.inf;
		minMag = args.minmag;
		maxQuakes = windowHeight-2;	
		count = 0
		if(botIndex>=len(self.quakeArray)):
			botIndex=len(self.quakeArray);
		for i in range(topIndex, botIndex+2):
			if(self.quakeArray[i].isValidQuake() and self.quakeArray[i].getMag() > minMag and (args.tsunami == True and self.quakeArray[i].hasTsunami() == True or args.tsunami == False)):
				self.quakeArray[i].curseQuake(scr,count+1);
				count+=1;
			if(count >=maxQuakes or count>=limit):
				break;

		
			
