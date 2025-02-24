'''This programme is meant to create and log flame objects that have PTX from FFCMII webpage.
    https://web.stanford.edu/group/haiwanglab/FFCM2/docs/Results/Test/
'''

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
        print(f"{file_name} has not been generated.")
        print(f"Generating {file_name} (rough guess)...")
        flame(T,P,X,scheme,file_name,save_path,restart_csv="restart.csv")
    restart_csv = save_path + file_name
    print(f"recalculating {file_name}...")
    gas = ct.Solution(scheme) # define gas with mechanism scheme
    p = P * ct.one_atm # initioal pressure unit Pa
    gas.TPX = T, p, X  # define initial state of gas with T (K), p (Pa), X (mole fraction)
    try:
        f = ct.FreeFlame(gas, width=0.03) # define flame with gas, and reaction regio domain, unit of width [m]
        f.set_refine_criteria(ratio=3, slope=0.02, curve=0.02) # set up criteria for refining grid
        f.transport_model = 'multicomponent'
        f.soret_enabled
        f.energy_enabled = True
        df = pd.read_csv(restart_csv)
        df_pruned = df[::2]
        f.set_initial_guess(data=df_pruned)
        f.solve(loglevel=0)
        f.save(restart_csv, basis='mole',overwrite=True)
        print(f"Flame resolved and documented as {file_name}")
        return None
    except ct.CanteraError as e:
        print(f"CantaraError: {e} \n Fail to resolve flame {file_name}.")
        return None
    except Exception as e:
        print(f"Unexpected error: {e} \n Fail to resolve flame {file_name}.")
        return None
        
def recover_flame_csv(path, fileName, scheme):
    '''Recover a flame object from csv files in save_path.'''
    # Open and read the JSON file to get the PTX of the flame object
    with open(path+"TPX_flames.json", "r") as json_file:
        TPX = json.load(json_file)  
    
    # extract the index in order to find the corresponding PTX
    numbers = re.findall(r'_(\d+)',fileName)  # extract the index in order to find the corresponding PTX
    T_flame = TPX['T'][int(numbers[0])]
    P_flame = TPX['P'][int(numbers[0])]
    phi_flame = TPX['phi'][int(numbers[0])][int(numbers[-1])]
    X_flame = f"CH4:%f,O2:2,N2:7.52"%(phi_flame)
    try:
        gas = ct.Solution(scheme)
        gas.TPX = T_flame, P_flame*ct.one_atm, X_flame
        f = ct.FreeFlame(gas, width=0.03)
        f.set_initial_guess(data=path+fileName)
        return f
    except Exception as e:
        print(f"Unexpected error: {e} \n Fail to recover flame {fileName}.")
        return None

def flame_csv_to_dict (path, fileName, scheme):
    '''Convert flame csv file to dictionary, and add mole concentration
    of each species to the dictionary.'''
    df = pd.read_csv(path+fileName)
    dict = df.to_dict(orient='list')
    flame = recover_flame_csv(path, fileName, scheme)    
    flame_mole_density = flame.density_mole # [kmol/m^3]
    # add mole concentration of each species to the dictionary. Prior to that, check if
    # the length of grid and mole density are equal.
    if len(flame_mole_density) != len(dict['grid']):
        print(f"Error: The length of grid and mole density are not equal.")
        return None
    else:
        for i in range(4, len(dict.keys())):
            new_key = "MC_"+list(dict.keys())[i][2:]    # 'MC' stands for Mole Concentration
            new_value = dict[list(dict.keys())[i]] * flame_mole_density
            dict.update({new_key: new_value})
    return dict

def dict_clct_flames_dict(path, scheme, fileName='ALL'):
    '''Collect all flame csv files in the path and collect them to a master_dict'''
    if fileName == 'ALL':
        # Open and read the JSON file to get the PTX of the flame object
        f_m_dict = {}   # master dictionary to collect all flame dictionaries
        with open(path+"TPX_flames.json", "r") as json_file:
            TPX = json.load(json_file)
        # extract the index in order to find the corresponding PTX
        files = os.listdir(path)
        files = [file for file in files if not file.endswith('.json')]
        for csv in files:
            numbers = re.findall(r'_(\d+)',csv)  # extract the index in order to find the corresponding PTX
            T_flame = f"{float(TPX['T'][int(numbers[0])]):.2f}"
            T_flame = T_flame.replace('.','_')
            P_flame = f"{float(TPX['P'][int(numbers[0])]):.2f}"
            P_flame = P_flame.replace('.','_')
            phi_flame = f"{float(TPX['phi'][int(numbers[0])][int(numbers[-1])]):.2f}"
            phi_flame = phi_flame.replace('.','_')
            key_name = f"P{P_flame}T{T_flame}X{phi_flame}"
            flame_csv = flame_csv_to_dict(path, csv, scheme)
            f_m_dict.update({key_name: flame_csv})
        return f_m_dict
    else:
        print("This part of the code is not yet implemented.")
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

TPX_flames = {
    'T': T,
    'P': P,
    'phi': phi
}
with open(save_path + 'TPX_flames.json', 'w') as json_file:
    json.dump(TPX_flames, json_file, indent=4)

# Determine the number of CPUs for executing the code
max_cpu = mp.cpu_count() - 2
task_cpu = 50
task_cpu = min(task_cpu, max_cpu)
print(f"Number of CPUs on this programme: {task_cpu}")

#####################################################################################
## use multiprocessing to execute the flame function
# # create list of arguements (tuple)
# input_data = []
# for i in range(len(T)):
#     for j in range(len(phi[0])):
#         X_temp = f"CH4:%f,O2:2,N2:7.52"%(phi[i][j])
#         P_temp = P[i]
#         T_temp = T[i]
#         # file_name = save_path + f"flame_{i}_{j}.csv"                                # create file name for saving flame object  
#         file_name = f"flame_{i}_{j}.csv"                                # create file name for saving flame object  
#         # if i == 0 and j == 0:   # first iteration has no restart
#         #     restart_csv = None
#         # elif i != 0 and j == 0: # [i,0] has restart from [i-1,0]  
#         #     restart_csv = save_path + f"flame_{i-1}_{j}.csv"
#         # else:                   # [i,j] has restart from [i,j-1]
#         #     restart_csv = save_path + f"flame_{i}_{j-1}.csv"
#         # params_temp = (T_temp, P_temp, X_temp, mechanism, file_name,save_path, restart_csv)   # create tuple as arguement input for flame function
#         params_temp = (T_temp, P_temp, X_temp, mechanism, file_name,save_path)   # create tuple as arguement input for flame function
#         input_data.append(params_temp)
        
# # # Execute the flame function in parallel
# # with mp.Pool(processes=task_cpu) as pool:
# #         results = pool.starmap(flame, input_data)  # `starmap` unpacks each tuple as function argumentsf = flame(input_data[i])
# # print("All flames resolved.")      

#####################################################################################

# Use single core to execute the flame function
for i in range(len(T)):
    for j in range(len(phi[0])):
        X_temp = f"CH4:%f,O2:2,N2:7.52"%(phi[i][j])
        P_temp = P[i]
        T_temp = T[i]
        file_name = f"flame_{i}_{j}.csv"                                # create file name for saving flame object  
        flame_accurate(T_temp, P_temp, X_temp, mechanism, file_name,save_path)   # create tuple as arguement input for flame function
print("All flames resolved.")        

        
