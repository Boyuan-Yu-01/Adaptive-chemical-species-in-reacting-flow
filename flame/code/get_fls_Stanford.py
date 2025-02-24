'''The purpose of this script is to calculate the fls at conditions given by Stanford experiment.'''
# Import libraries
import pandas as pd
import numpy as np
import os
import random
import cantera as ct
import pandas as pd
import multiprocessing as mp
import json
import re
from pathlib import Path
import shutil

Stanford_dir = "/home/boyuan-yu/Documents/USC/research/log/flame/Stanford_fls/"
Stanford_file = "methane_flame_speed_2.xlsx"
# mechanism = 'FFCM2.yaml'
mechanism = "FFCM1_skeletal.yaml"

# flame function
def flame(T,P,X,scheme,file_name,save_path,restart_csv=None):
    ''' Create flame object and save it as csv file under save_path.'''
    files = os.listdir(save_path)
    if file_name.replace(save_path,'') in files:
        print(f"Flame {file_name} already exists.")
        flame = pd.read_csv(save_path + file_name)
        velocity = flame["velocity"][0] * 100
        return velocity
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
        f.save(save_path+file_name, basis='mole',overwrite=True)
        print(f"Flame resolved and documented as {file_name}")
        return f.velocity[0] * 100
    except ct.CanteraError as e:
        print(f"CantaraError: {e} \n Fail to resolve flame {file_name}.")
        return None
    except Exception as e:
        print(f"Unexpected error: {e} \n Fail to resolve flame {file_name}.")
        return None
    
def fls_accurate(T,P,X,scheme,restart_file,restart_path):
    '''This function is similar to the flame function. 
            DIFFERENCE:
            - If the flame object does not exist, function "flame" will be called to generate the preliminary flame object.
            - Given the flame object exists, this function restarts the flame object with:
                                                                                - transport_model = 'multicomponent'
                                                                                - Soret effect enabled'''
    files = os.listdir(restart_path)
    if restart_file.replace(restart_path,'') not in files:
        print(f"{restart_file} has not been generated.")
        print(f"Generating {restart_file} (rough guess)...")
        flame(T,P,X,scheme,restart_file,restart_path,restart_csv="restart.csv")
    restart_csv = restart_path + restart_file
    print(f"recalculating {restart_file}...")
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
        return f.velocity[0] * 100
    except ct.CanteraError as e:
        print(f"CantaraError: {e} \n Fail to resolve flame {restart_file}.")
        return None
    except Exception as e:
        print(f"Unexpected error: {e} \n Fail to resolve flame {restart_file}.")
        return None

# read "Stanford_file"
df = pd.read_excel(Stanford_dir + Stanford_file, sheet_name='Sheet1')
file_data = df.to_dict(orient='list')

case = []   # create a list to store the case name.
temp_path = [] # temp_path is used to temporarily store the flame of the first round
T = []
P = []
X = []
phi = []
Stanford_fls = []
cantera_accurate_fls = []
error_accurate = []
error_rough = []

for i in range(len(file_data['Species'])):
    species_i = file_data['Species'][i]
    Temp_i = file_data['Temp'][i]
    Pres_i = file_data['Pres'][i]
    phi_i = file_data['Phi'][i]
    oxi_comp_i = file_data['Oxi_comp'][i]
    fls_i = file_data["FFCM-2"][i]
    
    # construct P, T, X for Cantera to run the simulation
    species_i = species_i + ": " + str(phi_i)  # add phi to species name
    numbers = re.findall(r':\s*([\d\.]+)', oxi_comp_i)  # Find oxidizer composition from "oxi_comp_i" by extracting the float numbers
    numbers = list(map(float, numbers))  # convert the numbers to float
    oxi_comp_new = [i * 2/numbers[0] for i in numbers]  # convert the oxidizer composition to mole fraction
    oxi_comp_i = re.sub(r'(: )[\d\.]+', lambda m: m.group(1) + str(oxi_comp_new.pop(0)), oxi_comp_i)  # replace the oxidizer composition in "oxi_comp_i" with the new composition
    X_i = species_i + "," + oxi_comp_i
    Pres_i = float(Pres_i)
    Temp_i = float(Temp_i)
    fls_i = float(fls_i)
    case.append(f"case{i}.csv")
    temp_path.append(Stanford_dir + "temp/")
    T.append(Temp_i)
    P.append(Pres_i)
    phi.append(phi_i)
    X.append(X_i)
    Stanford_fls.append(fls_i)

#################################################################################################################################
# Use multiple cores to solve the initial round of flame object. ###########################################################
task_cpu = mp.cpu_count() - 2 # leave two cores idle for daily use
os.makedirs(Stanford_dir + "temp/", exist_ok=True)
with mp.Pool(processes=task_cpu) as pool:
    cantera_rough_fls = pool.starmap(flame, zip(T, P, X, [mechanism]*len(T), case, temp_path, ["restart.csv"]*len(T)))
#################################################################################################################################

#################################################################################################################################
# Use single core to solve the accurate flame speed #######################################################################
for i in range(len(case)):
    fls_i_cantera = fls_accurate(T[i], P[i], X[i], mechanism, case[i], temp_path[i])
    cantera_accurate_fls.append(fls_i_cantera)
    error_accurate.append(abs(fls_i_cantera - Stanford_fls[i]))
    error_rough.append(abs(cantera_rough_fls[i] - Stanford_fls[i]))

# shutil.rmtree(temp_path[0]) # remove the temporary directory
    
## Save result into a .csv file:
# step 1: create a dictionary
result = {
    "T": T,
    "P": P,
    "X": X,
    "phi": phi,
    "Stanford_fls [cm/s]": Stanford_fls,
    "cantera_rough_fls [cm/s]": cantera_rough_fls,
    "cantera_accurate_fls [cm/s]": cantera_accurate_fls,
    "error_accurate": error_accurate,
    "error_rough": error_rough,
}
# step2: store them into the csv file
df = pd.DataFrame(result)
df.to_csv(Stanford_dir+"methane_fls_skeletal.csv", index=False)

print(f"Mean error (accurate): {np.mean(error_accurate)}") # print mean absolute error
print(f"Max error (accurate): {np.max(error_accurate)}") # print max absolute error
print(f"Min error (accurate): {np.min(error_accurate)}") # print min absolute error
print(f"Mean error (rough): {np.mean(error_rough)}") # print mean absolute error
print(f"Max error (rough): {np.max(error_rough)}") # print max absolute error
print(f"Min error (rough): {np.min(error_rough)}") # print min absolute error