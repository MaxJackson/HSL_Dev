"""
This script generates conversion text files for MC_Datatool
"""
print("Importing Libraries...\n")
import os

from hsl_lib.MCS_Functions import get_dirname



def generate_conversion_script(conversion_script_path, data_output_dir, script_output_dir, filename, file_path, channels_to_convert, bat_file):
	print(file_path)
	
	i = 1
	if os.path.isfile(conversion_script_path + ".txt"):
		while os.path.isfile(conversion_script_path + "_" + str(i) + ".txt"):
			i += 1
		conversion_script_path = conversion_script_path + "_" + str(i) + ".txt"
	else: 
		conversion_script_path = conversion_script_path + ".txt"

	with open(conversion_script_path, 'w') as f:
		writeline = "-i \"" + file_path + "\"\n"
		f.write(writeline)
		data_outfile = data_output_dir + "_".join("_".join(file_path.split(":")[-1][:-4].split("/")).split("\\")) + ".txt"
		writeline = "-o \"" + data_outfile + "\"\n"
		f.write(writeline)
		f.write("\n")	
		
		for channel in channels_to_convert:
			writeline = "-s \"Electrode Raw Data:" + str(channel) + "\"\n"
			f.write(writeline)

		writeline = "-s \"Analog Raw Data:A1" + "\"\n"
		f.write(writeline)

		writeline = "-ToUnsigned"
		f.write(writeline)
	with open(bat_file, 'a') as b:
		#print(bat_file)
		
		b.write("\nMC_Datatool -file \"" + conversion_script_path + "\" -bin -WriteHeader\n")


def main():
	dirname = get_dirname()
	dirs = [x[0] for x in os.walk(dirname)]
	#print(dirname)
	channels_to_convert = [61, 53, 52, 41, 44, 54, 51, 42, 43, 31]

	#output_dir = os.getcwd() + "\\Output\\"
	data_output_dir = "/".join(os.getcwd().split("\\")) + "/MC_DataTool_Output/"
	script_output_dir = "/".join(os.getcwd().split("\\")) + "/MC_DataTool_Scripts/"

	if not os.path.exists(data_output_dir):
		os.makedirs(data_output_dir)

	if not os.path.exists(script_output_dir):
		os.makedirs(script_output_dir)

		
	#output_file = dirname.split("/")[-1] + "_datatool_script"
	bat_file = dirname.split("/")[-1] + "_datatool_script_bat"
	i = 1
	if os.path.isfile(bat_file + ".bat"):
		while os.path.isfile(bat_file + "_" + str(i) + ".bat"):
			i += 1
		bat_file = bat_file + "_" + str(i) + ".bat"
	else: 
		bat_file = bat_file + ".bat"	



	for dir in dirs:
		for filename in os.listdir(dir):
			if filename.endswith(".mcd"):
				conversion_script_path = script_output_dir + filename.split(".")[0] + "_datatool_script"
				file_path = dir + "\\" + filename
				generate_conversion_script(conversion_script_path, data_output_dir, script_output_dir, filename, file_path, channels_to_convert, bat_file)
				
					
	with open(bat_file, 'a') as b:
		b.write("\npause\n")

if __name__ == "__main__":
	main()