from __future__ import print_function
import os, time, threading
import numpy as np

#import neuroshare as ns
import matplotlib.pyplot as plt
from numpy import fromfile
from Tkinter import Tk
from matplotlib.mlab import PCA as mlabPCA
from mpl_toolkits.mplot3d import Axes3D
from tkFileDialog import askdirectory, askopenfilename, askopenfilenames
from MCS_Objects import MCS_Data_Channel, MCS_Analog_Channel, MCS_Spike, MCS_Preprocessed_Channel




def log_error(file, error):
    error_dir = os.getcwd() + "/error_log/"
    if not os.path.exists(error_dir):
        os.makedirs(error_dir)
    date_time = time.strftime("%d-%m-%Y") + "_" + time.strftime("%H-%M-%S")
    error_file = error_dir + "error_log_" + date_time + ".txt"

    print("Error processing file at:\n" + file + "\nWriting to " + error_file + "\n")
    with open(error_file, 'ab+') as e:
        print(error)
        e.write(error)
        e.write('\n')

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

def get_filenames():
    Tk().withdraw()
    print("Initializing Dialogue... \nPlease select a file.")
    tk_filenames = askopenfilenames(initialdir=os.getcwd(), title='Please select one or more files')
    filenames = list(tk_filenames)
    return filenames


def get_filename():
    Tk().withdraw()
    print("Initializing Dialogue... \nPlease select a file.")
    filename = askopenfilename(initialdir=os.getcwd(),title='Please select a file')
    print("You chose " + filename)
    return filename 
    

def is_int(i):
    try: 
        int(i)
        return True
    except ValueError:
        return False


def get_data(full_file_path, channels_to_read):
    ext = full_file_path.split(".")[-1]
    if ext == "txt":
        all_channels, analog_channels, sampling_rate = get_data_txt(full_file_path, channels_to_read)
    elif ext == "raw":
        all_channels, analog_channels, sampling_rate = get_data_raw(full_file_path, channels_to_read)
    else:
        print('Invalid File!\n ' + full_file_path)
        return [], [], 0.0

    return all_channels, analog_channels, sampling_rate


def process_channel(channel_array, pre_processed_channel):
    c = pre_processed_channel
    #print("processing " + str(c.channel_name))
    channel_array.append(MCS_Data_Channel(c.voltage_data, c.time_data, c.channel_name, c.sampling_rate))
    #print("finished " + str(c.channel_name))

def get_data_raw(full_file_path, channels_to_read):
    """
        This function extracts the data from a MC_DataTool-converted txt file 
        input:
            full_file_path(string)
            channels_to_read([int])
        output:
            all_channels(MCS_Data_Channel)
            analog_channels([MCS_Analog_Channels])
            sampling_rate(float)
    """
    print("Importing data from " + full_file_path)
    with open(full_file_path, 'rb') as f: 
        f.readline()
        f.readline()
        f.readline()
        sampling_rate = float(f.readline()[14:-2])
        print('Sampling rate: ' + str(sampling_rate))
        ADC_zero = float(f.readline()[11:-2])
        print('Offset: ' + str(ADC_zero))
        El = float(f.readline()[5:11])
        print('Scaling: ' + str(El))
        channel_names = f.readline()[10:].split(';')
        print(str(len(channel_names))+' channels')
        channel_names[-1] = channel_names[-1][:-2]
        f.readline()

        data = fromfile(f, dtype='uint16')
        data = data.reshape((len(channel_names),-1), order='F').astype('float')

        for i in range(len(channel_names)):
            if channel_names[i].startswith('El'):
                data[i] = (data[i]-ADC_zero)*El

    all_channels = []
    pre_processed_channels = []
    analog_channels = []
    time_data = [float(x)*1.0/sampling_rate for x in range(len(data[0]))]
    for i in range(len(channel_names)):
        if channel_names[i].startswith('A'):
            mcs_analog_channel = MCS_Analog_Channel(data[i], time_data, int(channel_names[i][-1]))
            analog_channels.append(mcs_analog_channel)
        else:
            if(int(channel_names[i][-2:]) in channels_to_read):
                pre_processed_channel = MCS_Preprocessed_Channel(data[i], time_data, int(channel_names[i][-2:]), sampling_rate)
                pre_processed_channels.append(pre_processed_channel)

    #print("Processing channels...")
    for c in pre_processed_channels:
        t = threading.Thread(target=process_channel, args = (all_channels, c))
        t.daemon = True
        t.start()     

    #print(len(all_channels))
    return all_channels, analog_channels, sampling_rate


