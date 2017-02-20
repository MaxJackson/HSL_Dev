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
#print(dirname)
channels_to_convert = [61, 53, 52, 41, 44, 54, 51, 42, 43, 31]

output_dir = cwd = os.getcwd() + "\\Output\\"

if not os.path.exists(output_dir):
	os.makedirs(output_dir)

	
output_file = dirname.split("/")[-1] + "_datatool_script"
bat_file = dirname.split("/")[-1] + "_datatool_script_bat"
i = 1
if os.path.isfile(output_file + ".txt"):
	while os.path.isfile(output_file + "_" + str(i) + ".txt"):
		i += 1
	output_file = output_file + "_" + str(i) + ".txt"
	bat_file = bat_file + "_" + str(i) + ".bat"
else: 
	output_file = output_file + ".txt"
	bat_file = bat_file + ".bat"
	
with open(bat_file, 'w') as f:
	f.write("MC_Datatool -file " + output_file + " -ascii")
	print(bat_file)

	
with open(output_file, 'w') as f:
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
