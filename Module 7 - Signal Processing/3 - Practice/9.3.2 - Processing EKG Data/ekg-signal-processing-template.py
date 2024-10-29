import matplotlib.pyplot as plt
import numpy as np

"""
Step 0: Select which database you wish to use.
"""

# database name
database_name = 'mitdb_201'

# path to ekg folder
path_to_folder = "../../../data/ekg/"

# select a signal file to run
signal_filepath = path_to_folder + database_name + ".csv"

"""
Step #1: load data in matrix from CSV file; skip first two rows. Call the data signal.
"""

signal = 0
data = np.genfromtxt(signal_filepath, delimiter=',')

time =  data[2:,0]
mlii = data [2:,1]
voltage = data[2:,2]

"""
Step 2: (OPTIONAL) pass data through LOW PASS FILTER (fs=250Hz, fc=15, N=6). These may not be correctly in radians
"""

## YOUR CODE HERE ##

"""
Step 3: Pass data through weighted differentiator
"""
diff_conv = [1,-1]
diffs = np.convolve(voltage,diff_conv)

"""
Step 4: Square the results of the previous step
"""
 ## YOUR CODE HERE ##

norm_data = np.square(diffs)

"""
Step 5: Pass a moving filter over your data
"""

## YOUR CODE HERE
window = [1,1,1,1,1,1,1,1,1,1]
moving_average = np.convolve(voltage, window)

# make a plot of the results. Can change the plot() parameter below to show different intermediate signals
plt.title('Process Signal for ' + database_name)
plt.plot(time[len(norm_data)], norm_data)
plt.show()