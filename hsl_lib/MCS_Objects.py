import os, time, math
import matplotlib.pyplot as plt 
import numpy as np
from matplotlib.widgets import SpanSelector

class MCS_Spike(object): 
    """
    This object represents an individual spike. It takes a snapshot of voltage data and analyzes the positive and negative peak of that snapshot. 
    Its init arguments are channel(int), voltage_data([float]), and timestamp_data([float)]
    """


    channel = 0
    start_time = 0.0
    timestamp_data = [0.0]
    voltage_data = [0.0]

    def analyze_positive_peak(self, voltage_data, timestamp_data):
        """
        This function analyzes the positive peak of a spike.
        input:
            voltage_data([float])
            timestamp_data([float])
        output:
            spike_max(float), 
            spike_positive_start_time(float)
            spike_max_time(float)
            spike_positive_end_time(float)
            area_under_curve_positive(float), 
            spike_half_peak_width_positive(float), 
            spike_positive_slope(float)
        """
        area_under_curve_positive = 0.0
        first_half_peak_positive = 0
        second_half_peak_positive = 0
        spike_positive_start_time = 0
        spike_positive_end_time = 0
        voltage_data = self.voltage_data
        time_data = self.timestamp_data

        spike_max = max(voltage_data)
        max_index = np.argmax(voltage_data)
        spike_max_time = time_data[max_index]

        for p in range((np.argmax(voltage_data)), 0, -1):
            area_under_curve_positive += (float(voltage_data[p]))
            if voltage_data[p] <= math.floor((max(voltage_data)/2)):
                first_half_peak_positive = p
            if voltage_data[p] <= 0:
                spike_positive_start_time = time_data[p]
                break
        
        #Start from the maxVoltage timepoint and work forwards until you hit a zero 
        for p in range((np.argmax(voltage_data)), 1000-(np.argmax(voltage_data)), 1):
            area_under_curve_positive += (float(voltage_data[p]))
            if voltage_data[p] <= (math.floor((max(voltage_data))/2)):
                second_half_peak_positive = p
            if voltage_data[p] <= 0:
                spike_positive_end_time = time_data[p]
                break 
            if p == len(timestamp_data) - 1:
                spike_positive_start_time = timestamp_data[p]
                break
                    
        spike_half_peak_width_positive = (second_half_peak_positive - first_half_peak_positive) * 0.02

        if spike_max_time - spike_positive_start_time != 0:
            spike_positive_slope = spike_max / (spike_max_time - spike_positive_start_time)
        else:
            spike_positive_slope = 0

        return spike_max, spike_positive_start_time, spike_max_time, spike_positive_end_time, area_under_curve_positive, spike_half_peak_width_positive, spike_positive_slope

    def analyze_negative_peak(self, voltage_data, timestamp_data):

        """
        This function analyzes the negative peak of the voltage data.
        input:
            voltage_data([float])
            timestamp_data([float])
        output:
            spike_min(float), 
            spike_negative_start_time(float), 
            spike_min_time(float), 
            spike_negative_end_time(float), 
            area_under_curve_negative(float), 
            spike_half_peak_width_negative(float), 
            spike_negative_slope(float)
        """
        area_under_curve_negative = 0
        first_half_peak_negative = 0
        second_half_peak_negative = 0
        spike_negative_start_time = 0
        spike_negative_end_time = 0
        voltage_data = self.voltage_data
        time_data = self.timestamp_data

        spike_min = min(voltage_data)

        min_index = np.argmin(voltage_data)

        spike_min_time = time_data[min_index]

        #Start from the minVoltage timepoint and work backwards until you hit a zero                    
        for p in range(min_index, 0, -1):
            area_under_curve_negative += (float(voltage_data[p]))
            if voltage_data[p] >= (math.floor((min(voltage_data))/2)):
                first_half_peak_negative = p
            if voltage_data[p] >= 0:
                spike_negative_start_time = timestamp_data[p]
                break
        
        #Start from the minVoltage timepoint and work forwards until you hit a zero 
        for p in range(min_index, 1000-(np.argmin(voltage_data)), 1):
            area_under_curve_negative += (float(voltage_data[p]))
            if voltage_data[p] >= (math.floor((min(voltage_data))/2)):
                second_half_peak_negative = p
            if voltage_data[p] >= 0:
                spike_negative_end_time = timestamp_data[p]
                break 
            if p == len(timestamp_data) - 1:
                spike_negative_end_time = timestamp_data[p]
                break

        
        spike_half_peak_width_negative = (second_half_peak_negative - first_half_peak_negative) * 0.02

        spike_negative_slope = spike_min / (spike_min_time - spike_negative_start_time)

        return spike_min, spike_negative_start_time, spike_min_time, spike_negative_end_time, area_under_curve_negative, spike_half_peak_width_negative, spike_negative_slope

    def __init__(self, channel, voltage_data, timestamp_data): 
        
        self.channel = channel
        self.voltage_data = [x - voltage_data[0] for x in voltage_data]
        self.timestamp_data = timestamp_data
        #print("Generating spike...")


        # Positive Peak
        spike_max, spike_positive_start_time, spike_max_time, spike_positive_end_time, area_under_curve_positive, spike_half_peak_width_positive, spike_positive_slope = self.analyze_positive_peak(voltage_data, timestamp_data)

        self.spike_max = spike_max      
        self.spike_positive_start_time = spike_positive_start_time
        self.spike_max_time = spike_max_time
        self.spike_positive_end_time = spike_positive_end_time
        self.positive_time = spike_positive_end_time - spike_positive_start_time
        self.area_under_curve_positive = area_under_curve_positive
        self.spike_half_peak_width_positive = spike_half_peak_width_positive
        self.spike_positive_slope = spike_positive_slope  

        # Negative Peak
        spike_min, spike_negative_start_time, spike_min_time, spike_negative_end_time, area_under_curve_negative, spike_half_peak_width_negative, spike_negative_slope = self.analyze_negative_peak(voltage_data, timestamp_data)

        self.spike_min = spike_min
        self.spike_negative_start_time = spike_negative_start_time 
        self.spike_min_time = spike_min_time
        self.spike_negative_end_time = spike_negative_end_time
        self.spike_negative_total_time = spike_negative_end_time - spike_negative_start_time
        self.area_under_curve_negative = area_under_curve_negative
        self.spike_half_peak_width_negative = spike_half_peak_width_negative
        self.spike_negative_slope = spike_negative_slope
        
        self.area_under_curve_total = area_under_curve_positive + area_under_curve_negative

        self.spike_max_min_interval = spike_min_time - spike_max_time

