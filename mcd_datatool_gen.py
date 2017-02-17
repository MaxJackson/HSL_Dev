"""
This script generates conversion text files for MC_Datatool
"""

import os
from Tkinter import Tk
from tkFileDialog import askdirectory

def get_dirname():
	Tk().withdraw()
	print("Initializing Dialogue...\nPlease select a directory.")
	dirname = askdirectory(initialdir=os.getcwd(),title='Please select a directory')
	if len(dirname) > 0:
		print ("You chose %s" % dirname)
		return dirname
	else: 
		dirname = os.getcwd()
		print ("\nNo directory selected - initializing with %s \n" % os.getcwd())
		return dirname


dirname = get_dirname()
dirs = [x[0] for x in os.walk(dirname)]
channels_to_convert = [61, 53, 52, 41, 44, 54, 51, 42, 43, 31]

output_dir = cwd = os.getcwd() + "\\Output\\"

if not os.path.exists(output_dir):
	os.makedirs(output_dir)

with open('test.txt', 'w') as f:
	for dir in dirs:
		for filename in os.listdir(dir):
			if filename.endswith(".mcd"):
				writeline = "-i \"" + dir + "\\" + filename + "\"\n"
				print(dir + "\\" + filename)
				f.write(writeline)
				#outfile = filename.split('.')[0] + ".txt"
				#writeline = "-o \"" + outfile + "\"\n"
				#f.write(writeline)
				
	f.write("-o \"" + output_dir + "\"\n")			
	f.write("\n")	
	
	for channel in channels_to_convert:
		writeline = "-s \"Electrode Raw Data:" + str(channel) + "\"\n"
		f.write(writeline)
