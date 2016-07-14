#!/usr/local/bin/python3
import curses;
import time;
#Custom Classes
import earthquake;

class earthquakeList:
	quakeArray = [];	
	def __init__(quakeJSON):
		for quake in quakeJSON['features']:
                        eq = earthquake(quake)
                        quakeArray.append(eq);
	def print(args,topIndex,botIndex,maxQuakes):
		limit=args.limit;
		maxQuakes=	
		for i in range(topIndex, botIndex,1):
			if(quakeArray[i].isValidQuake() and quakeArray[i].getMag() > minMag and (args.tsunami == True and quakeArray[i].hasTsunami() == True or args.tsunami == False)):
				quakeArray[i].curseQuake(scr,count+1);
				count+=1;
				if(count >=maxQuakes or count>=limit):
					break;

		
			
