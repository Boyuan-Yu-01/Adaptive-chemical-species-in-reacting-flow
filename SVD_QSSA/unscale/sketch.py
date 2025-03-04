import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

import os
print("Current Directory:", os.getcwd())  # Show the directory where the script is running


k1 = 0.04
k2 = 3e7
k3 = 1e4

t0 = 30.0601
A0 = 0.744153177
B0 = 1.04E-05
C0 = 0.25583845

alpha = k3*B0**3
beta = k3/k1*B0*C0-k3/k1*B0**3
gamma = A0 + k3/k1*B0**3 - k3/k1*B0*C0

t = np.linspace(0, 20000-t0, 1000)
A = np.zeros(t.shape)
A = alpha*t + beta + gamma * np.exp(-k1*t)
C = k2*B0**2*t + C0

df = pd.read_csv('QSSA_ana_2.csv').values

plt.plot(t, A, color='blue', linestyle="--", label=f'A:QSSA')
plt.plot(t, C, color='green', linestyle="--",label=f'C:QSSA')
plt.xlabel('t')
plt.ylabel('Concentration')
plt.legend()
plt.title(f'QSSA at t={t0:.3f}')
plt.show()