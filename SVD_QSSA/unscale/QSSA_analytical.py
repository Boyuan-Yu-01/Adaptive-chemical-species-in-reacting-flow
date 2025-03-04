''' This file is to emply the QSSA to species B and applying the analytical solution
to species A and C.'''

import numpy as np
from tqdm import tqdm
import pandas as pd


def analytical_QSSA(t_start, t_end, file_name, k1, k2, k3, save_points=1000000):
    # Analytical solution of the ROBER problem
    t = np.linspace(0, t_end-t_start, save_points)  # time from 0 to t_end-t_start
    df = pd.read_csv(file_name).values
    index = np.abs(df[:,0] - t_start).argmin()
    if index == 0 or index == len(df) - 1:
        print("\n\n\tThe time is out of range, you may consider to change a file.\n\n")
        exit()
    df = df[:index,:]
    x_ini = df[index-1:index,1:]   # x_ini = [[A0, B0, C0]]
    previous_data = df[:-1,:]
    x = np.zeros((len(t)-1, 3))
    x = np.vstack((x_ini, x))
    x_ini = x[0,:]
    alpha = k2*k3/k1*x_ini[1]**3
    beta = (k3/k1)*x_ini[1]*x_ini[2] - (k2*k3/k1**2)* x_ini[1]**2
    gamma = k2*k3/k1**2*x_ini[1]**3 - k3/k1*x_ini[1]*x_ini[2] + x_ini[0]
    
    for i in tqdm(range(1,len(t))):
        A = alpha * t[i] + beta + gamma * np.exp(-k1*t[i])
        B = x_ini[1]
        C = k2*x_ini[1]**2*t[i] + x_ini[2]
        x[i] = [A, B, C]
        if np.max(x[i]) > 2:
            t = t[:i]
            x = x[:i,:]
            break
    t = t + t_start
    if t.shape[0] > 500:
        indices = np.linspace(0, t.shape[0]-1, num=500, dtype=int)
        t = t[indices]
        x = x[indices,:]
    data = np.hstack((t[:,None], x))
    data = np.vstack((previous_data, data))
    return data


# input_file = "unscale_ini.csv"    # for case1 and case2
input_file = "unscale_00001.csv"    # for rest cases
output_file = "QSSA_ana_6.csv"
# t_start = 10**-2  # case2
# t_start = 7600  # case3
# t_start = 10    # case5
t_start = 100    # case6
# t_start = 1000    # case7
# t_start = 5000    # case8
# t_start = 500   # case9
# t_start = 10000 # case10
t_end = 2*10**4

k1 = 0.04
k2 = 3e7
k3 = 1e4
data = analytical_QSSA(t_start, t_end, input_file, k1, k2, k3)
df = pd.DataFrame(data, columns=['time', '[A]', '[B]', '[C]'])
df.to_csv(output_file, index=False)