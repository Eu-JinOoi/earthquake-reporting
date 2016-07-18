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

	#Arg Stuff
	tsunami = False;
	limit = math.inf;


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

	def events(self):
		return len(self.quakeArray);
	def parseArgs(self, args):
		if(args.tsunami == True):
			this.tsunami = True;
		if(args.limit > 0):
			this.limit = args.limit;
			
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
		positionIndex = topIndex
		if(botIndex>=len(self.quakeArray)):
			botIndex=len(self.quakeArray);
		scr.addstr(21,0,"Events: "+ str(self.events()));
		firstRelevant = -1;
		while(True):
			#if(count >= args.limit or count >= maxQuakes or positionIndex >= self.events()):
			if(count >= maxQuakes or positionIndex >= self.events()):
			#	scr.addstr(20,0,"Breaking on count = "+str(count)+" and positionIndex "+str(positionIndex));
				break;
			if(self.quakeArray[positionIndex].isValidQuake() 
				and self.quakeArray[positionIndex].getMag() > minMag 
				and (args.tsunami == True and self.quakeArray[positionIndex].hasTsunami() == True or args.tsunami == False)
			):
				if(firstRelevant < 0):
					firstRelevant = positionIndex;
				self.quakeArray[positionIndex].curseQuake(scr,count+1);
				count += 1;
			positionIndex += 1;

		#for i in range(topIndex, botIndex+2):
		#	if(self.quakeArray[i].isValidQuake() and self.quakeArray[i].getMag() > minMag and (args.tsunami == True and self.quakeArray[i].hasTsunami() == True or args.tsunami == False)):
		#		self.quakeArray[i].curseQuake(scr,count+1);
		#		count+=1;
		#	if(count >=maxQuakes or count>=limit):
		#		break;

		#This will return the index of the first relevant entry. 
		#This should help with scrolling through event when a filter is applied. 	
		return firstRelevant;
			