class MCS_Data_Channel(object):
    """
        This object represents all information for a given non-analog channel on the cMEA. 

        __init__ parameters: voltage_data([float]), time_data([float]), channel_number(int), sampling_rate(float)


    """

    def get_waveform_stats(self, all_spikes):
        """
            This function takes all spikes from a channel and computes the average/std at each point of the waveform. 
            input: 
                all_spikes([MCS_Spike])
            output: 
                average_waveform([float]),  
                std_waveform([float])

        """ 
        all_spikes = self.all_spikes
        if len(all_spikes) == 0:
            return [0], [0]

        all_spike_data = []
        average_waveform = []
        std_waveform = []
        voltage_index_data = []

        for spike in all_spikes:
            all_spike_data.append(spike.voltage_data)

        for voltage_index in range(0, len(all_spike_data[0])):
            voltage_index_data = []
            for spike_index in range(0, len(all_spike_data)):
                voltage_index_data.append(all_spike_data[spike_index][voltage_index])
            average_waveform.append(np.mean(voltage_index_data))
            std_waveform.append(np.std(voltage_index_data))

        return average_waveform, std_waveform


    def get_stats(self, data):
        """
        This function computes the mean and standard deviation of a given float array. 
        input: data([float])
        output: data_mean(float), data_std(float)
        """
        data_mean = np.mean(data)
        data_std = np.std(data)
        return data_mean, data_std

    def get_spikes(self, channel_number, voltage_data, time_data, spike_threshold):
        """
        This function scans the voltage data of a channel for crossings of the spike threshold, grabbing data around that threshold and generating MCS_Spikes from that data. 
        input: 
            channel_number(int), 
            voltage_data([float]), 
            time_data([float]), 
            spike_threshold(float)
        output: 
            all_spikes([MCS_Spike])
        """
        all_spikes = []
        this_spike_voltage_data = []
        this_spike_time_data = []
        pass_index = 0

        spike_window_start = 150
        spike_window_end = 1850
        #print(spike_threshold)
        for index in range(spike_window_start, len(voltage_data) - spike_window_end):
            if index > pass_index:
                if voltage_data[index] > spike_threshold:
                    this_spike_voltage_data = voltage_data[index-spike_window_start:index+spike_window_end]
                    this_spike_time_data = time_data[index-spike_window_start:index+spike_window_end]
                    this_spike = MCS_Spike(channel_number, this_spike_voltage_data, this_spike_time_data)
                    all_spikes.append(this_spike)
                    pass_index = index + spike_window_end
        return all_spikes

    def get_over_threshold_number(self, voltage_data, spike_threshold):
        """"
        This function scans voltage data and returns the number of data points above the threshold. 
        input: voltage_data([float]), spike_threshold(float)
        """
        over = 0
        for data_point in voltage_data:
            if data_point >= spike_threshold:
                over += 1
        return over


    def __init__(self, voltage_data, time_data, channel_number, sampling_rate):
        self.voltage_data = voltage_data
        self.time_data = time_data
        self.channel_number = int(channel_number)
        self.sampling_rate = sampling_rate
        print("Processing MCS Channel " + str(channel_number))
        #print(str(len(voltage_data)) + " data points")

        voltage_mean, voltage_std = self.get_stats(voltage_data)
        self.voltage_mean = voltage_mean
        self.voltage_std = voltage_std

        spike_threshold = voltage_mean + 5*voltage_std #changed from 5
        self.spike_threshold = spike_threshold# 5 stds above the mean

        #over_threshold_number = self.get_over_threshold_number(voltage_data, spike_threshold)
        #self.over_threshold_number = over_threshold_number

        all_spikes = self.get_spikes(channel_number, voltage_data, time_data, spike_threshold)
        self.all_spikes = all_spikes

        average_waveform, std_waveform = self.get_waveform_stats(all_spikes)
        self.average_waveform = average_waveform
        self.std_waveform = std_waveform