def get_data_txt(full_file_path, channels_to_read):
    """
        This function extracts the data from a MC_DataTool-converted txt file 
        input:
            full_file_path(string)
            channels_to_read([int])
        output:
            all_channels(MCS_Data_Channel)
            analog_channels([MCS_Analog_Channels])
            sampling_rate(float)
    """
    print("Processing " + full_file_path)
    with open(full_file_path, 'r') as f:
        lines = f.readlines()

        channel_line = lines[2]
        channel_numbers = [int(x) for x in channel_line.split() if is_int(x)]
        analog_channel_numbers = [x for x in channel_line.split() if x.startswith('A') and is_int(x[-1])]
        all_channels = []
        analog_channels = []
        sampling_rate = 1000.0 / (float(lines[5].split()[0]) - float(lines[4].split()[0]))
        time_data = []


        all_channel_data = []
        pre_processed_channels = []
        analog_channel_data = []
        for i in range(0, len(channel_numbers)):
            all_channel_data.append([])
        for line in lines[4:]:
            time_data.append(float(line.split()[0]))
            analog_channel_data.append(float(line.split()[-1]))
            data_line = line.split()[1:]
            for i in range(0, len(channel_numbers)):
                if channel_numbers[i] in channels_to_read:
                    all_channel_data[i].append(float(data_line[i]))
        for i in range(0, len(channel_numbers)):
            if all_channel_data[i]:
                pre_processed_channel = MCS_Preprocessed_Channel(all_channel_data[i], time_data, int(channel_numbers[i]), sampling_rate)
                pre_processed_channels.append(pre_processed_channel)

        if analog_channel_numbers:
            mcs_analog_channel = MCS_Analog_Channel(analog_channel_data, time_data, analog_channel_numbers[0])
            analog_channels.append(mcs_analog_channel)

        

    for c in pre_processed_channels:
        t = threading.Thread(target=process_channel, args = (all_channels, c))
        t.daemon = True
        t.start()

    return all_channels, analog_channels, sampling_rate
    
    
### REMOVED PENDING NEUROSHARE INTEGRATION  
# def get_data_mcd(full_file_path, channels_to_read):
    # """
        # This function extracts the data from a given .mcd file.
        # input:
            # full_file_path(string), channels_to_read([int])
        # output:
            # all_channels([MCS_Data_Channel])
            # analog_channels([MCS_Analog_Channels])
            # sampling_rate(float)
    # """

    # print ("Processing " + full_file_path) 
    # fd = ns.File(full_file_path)
    # sampling_rate = (1.0/fd.time_stamp_resolution)
    # print("Sampling Rate: " + str(sampling_rate))
    # counter = len(fd.entities)
    # all_channels = []
    # analog_channels = []

    # for i in range(0, counter):
        # analog1 = fd.entities[i] #open channel 
        # if analog1.entity_type == 2:
            # channel = analog1.label[-2:] #identify channel 
           # print(channel)
            # if channel.startswith('A'):
                # data, taimes, count = analog1.get_data()
                # print(channel)
                # analog_channel = MCS_Analog_Channel(data, times)
                # analog_channels.append(analog_channel)

            # if not channel.startswith('A') and int(channel) in channels_to_read: #if it is not an analog channel and if the channel is in the range of channels in the pattern
                # data, times, count = analog1.get_data() #load data

                # data2 = [d + data[0] for d in data]
                # print(channel)
        
                # mcs_data_channel = MCS_Data_Channel(data2, times, channel, sampling_rate)
                # if len(mcs_data_channel.all_spikes) > 0:
                    # all_channels.append(mcs_data_channel)
    # return all_channels, analog_channels, sampling_rate

