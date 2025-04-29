#!/usr/bin/python

import matplotlib.pyplot as plt
import numpy as np
from os import path, scandir

def read_probe_data(filename):
    # Read the header lines to get probe locations
    with open(filename, 'r') as f:
        probe_locations = []
        for i in range(9):  # First 9 lines are probe locations
            line = f.readline().strip()
            if line.startswith('# Probe'):
                probe_locations.append(line)
    
    # Read the data, skipping the header
    data = np.loadtxt(filename, skiprows=10)
    
    return data, probe_locations

# Read data from p file
probe_file = 'postProcessing/p/0/p'
data, probe_locations = read_probe_data(probe_file)

# Create the plot
plt.figure(figsize=(12, 8))

# Plot data for each probe
time = data[:, 0]  # First column is time
for i in range(1, 10):  # Columns 1-9 are probe data
    pressure = data[:, i]
    label = probe_locations[i-1]
    plt.plot(time, pressure, label=label)

# Add labels and legend
plt.xlabel('Time (s)')
plt.ylabel('Pressure (Pa)')
plt.title('Pressure Evolution at Probe Points')
plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
plt.grid(True)

# Adjust layout to prevent label cutoff
plt.tight_layout()

# Show the plot
plt.show()
