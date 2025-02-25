import numpy as np
import sys
from tqdm import tqdm
import pandas as pd
import warnings

# function
def progress_reaction(x_initial, t_start, A, timeStep, t_interval=50, save_points=1):
    # reaction progression of the ROBER problem
    x = x_initial.copy()
    t = np.arange(t_start+timeStep, t_interval+t_start+timeStep, timeStep)
    for i in tqdm(range(1,len(t))):   # reaction pregressions
        reaction = [[x[0,i-1]],[x[1,i-1]*x[2,i-1]],[x[1,i-1]**2]]
        delta_x = np.dot(A, reaction) * timeStep
        if np.min(x[:, i-1] + delta_x[:, 0])<0:
            warnings.warn('Concentration values are negative. Take zero instead.')
        new_x = np.maximum(x[:, i-1] + delta_x[:, 0], 0)
        x = np.hstack((x, new_x[:, None]))
        if np.max(x[:, i]) > 1e3:
            sys.exit('Concentration values are too high. Exiting...')
    data = np.hstack((t[:,None], x.T))
    indices = np.linspace(0, data.shape[0]-1, num=save_points, dtype=int)
    data = data[indices]
    return data

## edit input parameters from bash script
# timeStep = float(sys.argv[1])
# output = sys.argv[2]
timeStep = 0.0001 # for testing

## Define the reaction coefficients and reaction matrix
k1 = 0.04
k2 = 3e7
k3 = 1e4
A = [[-k1, k3, 0],[k1, -k3, -k2],[0, 0, k2]]
alpha = 1e-3
# beta = 4e5
# gamma = 1
beta = 448998.89
gamma = 8064.0
coefs = np.array([alpha, beta, gamma])

## Construct A_prime
spec_trans = [1/alpha, 1/beta, 1/gamma] 
spec_trans = np.diag(spec_trans)
reac_trans = [1/alpha, 1/(beta * gamma), 1/(beta * beta)]
reac_trans = np.diag(reac_trans)
A_prime = np.dot(np.linalg.inv(spec_trans), np.dot(A, reac_trans))
print(np.linalg.eigvals(A_prime))




# ## save the results to a csv file
# t = t[:,None]
# data = np.hstack((t, x.T))
# indices = np.linspace(0, data.shape[0]-1, num=300, dtype=int)
# data = data[indices]
# df = pd.DataFrame(data, columns=['time', '[A]', '[B]', '[C]'])
# df.to_csv('output.csv', index=False)