#! /usr/bin/python

import csv
import sys
import numpy as np
import matplotlib.pyplot as plt
import matplotlib

ot_data = []

def cmap_map(function, cmap):
    cdict = cmap._segmentdata
    step_dict = {}
    for key in ('red', 'green', 'blue'):
        step_dict[key] = list(map(lambda x: x[0], cdict[key]))
    step_list = sum(step_dict.values(), [])
    step_list = np.array(list(set(step_list)))
    reduced_cmap = lambda step : np.array(cmap(step)[0:3])
    old_LUT = np.array(list(map(reduced_cmap, step_list)))
    new_LUT = np.array(list(map(function, old_LUT)))
    cdict = {}
    for i, key in enumerate(['red','green','blue']):
        this_cdict = {}
        for j, step in enumerate(step_list):
            if step in step_dict[key]:
                this_cdict[step] = new_LUT[j, i]
            elif new_LUT[j,i] != old_LUT[j, i]:
                this_cdict[step] = new_LUT[j, i]
        colorvector = list(map(lambda x: x + (x[1], ), this_cdict.items()))
        colorvector.sort()
        cdict[key] = colorvector
    return matplotlib.colors.LinearSegmentedColormap('colormap',cdict,1024)


# Header Checker and Adder [Header fileds are hardcoded] 'log_ot_20200416_171758.csv'
with open(sys.argv[1], 'r') as f:
    read = csv.reader(f)
    data = [line for line in read]

    if (data[0][0]) != 'time':
        new_data = [['time', 'model_name', 'model_type', 'x', 'y', 'z', 'yaw', 'level_name']]
        # print(len(data))

        for count in range(len(data)):
            new_data.append(data[count])
        data = new_data
        # print(len(data))

        with open(sys.argv[1], 'w') as f:
            write = csv.writer(f)
            write.writerows(data)

# Data Cleanup [data conversion to dict and variable typing]
with open(sys.argv[1], 'r') as f:
   for row in csv.DictReader(f):
       ot_data.append(dict(row))

for variable in ot_data:
   variable['time'] = float(variable['time'])
   variable['x'] = round(float(variable['x'])*2)/(2.0)
   variable['y'] = round(float(variable['y'])*2)/(2.0)
   #variable['z'] = float(variable['z'])
   #variable['yaw'] = float(variable['yaw'])
   # only the variable of interest will be processed

# Data processing
data_time_max = ot_data[len(ot_data)-1]['time']
interest_max_time = data_time_max # can be changed later to time duration of interest
interest_min_time = 0.0
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

color_by = traffic_density_log
max_color_by = 0.8 * max(color_by)
min_color_by = min(color_by)

dark_cmap = cmap_map(lambda x : x*0.85, matplotlib.cm.bwr)

plt.figure(figsize = (25, 15))
plt.scatter(x_axis, y_axis, 
            c = color_by, 
            s =15, marker='o', 
            alpha = '0.9',
            cmap = dark_cmap,
            vmin = min_color_by,
            vmax = max_color_by).axes.invert_yaxis()

plt.colorbar(label = 'Traffic Density')   
plt.xlabel('X Coordinate, metres')
plt.ylabel('Y Coordinate, metres')
plt.title('Traffic Heatmap')
plt.savefig("heatmap.pdf")
plt.show()

