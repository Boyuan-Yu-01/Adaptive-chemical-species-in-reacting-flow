import sys
import torch
from torch import tensor

import matplotlib.pyplot as plt

# Coordinates of the dot
x = 2
y = 3

# Create the plot
plt.scatter(x, y, color='red', s=100, label="Point (2,3)")  # Plot the dot

# Annotate the point
plt.annotate("This is the point (2,3)", 
             xy=(x, y), 
             xytext=(x + 0.5, y + 0.5),  # Offset text position
             arrowprops=dict(facecolor='black', arrowstyle="->"), 
             fontsize=12)

# Set axis limits
plt.xlim(0, 5)
plt.ylim(0, 5)

# Add labels and title
plt.xlabel("X-axis")
plt.ylabel("Y-axis")
plt.title("Single Dot with Annotation")

# Show the plot
plt.show()