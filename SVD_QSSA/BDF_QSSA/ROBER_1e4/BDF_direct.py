from scipy.integrate import solve_ivp
import numpy as np
import matplotlib.pyplot as plt
import csv
import pandas as pd
from time import perf_counter


csv_name = 'ROBE_BDF.csv'

# Define ROBER as a system of ODEs
def ROBER(t, sysUnknow, k1=0.04, k2=3e7, k3=1e4):
    y1,y2,y3 = sysUnknow
    y1_dot = -k1*y1 + k3*y2*y3
    y2_dot = k1*y1 - k2*y2**2 - k3*y2*y3
    y3_dot = k2*y2**2
    return [y1_dot, y2_dot, y3_dot]

# initial conditions
y0 = [1.0, 0.0, 0.0]
t_span = (0,1e4)
t_eval = np.linspace(*t_span, int(1e8))

start = perf_counter()
# Solve using BDF method
sol = solve_ivp(ROBER, t_span, y0, t_eval=t_eval, method='BDF')
end = perf_counter()

print(f"Time taken: {end - start:.2f} seconds")    
    
# Extract the solution
t = sol.t
y1 = sol.y[0]
y2 = sol.y[1]
y3 = sol.y[2]


# # Save the solution to a CSV file
# data = np.vstack((sol.t,sol.y))
# data = data.T
# data = pd.DataFrame(data, columns=['t', 'y1', 'y2', 'y3'])
# data.to_csv(csv_name, index=False)

# Create vertical subplots (2 rows, 1 column)
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(8, 6), sharex=True)

# Top plot
ax1.plot(t, y1, label='species A')
ax1.plot(t, y3, label='species C')
ax1.set_ylabel('concentration')
ax1.set_xlabel('t')
ax1.legend()
ax1.grid()


# Bottom plot
ax2.plot(t, y2, label='species B')
ax2.set_ylabel('concentration')
ax2.set_xlabel('t')
ax2.legend()
ax2.grid()

# Adjust layout
plt.xlim(*t_span)
plt.tight_layout()
plt.show()