#! /usr/bin/env python

import csv
import sys

sys.dont_write_bytecode = True

parsed_data = []

class csv_interpreter():

    def parse(self, file):
        # Header Checker and Adder [Header fileds are hardcoded under new_data]
        with open(file, 'r') as f:
            read = csv.reader(f)
            data = [line for line in read]

            if (data[0][0]) != 'time':
                new_data = [['time', 
                             'model_name', 
                             'model_type', 
                             'x', 
                             'y', 
                             'z', 
                             'yaw', 
                             'level_name']]
                # print(len(data))

                for count in range(len(data)):
                    new_data.append(data[count])
                data = new_data
                # print(len(data))

                with open(file, 'w') as f:
                    write = csv.writer(f)
                    write.writerows(data)

        # Data Cleanup [data conversion to dict and variable typing]
        with open(file, 'r') as f:
            for row in csv.DictReader(f):
                parsed_data.append(dict(row))

        # Variable X, Y are adjusted to the submeter granularity
        for variable in parsed_data:
            variable['time'] = float(variable['time'])
            variable['x'] = round(float(variable['x'])*2)/(2.0)
            variable['y'] = round(float(variable['y'])*2)/(2.0)
            #variable['z'] = float(variable['z'])
            #variable['yaw'] = float(variable['yaw'])
            # only the variable of interest will be processed

        return parsed_data
