#! /usr/bin/env python

import sys
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import plot_ColorContrast as contrast
from csv_interpreter import csv_interpreter as reader

################################ Data Parser ####################################
# parser to convert csv data into dictionary form with variable types corrected
ot_data = []
csv_data = reader()
ot_data = csv_data.parse(sys.argv[1])

############################# Mode of processing ################################
plot_mode = int(sys.argv[2]) # 0: Overall; 1: Interval Increment
data_time_max = int(ot_data[len(ot_data)-1]['time'])
interval = 300 # Hardcored interval value
interest_min_time = 0

if plot_mode == 1:
    interest_max_time = interval
elif plot_mode == 0:
    interest_max_time = data_time_max
else:
    print("*** Error Unknown Plot mode!!! ***")

############################## Data processing ##################################

while (interest_max_time < (data_time_max + 1)):
    coord_data = [] # x, y
    traffic_data = [] # x, y, count
    for variable in ot_data:
        time = variable['time']
        x_coord = variable['x']
        y_coord = variable['y']

        if time >= interest_min_time and time <= interest_max_time:
            coord_data.append([x_coord, y_coord])

    traffic_data.append(coord_data[0]) 
    traffic_data[0].append(1) # count value
    num = 1 

    for i in range(1, len(coord_data)):
        for j in range(len(traffic_data)):
            if coord_data[i][0] == traffic_data[j][0] and coord_data[i][1] == traffic_data[j][1]:
                traffic_data[j][2] += 1
                num += 1
                break
        if num < (i + 1):
            traffic_data.append(coord_data[i])  
            traffic_data[len(traffic_data)-1].append(1)
            num += 1

    print("Total coordinate data entry count: " + str(len(coord_data)))
    print("Total unique coordinate data entry count: " + str(len(traffic_data)))

    # Convert data to plot axis 
    x_axis = []
    y_axis = []
    traffic_density = []

    for data in traffic_data:
        x_axis.append(data[0])
        y_axis.append(data[1])
        traffic_density.append(data[2])

    # traffic data coversion to log10 scale
    traffic_density_log = np.log(traffic_density)

################################ Figure Settings #############################
    plt.figure(figsize = (30, 20))
    plt.xlim(0, 180)
    plt.ylim(0, 100)
    plt.xlabel('X Coordinate, metres')
    plt.ylabel('Y Coordinate, metres')
    plt.title('Traffic Heatmap')    
    color_by = traffic_density_log
    # max_color_by = 0.8 * max(color_by)
    # min_color_by = min(color_by)
    dark_cmap = contrast.cmap_map(lambda x : x*0.85, matplotlib.cm.bwr)
    
    img = plt.imread("cgh_l3_cropped.png")
    plt.imshow(img, zorder = 0,extent = [0, 178, 100, 0])
#############################################################################

    plt.scatter(x_axis, y_axis, 
                c = color_by, 
                s = 10, marker='o', 
                alpha = '0.9',
                cmap = dark_cmap,
                vmin = 0 ,
                vmax = 8,
                zorder = 1).axes.invert_yaxis()
    plt.colorbar(label = 'Traffic Density')
    plt.savefig("img/heatmap_%s.png"%str(interest_max_time))
    plt.show()
    if (data_time_max == interest_max_time):
        interest_max_time = data_time_max + 1
    elif ((data_time_max - interest_max_time) < interval):
        interest_max_time = data_time_max
    elif (interest_max_time < data_time_max):
        interest_max_time += interval
    else:
        print("*** ERROR OCCURRED!!! *** ")
    
