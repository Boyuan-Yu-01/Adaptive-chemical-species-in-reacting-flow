import numpy as np
import sys
from tqdm import tqdm
import pandas as pd
import warnings


def progress_reaction_QSS_B(x_initial, t_start, k1, k2, k3, timeStep, t_interval=50, save_points=1):
    x = x_initial.copy()
    
    # define reacton nature, B is in quasi-steady state, so the concentration is fixed
    B = x[1,-1]
    A = [[-k1, k3*B], [0, 0]]
    b = [[0], [k2*B]]
    t = np.arange(t_start+timeStep, t_interval+t_start, timeStep)
    for i in tqdm(range(1,len(t))):   # reaction pregressions
        reaction = [[x[0,i-1]],[x[1,i-1]**2]]
        delta_x = (np.dot(A, reaction)+b) * timeStep     # delta_x record [[delta_A], [delta_C]]
        delta_x = np.insert(delta_x, 1, 0)[:,None]    # insert 0 to the second column!!!
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

# edit input parameters from bash script
timeStart = float(sys.argv[1])
timeStep = float(sys.argv[2])
inputFile = sys.argv[3]
outputFile = sys.argv[4]
t_interval = int(sys.argv[5])
save_points = int(sys.argv[6])
# timeStart = 7600
# timeStep = 0.001
# inputFile = '/home/boyuan-yu/Documents/USC/research/log/SVD_QSSA/unscale/unscale_00001.csv'
# outputFile = '/home/boyuan-yu/Documents/USC/research/log/SVD_QSSA/unscale/unscale_00001_test.csv'
# t_interval = 70
# save_points = 5

if inputFile != outputFile:
    df = pd.read_csv(inputFile).values 
    index = np.abs(df[:,0] - timeStart).argmin() # find the index of the time closest to t
    previous_data = df[:index, :]
    if index == 0 or index == len(df) - 1:
        print("\n\n\tThe time is out of range, you may consider to change a file.\n\n")
    species_0 = df[index, 1:][:,None]              # get the species concentration at time t
    new_data = progress_reaction_QSS_B(species_0, timeStart, k1, k2, k3, timeStep, t_interval, save_points)[1:,:]
    data = np.vstack((previous_data, new_data))
    df = pd.DataFrame(data, columns=['time', '[A]', '[B]', '[C]'])
    df.to_csv(outputFile, index=False)
else:
    df = pd.read_csv(outputFile)
    species_0 = np.array([
    df["[A]"].iloc[-1], 
    df["[B]"].iloc[-1], 
    df["[C]"].iloc[-1]
    ])
    species_0 = species_0[:,None]
    t_start = float(df["time"][len(df["time"])-1])
    previous_data = np.array(df[["time", "[A]", "[B]", "[C]"]])    
    new_data = progress_reaction_QSS_B(species_0, t_start, k1, k2, k3, timeStep, t_interval, save_points)[1:,:]
    data = np.vstack((previous_data, new_data))
    df = pd.DataFrame(data, columns=['time', '[A]', '[B]', '[C]'])
    df.to_csv(outputFile, index=False)