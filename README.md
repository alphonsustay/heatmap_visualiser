# heatmap_visualiser

## The repo holds a few python scripts which processes x, y robot traffic coordinates collected over a  period of time and displays the data in a scatter plot

The heatmap_visualiser.py will

1) Call `csv_interpreter.py` to read the given CSV file, extracted from the simulated traffic movement. The `csv_interpreter.py` also cleans up the key value variable type as well as sets the value granularity(x, y coordinates) to be used in `heatmap_visualiser.py`

2) Process the traffic coordinated data logged in the CSV file

3) Plot the data into scatter plot for visualisation of the traffic flow

** The `plot_ColorContrast.py` is an added function to make adjustments to the color contrast of the Traffic Density scale. This is to make the plots more visable

##  ** How to run **

run `python heatmap_visualiser <*.csv file> <plot mode value>`


### plot mode feature

The plot mode feature is currently still in development. The purpose is allow the selection of data visualisation modes. The current modes are:

- Overall data visualisation: plot mode value = 0
- Interval Incremental visualisation: plot mode value = 1

The interval incremental visualisation is to allow the user to study the changes of the traffic density as the time frame increases. The time interval is currently hardcoded within the `heatmap_visualiser.py` under the `interval` variable. Current, implementation of the interval imcremental visualisation requires the user to close each data plot before the next interval set is processed.
