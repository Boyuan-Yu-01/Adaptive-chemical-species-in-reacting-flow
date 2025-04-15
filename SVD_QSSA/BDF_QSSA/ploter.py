'''This script is created to draw QSSA species-time evolution plot and real species_time evolution plot.'''
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

file_path = "ROBER_1e4/"
QSSA_csv = file_path + "ROBER_QSSA_4250.csv"
direct_csv = file_path + "ROBER_BDF.csv"

# Read the CSV file
QSSA_data = np.array(pd.read_csv(QSSA_csv).values.tolist())
direct_data = np.array(pd.read_csv(direct_csv).values.tolist())

# Create vertical subplots (2 rows, 1 column)
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(8, 6), sharex=True)

# Top plot
ax1.plot(direct_data[:,0], direct_data[:,1], label='species A, direct', color = "black")
ax1.plot(direct_data[:,0], direct_data[:,3], label='species B, direct', color = "red")
ax1.plot(QSSA_data[:,0], QSSA_data[:,1], label='species A, QSSA', color = "black", linestyle='--')
ax1.plot(QSSA_data[:,0], QSSA_data[:,3], label='species B, QSSA', color = "red", linestyle='--')
ax1.set_ylabel('concentration')
ax1.set_xlabel('t')
ax1.legend()
ax1.grid()


# Bottom plot
ax2.plot(direct_data[:,0], direct_data[:,2], label='species B', color = "navy")
ax2.plot(QSSA_data[:,0], QSSA_data[:,2], label='species B, QSSA', color = "navy", linestyle='--')
ax2.set_ylabel('concentration')
ax2.set_xlabel('t')
ax2.legend()
ax2.grid()

# Adjust layout
plt.xlim([0, direct_data[-1,0]])
plt.tight_layout()
plt.show()