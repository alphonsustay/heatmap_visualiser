#! /usr/bin/env python

import os
import sys
import datetime
import cv2
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import plot_ColorContrast as contrast
from csv_interpreter import csv_interpreter as reader

print("[INFO] Welcome to the CSV - Heatmap Visualiser -- %s" %(str(datetime.datetime.now())))
################################ Data Parser ####################################
# parser to convert csv data into dictionary form with variable types corrected
ot_data = []
csv_data = reader()
ot_data = csv_data.parse(sys.argv[1])
if len(ot_data) != 0:
    print("[INFO] CSV data has successfully been parsed")
############################# Mode of processing ################################
plot_mode = int(sys.argv[2]) # 0: Overall; 1: Interval Increment
data_time_max = int(ot_data[len(ot_data)-1]['time'])
interval = 600 # Hardcoded interval value
interest_min_time = 0

if plot_mode == 1:
    interest_max_time = interval
    print("[INFO] Interval Plot Mode Selected")
elif plot_mode == 0:
    interest_max_time = data_time_max
    print("[INFO] Overall Plot Mode Selected")
else:
    print("[ERROR] Unknown Plot mode!!!")
###################### Creation of new folder directory #########################
time = datetime.datetime.now()
save_date = time.year * 10000 + time.month * 100 + time.day
save_time = time.hour *100 + time.minute
file_path ="img/" + str(save_date) + "_" + str(save_time) 
try:
    os.makedirs(file_path)
except OSError:
    print("[ERROR] Creation of the directory %s has failed" %file_path)
else:
    print("[INFO] Successfully created the directory %s" %file_path)

############################## Data processing ##################################
file_list = []
traffic_data = [] # x, y, count
data_count = 0

while (interest_max_time < (data_time_max + 1)):
    print("[INFO] Beginning Data Processing Iteration -- %s" %(str(datetime.datetime.now())))
    coord_data = [] # x, y

    for variable in ot_data:
        time = variable['time']
        x_coord = variable['x']
        y_coord = variable['y']

        if time > interest_min_time and time <= interest_max_time:
            coord_data.append([x_coord, y_coord])

    num = 0
    print("[INFO] Beginning Data Sorting Process -- %s" %(str(datetime.datetime.now())))
    for i in range(len(coord_data)):
        for j in range(len(traffic_data)):
            if coord_data[i][0] == traffic_data[j][0] and coord_data[i][1] == traffic_data[j][1]:
                traffic_data[j][2] += 1
                num += 1
                break
        if num < (i + 1):
            traffic_data.append(coord_data[i])  
            traffic_data[len(traffic_data)-1].append(1)
            num += 1
    data_count = data_count + len(coord_data)
    print("[INFO] Total data entry count: %d" %data_count)
    print("[INFO] Total unique data entry count: %d" %len(traffic_data))
############################### Data Plotting #################################

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
    plt.figure(figsize = (16, 9))
    plt.xlim(0, 180)
    plt.ylim(0, 100)
    plt.xlabel('X Coordinate, metres')
    plt.ylabel('Y Coordinate, metres')
    plt.title('Traffic Heatmap')    
    color_by = traffic_density_log
    dark_cmap = contrast.cmap_map(lambda x : x*0.9, matplotlib.cm.bwr)
    # img = plt.imread("background.png")
    # plt.imshow(img, zorder = 0,extent = [0, 178, 100, 0])
#############################################################################

    plt.scatter(x_axis, y_axis, 
                c = color_by, 
                s = 2, marker='o', 
                alpha = '0.9',
                cmap = dark_cmap,
                vmin = 0 ,
                vmax = 8,
                zorder = 1).axes.invert_yaxis()
    plt.colorbar(label = 'Traffic Density')
    file_name = 'heatmap_%s.png'%(str(interest_max_time))
    plt.savefig('%s/%s'%(file_path, file_name), dpi = 720, bbox_inches='tight')
    file_list.append(file_name)
    if (data_time_max == interest_max_time):
        interest_max_time = data_time_max + 1
    elif ((data_time_max - interest_max_time) < interval):
        interest_min_time = interest_max_time
        interest_max_time = data_time_max
    elif (interest_max_time < data_time_max):
        interest_min_time = interest_max_time
        interest_max_time += interval
    else:
        print("*** ERROR OCCURRED!!! *** ")
    
########################## Animation Processing ###############################    
if plot_mode == 1:
    print(file_list)
    fourcc = cv2.VideoWriter_fourcc(*'MJPG')
    fps = 1
    plot_check = cv2.imread('%s/%s'%(file_path, file_list[0]), 1)
    height = plot_check.shape[0]
    width = plot_check.shape[1]
    print(height, width)
    out = cv2.VideoWriter('%s/heatmap_animation.mp4'%file_path, fourcc, fps, (width, height) )

    for f in range(len(file_list)):
        plot = cv2.imread('%s/%s'%(file_path, file_list[f]))
        out.write(plot)

    out.release()
print("[INFO] Process has completed! -- %s" %(str(datetime.datetime.now())))