class MCS_Analog_Channel:

    def __init__(self, voltage_data, time_data, channel_name):
        self.voltage_data = voltage_data
        self.time_data = time_data
        self.channel_name = channel_name



class QT_Region_Selector(object):
    """
    This function selects a region of average waveform data, defining the QT interval as the start and end of that interval. It depends on the user visually determining the QT interval themselves.
    input: 
        qt_channel(MCS_Channel)
    """
    
    def __init__(self, qt_channel):
        plt.close()
        self.qt_channel = qt_channel
        self.title = "Channel " + str(qt_channel.channel_number)

        self.qt_average_waveform = qt_channel.average_waveform
        self.qt_average_waveform_x = range(0, len(self.qt_average_waveform))

        self.qt_all_spikes = qt_channel.all_spikes

        self.fig = plt.figure()
        self.ax = self.fig.add_subplot(311)
        self.ax1 = self.fig.add_subplot(312)
        self.ax2 = self.fig.add_subplot(313)
        self.line2, = self.ax2.plot(self.qt_average_waveform)

        self.indmax = 0
        self.indmin = 0

        qt_start_point, qt_end_point = self.get_QT_interval(self.fig, self.ax, self.ax1, self.ax2, self.line2, self.qt_average_waveform, self.qt_all_spikes)

        self.qt_start_point, self.qt_end_point = qt_start_point, qt_end_point



    def get_QT_interval(self, fig, ax, ax1, ax2, line2, qt_average_waveform, qt_all_spikes):
        """
        This function allows the user to select the QT interval for a region of data. 
        input:
            fig(plt.fig)
            ax, ax1, ax2(plt.fig.subplot)
            line2(plt.fig.subplot.plot([float]))
            qt_average_waveform([float])
            qt_all_spikes([MCS_Spike])
        """
        ax.set_title(self.title)
        ax.plot(qt_average_waveform) 
        for spike in qt_all_spikes:
            ax1.plot(spike.voltage_data)
      
        span = SpanSelector(ax, self.onselect, 'horizontal', useblit=True,
                        rectprops=dict(alpha=0.5, facecolor='red'))

        plt.show(block=False)
        a = raw_input("Press any key... ")

        qt_start_point = self.indmin
        qt_end_point = self.indmax

        return qt_start_point, qt_end_point

    def onselect(self, xmin, xmax):
        """
        This is the onselect function for the Spanselector in get_QT_interval above.
        """
        indmin, indmax = np.searchsorted(self.qt_average_waveform_x, (xmin, xmax))
        indmax = min(len(self.qt_average_waveform) - 1, indmax)


        thisx2 = self.qt_average_waveform_x[indmin:indmax]
        thisy2 = self.qt_average_waveform[indmin:indmax]

        self.indmin = indmin
        self.indmax = indmax

        self.line2.set_data(thisx2, thisy2)
        self.ax2.set_xlim(thisx2[0], thisx2[-1])
        self.ax2.set_ylim(min(thisy2), max(thisy2))
        self.fig.canvas.draw()


