# HSL_DEV

## Overview
This repo contains python scripts for analyzing MEA electrophysiology data.

## Installation
Download and install Anaconda for Python 2.7, found here: https://www.continuum.io/downloads

Download this repository and unzip it in your directory of choice. 


## Usage
To use these scripts, double click on their associated batch file. Alternatively, open a command line in the script's directory and enter `python script_name.py`. 
For example, to use CV_dev.py, enter `python CV_dev.py`.

### QT_dev.py
Analyzes QT intervals. The user selects a file, the channels to analyze within the file, then the QT region for each selected channel. The output is written to the command line for review. 

### CV_dev.py
Analyzes conduction velocity. The user selects a file, the two channels across which to analyze conduction velocity, then the region of data across which to analyze conduction velocity. The output is written to the command line for review. 

### Neuro_Pca_dev.py 
Analyzes and graphs spike features. The user selects a file and the channels to analyze within that file. 

### mcd_datatool_gen.py 
Generates bulk conversion scripts for MC DataTool. The user selects a folder, then the script generates a conversion script for MC_Datatool to convert all of the .mcd files in the folder and its subfolders. The script then generates a batch file that runs MC_DataTool with the generated conversion file. 

