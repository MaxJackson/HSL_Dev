"""
This script generates full MEA plots of all spikes and 3D PCA spike feature plots
"""


# Import Libraries
import matplotlib.pyplot as plt 
import numpy as np
import os
import math
import traceback
from matplotlib.mlab import PCA as mlabPCA
from mpl_toolkits.mplot3d import Axes3D
from hsl_lib.MCS_Objects import MCS_Spike, MCS_Data_Channel
from hsl_lib.MCS_Functions import plot_mea_waveforms, get_spike_feature_pca, plot_spike_feature_pca, get_data_txt, get_filename, get_filenames, log_error


def main():


	#full_file_path = get_filename()

	filenames = get_filenames

	for full_file_path in filenames:
		
		try:
			pca_image_output_folder = full_file_path.split('.')[0] + '/PCA_images/'
			if not os.path.exists(pca_image_output_folder):
				os.makedirs(pca_image_output_folder)
			channels_to_read = range(0, 100)

			all_channels, analog_channels, sampling_rate = get_data_txt(full_file_path, channels_to_read)

			print("Generating full-MEA waveform plots")
			plot_mea_waveforms(all_channels, full_file_path)

			print("Generating spike feature PCA plots")
			for channel in all_channels:
				if len(channel.all_spikes) > 3:
					
					pca_plot_filename = pca_image_output_folder + full_file_path.split('/')[-1].split('.')[0] + '_pca_' + str(channel.channel_number)
					print("Generating " + pca_plot_filename)
					spike_feature_pca = get_spike_feature_pca(channel)
					plot_spike_feature_pca(spike_feature_pca, channel.channel_number, pca_plot_filename)

		except:
			e = traceback.format_exc()
			log_error(full_file_path, e)


		

	print('Done!')



# Main Function
if __name__ == "__main__":

	main()
	
	