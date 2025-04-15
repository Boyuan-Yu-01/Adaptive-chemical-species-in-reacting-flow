from scipy.integrate import solve_ivp
import numpy as np
import matplotlib.pyplot as plt
import csv
import pandas as pd

csv_name = 'ROBE_BDF_QSSA_test.csv'

# Define the QSSA ROBER as a system of ODEs
def QSSA_ROBER(t, sysUnknow, k1=0.04, k2=3e7, k3=1e4):
    y1,y2,y3 = sysUnknow
    y1_dot = -k1*y1 + k3*y2*y3
    y2_dot = 0.0
    y3_dot = k2*y2**2
    return [y1_dot, y2_dot, y3_dot]

# initial conditions
y0 = [0.10744463654298722, 4.807361041364581e-07, 0.892554883623283]
t_span = (0,1e3)
t_eval = np.arange(t_span[0],t_span[1],1e-4)

# define switch threshold
threshold = 1e-3

sol = solve_ivp(QSSA_ROBER, t_span, y0, t_eval=t_eval, method='BDF')

t = sol.t
y1 = sol.y[0]
y2 = sol.y[1]
y3 = sol.y[2]

plt.plot(t, y1, label='species A')
plt.plot(t, y2, label='species B')
plt.plot(t, y3, label='species C')
plt.xlabel('t')
plt.ylabel('concentration')
plt.legend()
plt.grid(True)
plt.show()