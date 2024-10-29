
import matplotlib.pyplot as plt
import numpy as np

# import the CSV file using numpy
path = "../../../data/ekg/mitdb_201.csv"

# load data in matrix from CSV file; skip first two rows

data = np.genfromtxt(path, delimiter=',')

# save each vector as own variable

time =  data[2:,0]
mlii = data [2:,1]
voltage = data[2:,2]

# use matplot lib to generate a single

plt.plot(time,voltage)
plt.xlabel("Time [s]")
plt.ylabel("Voltage [V]")
plt.show()