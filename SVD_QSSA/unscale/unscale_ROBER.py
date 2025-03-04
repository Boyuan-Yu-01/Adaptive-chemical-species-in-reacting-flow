import numpy as np
import sys
from tqdm import tqdm
import pandas as pd
import warnings


# Define functions to progress the reaction
def progress_reaction(x_initial, t_start, A, timeStep, t_interval=50, save_points=1):
    # reaction progression of the ROBER problem
    x = x_initial.copy()
    t = np.arange(t_start+timeStep, t_interval+t_start, timeStep)
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
    
## Define the reaction coefficients and reaction matrix
k1 = 0.04
k2 = 3e7
k3 = 1e4
A = [[-k1, k3, 0],[k1, -k3, -k2],[0, 0, k2]]


# edit input parameters from bash script
timeStep = float(sys.argv[1])
outputFile = sys.argv[2]
t_interval = int(sys.argv[3])
save_points = int(sys.argv[4])

if sys.argv[5] == 'True':
    df = pd.read_csv(outputFile)
    species_0 = np.array([
    df["[A]"].iloc[-1], 
    df["[B]"].iloc[-1], 
    df["[C]"].iloc[-1]
    ])
    species_0 = species_0[:,None]
    t_start = float(df["time"][len(df["time"])-1])
    previous_data = np.array(df[["time", "[A]", "[B]", "[C]"]])
    new_data = progress_reaction(species_0, t_start, A, timeStep, t_interval, save_points)[1:,:]
    data = np.vstack((previous_data, new_data))
    df = pd.DataFrame(data, columns=['time', '[A]', '[B]', '[C]'])
    df.to_csv(outputFile, index=False)
else:
    species_0 = np.array([[1.0], [1e-6], [1e-6]])
    t_start = 0
    data = progress_reaction(species_0, t_start, A, timeStep, t_interval, save_points)
    df = pd.DataFrame(data, columns=['time', '[A]', '[B]', '[C]'])
    df.to_csv(outputFile, index=False)
    
    