def get_spike_feature_pca(channel):
    pca_matrix = []
    for spike in channel.all_spikes:
        row = []
        row.append(spike.spike_max)
        row.append(spike.spike_positive_slope)
        row.append(spike.spike_half_peak_width_negative)
        pca_matrix.append(row)
    pca_matrix = np.array(pca_matrix)
    #print(len(pca_matrix))
    #print(len(pca_matrix[0]))
    spike_feature_pca = mlabPCA(pca_matrix)

    return spike_feature_pca

def plot_spike_feature_pca(spike_feature_pca, channel_number, pca_plot_filename):
        
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.scatter(spike_feature_pca.Y[:,0], spike_feature_pca.Y[:,1], spike_feature_pca.Y[:,2], c='b', marker='o')

    ax.set_xlabel("Spike Height")
    ax.set_ylabel("Spike Positive Slope")
    ax.set_zlabel("Spike Half Peak Width")
    
    ax.set_xlim(-4, 4)
    ax.set_ylim(-4, 4)
    ax.set_zlim(-4, 4)

    plt.legend()
    plt.title(str(channel_number))
    plt.savefig(pca_plot_filename)
    plt.close()

def plot_mea_waveforms(channels, input_file):
    """
    This function plots all of the average waveform for a standard MEA.

    input:
        channels([MCS_Data_Channel])
        input_file(string)
    """
    f, axarr = plt.subplots(8, 8, squeeze=True)
    plt.subplots_adjust(hspace=0.001)
    plt.subplots_adjust(wspace=0.001)

    y_max = 0.0
    y_min = 0.0
    for channel in channels:
        if max(channel.average_waveform) > y_max:
            y_max = max(channel.average_waveform)
        if min(channel.average_waveform) < y_min:
            y_min = min(channel.average_waveform)

    y_max = y_max*1.1
    y_min = y_min*1.1
    for i in range(0, len(channels)):
        this_channel = channels[i]
        rawFlag = 0
        if rawFlag == 0:
            ypos = np.floor(this_channel.channel_number/10) - 1
            xpos = (this_channel.channel_number % 10) - 1
        if rawFlag == 1:
            xpos = np.floor(this_channel.channel_number/10) - 1
            ypos = (this_channel.channel_number % 10) - 1
        Xs = range(0, len(this_channel.average_waveform))
        axarr[xpos, ypos].plot(this_channel.average_waveform)
        axarr[xpos, ypos].errorbar(Xs, this_channel.average_waveform, this_channel.std_waveform, linestyle='None', capsize=0, capthick=0)
        

        axarr[xpos, ypos].axis([0, len(this_channel.average_waveform), y_min, y_max])
        
        axarr[xpos, ypos].text(len(this_channel.average_waveform)*0.7, y_min*0.7, this_channel.channel_number,  fontsize='small')
        #axarr[xpos, ypos].text(150, axMin+10, round((activeChannelCounts[i]/recordingTime),2), fontsize='small')
        plt.tick_params(axis='x', which='both', bottom='off', top='off', labelbottom='off') 
        plt.tick_params(axis='y', which='both', left='off', right='off', labelbottom='off') 

    axarr[0,0].set_frame_on(False)
    axarr[0,7].set_frame_on(False)
    axarr[7,0].set_frame_on(False)
    axarr[7,7].set_frame_on(False)
    
    for i in range(0,8):
        plt.setp([a.get_xticklabels() for a in axarr[i, :]], visible=False)
        plt.setp([a.get_yticklabels() for a in axarr[:, i]], visible=False)
        plt.setp([a.tick_params(axis='x', which='both', bottom='off', top='off', labelbottom='off') for a in axarr[:,i]])
        plt.setp([a.tick_params(axis='y', which='both', left='off', right='off', labelbottom='off') for a in axarr[:,i]])
    
    full_mea_plot_image_file = input_file.split('.')[0] + '_mea_plot_2.png'

    f.suptitle(input_file)
    f.savefig(full_mea_plot_image_file)
    plt.show(block=False)


