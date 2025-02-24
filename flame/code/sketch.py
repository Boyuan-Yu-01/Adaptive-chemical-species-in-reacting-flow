# Importing libraries
import numpy as np
import os
import random
import cantera as ct
import pandas as pd
import multiprocessing as mp
import json
import re
from pathlib import Path
mechanism = 'FFCM2.yaml'

# Functions
def flame(T,P,X,scheme,file_name,save_path,restart_csv=None):
    ''' Create flame object and save it as csv file under save_path.'''
    files = os.listdir(save_path)
    if file_name.replace(save_path,'') in files:
        print(f"Flame {file_name} already exists.")
        return None
    if restart_csv and not Path(restart_csv).is_file(): # check if restart file exists
        if files == []:                                 # if no files in directory, set restart_csv to None
            restart_csv = None
        else:                                           # if files exist in directory, randomly select a file to restart from
            restart_csv = save_path + random.choice(files)
    gas = ct.Solution(scheme) # define gas with mechanism scheme
    p = P * ct.one_atm # initioal pressure unit Pa
    gas.TPX = T, p, X  # define initial state of gas with T (K), p (Pa), X (mole fraction)
    try:
        f = ct.FreeFlame(gas, width=0.03) # define flame with gas, and reaction regio domain, unit of width [m]
        f.set_refine_criteria(ratio=3, slope=0.02, curve=0.02) # set up criteria for refining grid
        f.transport_model = 'mixture-averaged'
        f.energy_enabled = True
        if restart_csv != None:
            df = pd.read_csv(restart_csv)
            df_pruned = df[::2]
            f.set_initial_guess(data=df_pruned)
            f.solve(loglevel=0)
        else:
            f.solve(loglevel=0, auto=True)
        f.save(file_name, basis='mole',overwrite=True)
        print(f"Flame resolved and documented as {file_name}")
        # return f
        return None
    except ct.CanteraError as e:
        print(f"CantaraError: {e} \n Fail to resolve flame {file_name}.")
        return None
    except Exception as e:
        print(f"Unexpected error: {e} \n Fail to resolve flame {file_name}.")
        return None
    
def flame_accurate(T,P,X,scheme,file_name,save_path):
    '''This function is similar to the flame function. 
            DIFFERENCE:
            - If the flame object does not exist, function "flame" will be called to generate the preliminary flame object.
            - Given the flame object exists, this function restarts the flame object with:
                                                                                - transport_model = 'multicomponent'
                                                                                - Soret effect enabled'''
    files = os.listdir(save_path)
    if file_name.replace(save_path,'') not in files:
        print(f"Flame {file_name} has not been generated.")
        print(f"Generating flame {file_name} (rough guess)...")
        flame(T,P,X,scheme,file_name,save_path,restart_csv=None)
    restart_csv = save_path + file_name
    gas = ct.Solution(scheme) # define gas with mechanism scheme
    p = P * ct.one_atm # initioal pressure unit Pa
    gas.TPX = T, p, X  # define initial state of gas with T (K), p (Pa), X (mole fraction)
    f = ct.FreeFlame(gas, width=0.03) # define flame with gas, and reaction regio domain, unit of width [m]
    f.set_refine_criteria(ratio=3, slope=0.02, curve=0.02) # set up criteria for refining grid
    f.transport_model = 'multicomponent'
    f.soret_enabled
    f.energy_enabled = True
    df = pd.read_csv(restart_csv)
    df_pruned = df[::2]
    f.set_initial_guess(data=df_pruned)
    f.solve(loglevel=0)
    f.save(file_name, basis='mole',overwrite=True)
    print(f"Flame resolved and documented as {file_name}")
    return None

save_path = "flame_objects/"    # Define the path to save the flame objects
# Define the PTX of the flame object
T = [298, 298, 298, 360, 360, 360, 400, 400, 400, 298, 298, 298]            # Temperature in K
P = [0.25, 0.5, 3.0, 1.0, 5.0, 10.0, 1.0, 5.0, 10.0, 4.0, 10.0, 20.0]       # Pressure in atm
phi_lower = [0.7, 0.6, 0.6, 0.8, 0.8, 0.8, 0.8, 0.8, 0.8, 0.65, 0.8, 0.8]   # Lower equivalence ratio
phi_upper = [1.4, 1.5, 1.4, 1.2, 1.2, 1.2, 1.2, 1.2, 1.2, 1.2, 1.2, 1.4]    # Upper equivalence ratio
phi = [[0]*10]*len(phi_lower)                                               # Initialise equivalence ratio
for i in range(len(phi_lower)):                                             # Create equivalence ratio matrix
    phi_temp = np.linspace(phi_lower[i], phi_upper[i], 10)
    phi[i] = [phi_temp[j] for j in range(len(phi_temp))]
    
X_temp = f"CH4:%f,O2:2,N2:7.52"%(phi[0][0])
flame_accurate(T[0],P[0],X_temp,mechanism,"flame_0_0.csv",save_path)    # Generate flame object