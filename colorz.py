#!/usr/local/bin/python3

#COLOR GUIDE -  http://misc.flogisoft.com/bash/tip_colors_and_formatting

#COLOR DEFINITION
class colorz:
	HEADER = '\033[95m'
	OKBLUE = '\033[94m'
	OKGREEN = '\033[92m'
	WARNING = '\033[93m'
	FAIL = '\033[91m'
	ENDC = '\033[0m'
	BOLD = '\033[1m'
	UNDERLINE = '\033[4m'
	DEFAULT = '\033[39;49m';

	#Scale Background Colors
	#\EscapeCharacter[TextFormat; Text Color; background Color m
	scaleB = [
	'\033[97;40m', 			#0
	'\033[97;100m',			#1
	'\033[30;47m',			#2
	'\033[90;107m',			#3
	'\033[37;104m',			#4
	'\033[1;97;43m',		#5
	'\033[1;90;103m',		#6
	'\033[1;5;97;45m',		#7
	'\033[1;5;97;105m',		#8
	'\033[1;5;97;41m',		#9
	'\033[1;5;97;101m'		#10
	];
	
	
	def pretty(text,color):
		if(color=='red'):
			return colorz.BOLD+colorz.FAIL+text+colorz.ENDC
		elif(color=='redWARN'):
			return '\033[1;5;93;101m'+text+colorz.ENDC
		elif (color=='green'):
			return colorz.OKGREEN + text + colorz.ENDC;
		elif (color=='yellow'):
			return colorz.WARNING + text + colorz.ENDC;
		
		elif (color=='redBG'):
			return '\033[1;101m'+text + colorz.ENDC;
		elif (color=='orangeBG'):
			return '\033[1;101m'+text + colorz.ENDC;
		elif (color=='yellowBG'):
			return '\033[1;101m'+text + colorz.ENDC;
		elif (color=='greenBG'):
			return '\033[1;101m'+text + colorz.ENDC;
		else:
			return colorz.DEFAULT + text + colorz.ENDC;


	def scale(numericValue):
		val=int(numericValue)
		return colorz.scaleB[val]+str(numericValue).ljust(5)+colorz.ENDC;
#for i in range(0,11):
#	print(colorz.scale(i));
#for i in range(21,108):
#	if( i <48 or i>89):
#		print ('\033[1;'+str(i)+'m'+str(i)+colorz.ENDC);