def plot_cmea_waveforms(channels, input_file):
    """
    This function plots all of the average waveforms for a cMEA.

    input:
        channels([MCS_Data_Channel])
        input_file(string)
    """
    print("Generating cMEA waveform plots")

    channel_order = [61, 53, 52, 41, 44, 54, 51, 42, 43, 31]
    positions = [[0, 0], [0, 1], [0, 2], [0, 3], [0, 4], [1, 0], [1, 1], [1, 2], [1, 3], [1, 4]]
    f, axarr = plt.subplots(2, 5, squeeze=True)
    plt.subplots_adjust(hspace=0.001)
    plt.subplots_adjust(wspace=0.001)

    y_max = 0.0
    y_min = 0.0
    for channel in channels:
        if max(channel.average_waveform) > y_max:
            y_max = max(channel.average_waveform)
        if min(channel.average_waveform) < y_min:
            y_min = min(channel.average_waveform)

    y_max = y_max*1.1
    y_min = y_min*1.1
    for i in range(0, len(channels)):
        this_channel = channels[i]
        rawFlag = 0
        for j in range(0, len(channel_order)):
            if int(this_channel.channel_number) == channel_order[j]:
                xpos, ypos = positions[j]
        Xs = range(0, len(this_channel.average_waveform))
        axarr[xpos, ypos].plot(this_channel.average_waveform)
        axarr[xpos, ypos].errorbar(Xs, this_channel.average_waveform, this_channel.std_waveform, linestyle='None', capsize=0, capthick=0)
        

        axarr[xpos, ypos].axis([0, len(this_channel.average_waveform), y_min, y_max])
        
        axarr[xpos, ypos].text(len(this_channel.average_waveform)*0.7, y_min*0.7, this_channel.channel_number,  fontsize='small')
        #axarr[xpos, ypos].text(150, axMin+10, round((activeChannelCounts[i]/recordingTime),2), fontsize='small')
        plt.tick_params(axis='x', which='both', bottom='off', top='off', labelbottom='off') 
        plt.tick_params(axis='y', which='both', left='off', right='off', labelbottom='off') 

    
    for i in range(0, 2):
        plt.setp([a.get_xticklabels() for a in axarr[i, :]], visible=False)
    for i in range(0, 5):
        plt.setp([a.get_yticklabels() for a in axarr[:, i]], visible=False)
        plt.setp([a.tick_params(axis='x', which='both', bottom='off', top='off', labelbottom='off') for a in axarr[:,i]])
        plt.setp([a.tick_params(axis='y', which='both', left='off', right='off', labelbottom='off') for a in axarr[:,i]])
    
    cmea_plot_image_file = input_file.split('.')[0] + '_cmea_plot.png'

    f.suptitle(input_file)
    f.savefig(cmea_plot_image_file)
    plt.show(block=False)

def get_channels_to_compare(all_channels, channels_to_compare_input):
    """
        This function returns an array of MCS_Data_Channel objects from the array of all channels
        input:
            all_channels([MCS_Data_Channel])
            channels_to_compare_input([int])
        output:
            channels_to_compare({MCS_Data_Channel})
    """
    channels_to_compare = []
    for channel in all_channels:
        if int(channel.channel_number) in channels_to_compare_input:
            channels_to_compare.append(channel)
    return channels_to_compare

def get_channels_to_analyze(all_channels, channels_to_compare_input):
    """
        This function returns an array of MCS_Data_Channel objects from the array of all channels
        input:
            all_channels([MCS_Data_Channel])
            channels_to_compare_input([int])
        output:
            channels_to_analyze([MCS_Data_Channel])
    """
    channels_to_analyze = []
    for channel in all_channels:
        if int(channel.channel_number) in channels_to_compare_input:
            channels_to_analyze.append(channel)
    return channels_to_analyze


def get_spike_time_differences(channels_to_compare, start_time, end_time):
    """
        This function gets the time difference between spikes between two channels.
        input:
            channels_to_compare([MCS_Data_Channel])
            start_time(float)
            end_time(float)
        output:
            spike_time_differences([float])
    """
    spike_times_in_interval = []
    for channel in channels_to_compare:
        channel_interval_spike_times = []
        for spike in channel.all_spikes:
            if (start_time < spike.spike_positive_end_time < end_time): # changed from peak time
                channel_interval_spike_times.append(spike.spike_positive_end_time)
        spike_times_in_interval.append(channel_interval_spike_times)
    
    spike_time_differences = []
    for i in range(0, len(spike_times_in_interval[0])):
        spike_time_differences.append(spike_times_in_interval[0][i] - spike_times_in_interval[1][i])

    return spike_time_differences
