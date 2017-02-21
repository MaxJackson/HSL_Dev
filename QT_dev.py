"""
This script analyzes the conduction velocity within a user-specified region between user-specified channels.
"""


print("Importing Libraries...\n")
import os, time, math, sys
import matplotlib.pyplot as plt 
import numpy as np
from hsl_lib.MCS_Objects import QT_Region_Selector
from hsl_lib.MCS_Functions import get_data_txt, plot_mea_waveforms, plot_cmea_waveforms, get_channels_to_compare, get_spike_time_differences, get_channels_to_analyze, get_filename




def main():
	full_file_path = get_filename()

	cmea_electrodes = [61, 53, 52, 41, 44, 54, 51, 42, 43, 31]
	cmea_distances = [0.001 * x for x in range(0, len(cmea_electrodes))] # Electrodes are 1mm apart

	cmea_positions = []

	channels_to_read = cmea_electrodes
	all_channels, analog_channels, sampling_rate = get_data_txt(full_file_path, channels_to_read)

	# print(len(analog_channels))
	# plt.plot(analog_channels[0].voltage_data)
	# plt.show()
	# a = raw_input(" ")

	# print("Generating full-MEA waveform plots")
	# plot_mea_waveforms(all_channels, full_file_path)


	plot_cmea_waveforms(all_channels, full_file_path)

	print("Please enter the channels you would like to analyze")
	channels_to_analyze_input = [int(x) for x in raw_input("---->>>> ").split()]
	channels_to_analyze = get_channels_to_analyze(all_channels, channels_to_analyze_input)

	for channel in channels_to_analyze:
		region_selector = QT_Region_Selector(channel)
		qt_start_point, qt_end_point = region_selector.qt_start_point, region_selector.qt_end_point
		qt_interval = (qt_end_point - qt_start_point) * (1000/sampling_rate)
		print("Channel Average QT Interval: " + str(qt_interval)) + " ms"

if __name__ == "__main__":
	main()