class CV_Region_Selector(object):
    """
    This object lets the user select a region of data over which to calculate conduction velocity 
    __init__ variables: 
        channels_to_compare([MCS_Data_Channel]), 
        stim_channel(MCS_Analog_Channel)

    """
    
    def __init__(self, channels_to_compare, stim_channel):
        self.channels_to_compare = channels_to_compare
        self.title = str(channels_to_compare[0].channel_number) + " - > " + str(channels_to_compare[1].channel_number)

        self.channel_data_1 = channels_to_compare[0].voltage_data
        #self.channel_data_1_x = channels_to_compare[0].time_data
        self.channel_data_1_x = range(0, len(self.channel_data_1))
        self.channel_data_2 = channels_to_compare[1].voltage_data
        #self.channel_data_2_x = channels_to_compare[1].time_data
        self.channel_data_2_x = range(0, len(self.channel_data_2))

        self.stim_data = stim_channel.voltage_data

        self.fig = plt.figure()
        self.ax = self.fig.add_subplot(411)
        self.ax_stim = self.fig.add_subplot(412)
        self.ax1 = self.fig.add_subplot(413)
        self.line1, = self.ax1.plot(self.channel_data_1)
        self.ax2 = self.fig.add_subplot(414)
        self.line2, = self.ax2.plot(self.channel_data_2)

        self.indmax = 0
        self.indmin = 0

        start_time, end_time = self.get_CV_region(self.fig, self.ax, self.ax_stim, self.ax1, self.ax2, self.line1, self.line2, self.channel_data_1, self.channel_data_2, self.stim_data)

        self.start_time, self.end_time = start_time, end_time



    def get_CV_region(self, fig, ax, ax_stim, ax1, ax2, line1, line2, channel_data_1, channel_data_2, stim_data):
        """
            This function allows the user to select a region for the 
        """
        ax.set_title(self.title)
        ax.plot(channel_data_1)
        ax.plot(channel_data_2)     
        ax_stim.plot(stim_data)
      
        span = SpanSelector(ax, self.onselect, 'horizontal', useblit=True,
                        rectprops=dict(alpha=0.5, facecolor='red'))

        plt.show(block=False)
        a = raw_input("Press any key... ")

        start_time = self.channels_to_compare[0].time_data[self.indmin]
        end_time = self.channels_to_compare[0].time_data[self.indmax]

        return start_time, end_time

    def onselect(self, xmin, xmax):
        indmin, indmax = np.searchsorted(self.channel_data_1_x, (xmin, xmax))
        indmax = min(len(self.channel_data_1) - 1, indmax)

        thisx1 = self.channel_data_1_x[indmin:indmax]
        thisy1 = self.channel_data_1[indmin:indmax]
        thisx2 = self.channel_data_2_x[indmin:indmax]
        thisy2 = self.channel_data_2[indmin:indmax]

        self.indmin = indmin
        self.indmax = indmax

        self.line1.set_data(thisx1, thisy1)
        self.line2.set_data(thisx2, thisy2)
        self.ax1.set_xlim(thisx1[0], thisx1[-1])
        self.ax1.set_ylim(min(thisy1), max(thisy1))
        self.ax2.set_xlim(thisx2[0], thisx2[-1])
        self.ax2.set_ylim(min(thisy2), max(thisy2))
        self.fig.canvas.draw()