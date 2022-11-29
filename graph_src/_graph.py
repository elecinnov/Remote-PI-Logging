'''
Operating script for the EDM data graphing utility in python. More information about how the graphing and data
    analysis functions operate can be found in example.py and Graph.py.

This script can be modified to utilise the graphing utility by changing the starting parameters. These are described below.


'''

from Graph import Graphing
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import sys

if __name__ == "__main__":

# Configuration parameters #


    # Data Input and dataframe building config #

    # Single data file flag set to true if only using a single data file
    single_file = False
    # Directory containing only the data files to be used for multiple file processing (single_file = False)
    filedir = "path to files"
    # Type of file in directory to search for (".txt" or ".dta" only)
    filetype = ".txt"
    # If using mutilple files specify the name for the out file (if saving)
    outfile = "outfiledir/outfile"
    # If using a single file specify it 
    infile = "input data file"
    # Specify using presaved csv.zip data (will override single file and multiple file specifications)
    OpenCsv = True
    # Csv.zip file name/path
    csvfile = "csvfilename"
    # Specify if the data is in hexadecimal 
    hexfile = False
    # Specify if the data is instantaneous (heavily reduced functionality)
    intsdata = False
    # Specify if a historgram of EDM page length (rows between time stamps) and width (number of data columns) is requried 
    histogram = False
    # Specify if you wish to remove sections of data with columns smaller than the lagest from the historgam ( depreciated )
    removenone = False

    # Names of data channes recorded by the EDM in order from left to right in the file ( required for plotting )
    channel_names = ["Channel 1","Channel 2","Channel 3","Channel 4"]
    # Specify if all data should be plotted ('Time_all') or only time stamped data ('Time_real') for Subplots ansd 2yplot
    data_method = 'Time_all'
    # Specify if data columns should be scaled 
    scaling = True
    # Provide a list of columns to be scaled (list of list if they are scaled by the same factor )
    columns = [["Channel 1"], ["Channel 2","Channel 3"], ["Channel 4"]]
    # A list of scaling factors to be multiplied by the values in the columns
    scale_factors = [scale factor 1, scale factor 2, scale factor 3]

    # Set to true if you wish to save the data frame as a csv
    save = False
    # Copression type ('zip' or 'gzip' only at the moment)
    compression = 'zip'


    # GRAPHING SELECTION #

    # Set to true to plot ints data
    Graph_ints = False
    
    # Set to true to plot instantaneous data on one plot with two axis
    Graph_2y_ints =False
    # List of channels to plot on the first y-axis
    Iaxis1 = ["Left Y-axis data"]
    # List of channels to plot on the second y-axis
    Iaxis2 = ["Right Y-axis data"]
    # Number of Time samples to skip at the start of plotting
    cut = 100294
    # Value to convert samples to time steps.
    Ifactor = 12
    # X-axis title
    Ixaxis = "X-axis Label"
    # Left yaxis title
    Iyaxis1 = "Left Y-axis label"
    # Right yaxis title
    Iyaxis2 = "Right Y-axis Label"
    # right yaxis limits
    Iyaxis2_lim = [lower right axis limit,upper right axis limit]
    # Colours for each of the data channels (must match number of plotted lines)
    Ilin_col = ['r','b']

    # Set to True to plot a single plot with only timestamped data 
    Graph_stamped = True
    # Number of plots to create (match length of lists)
    numberGS = 3
    # List of specific channels (None indicates all on one plot)
    specGS = [None, ["Channel 1","Channel 2"], "Channel 3"]
    # List of times to start plotitng for each plot (sometimes is funky)
    startGS = [None, None]

    # Set to true to plot single plots using all the available data
    Graph_all = True
    # Number of plots to create 
    numberGA = 2
    # List of specific channels (None indicates all on one plot)
    specGA = [None,"Channel 4"]
    # List of times to start plotitng for each plot (sometimes is funky)
    startGA = [None,None]

    # Set to True to produce a subplot with 3 plots 
    subplot = False
    # A list of lists containg the data columns to be plotted on each subplot 
    subplotdata = [["Channel 1"],["Channel 2","Channel 3"],["Channel 4"]]
    # Labels for each yaxis of the plot
    subplot_ylabels = ["Top y label ", "Mid y label","Bottom y label"]
    # Label for the shared xaxis of the plot
    subplot_xlabel = "X axis Label"
    # Super label for the Y axis (can be left blank )
    subplot_yaxis = "Y Axis title "

    # Set to true to produce a sing plot with 2 y-axis
    ploty2 = True
    # List of channels to plot on the first y-axis
    axis1 = ["Channel 1","Channel 2"]
    # List of channels to plot on the second y-axis
    axis2 = ["Channel 3","Channel 4"]
    # Colours for each of the data channels (must match number of plotted lines)
    line_col = ["r","b","g","m"]
    # X-axis label
    xlab = "time"
    # first yaxis label
    ylab1 = "ylabel1"
    # second yaxis label 
    ylab2 = "ylabel2"


# Appliaction section #

    if OpenCsv:
        obj = Graphing("", hexflag = hexfile)
        obj.open_csv(csvfile)
    else:
        if single_file:
            obj = Graphing(infile, hexflag = hexfile)
            obj.mkdata()
        else:
            obj = Graphing("", hexflag = hexfile)
            filelist = obj.collect_files(extension = filetype, directory = filedir)
            obj.join_data_text(filelist, outfile)

    obj.name_channel(channel_names)

    if histogram:
        obj.Histogram_data()

    if removenone:
        obj.Remove_None()

    if scaling:
        for idx in range(len(columns)):
            obj.Convert_channel(columns[idx],scale_factors[idx])

    if intsdata:
        if Graph_ints:
            obj.mkGraph_inst()
        if Graph_2y_ints:
            obj.single_plot_2y_inst(Iaxis1, Iaxis2,Ilin_col, xaxis = Ixaxis, yaxis =Iyaxis1,yaxis2 = Iyaxis2, y2lim = Iyaxis2_lim, samplecut = cut,samplefact = Ifactor, legendsize = 10)
        plt.show()
        sys.exit(0)
        

    if data_method == 'Time_all' or Graph_all:
        obj.ext_time_d()

    if Graph_stamped:
        for idy in range(numberGS):
            obj.mkGraph_true(specific = specGS[idy], start_time = startGS[idy])

    if Graph_all:
        for idz in range(numberGA):
            obj.mkGraph_add(specific = specGA[idz], start_time = startGA[idz])

    if subplot:
        obj.Subplot_data(subplotdata,method = data_method, ylabels = subplot_ylabels, yaxis = subplot_yaxis, xaxis = subplot_xlabel)

    if ploty2:
        obj.single_plot_2y(axis1,axis2,line_col,method = data_method)

    if save:
        obj.save_compress(compression)

    
    plt.show()
    
