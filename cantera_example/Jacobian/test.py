import cantera as ct
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib.colors import Normalize
import numpy as np
import pandas as pd
scheme = "FFCM2.yaml"
# scheme = "FFCM1_21.yaml"

def const_vol_adia(gas, dt_max, t_end):
    '''this function simulates a constant pressure homogeneous reactor with adiabatic wall
       this function returns the mole fraction of each species at each time step.'''
    r = ct.IdealGasMoleReactor(gas)
    sim = ct.ReactorNet([r])
    sim.verbose = True
    states = ct.SolutionArray(gas)
    # initial conditions
    t = [0]  # initialise the time array
    P_ini = gas.P
    T_ini = gas.T
    rho_ini = gas.density
    net_production_rates_ini = gas.net_production_rates
    concentrations_ini = gas.concentrations
    X_ini = gas.X

    while sim.time < t_end:
        sim.advance(sim.time + dt_max)
        states.append(r.thermo.state)
        t.append(sim.time)
    
    # convert the states to numpy arrays
    t = np.array(t)                                                                         # time, have size m                                                       # pressure, have size m   
    P = np.array(states.P)                                                                  # pressure, have size m         
    P = np.insert(P, 0, P_ini )                           
    T = states.T                                                                            # temperature, have size m
    T = np.insert(T, 0, T_ini)
    rho = states.D                                                                          # density, have size m                         
    rho = np.insert(rho, 0, rho_ini)
    species = np.array(states.species_names)                                                # species names, have size n                                  
    net_production_rates = np.vstack((net_production_rates_ini, states.net_production_rates))                            # reaction rates, have size m*n
    concentrations = np.vstack((concentrations_ini, states.concentrations)) 
    X = np.vstack((X_ini, states.X))# concentrations, have size m*n
    
    return t, P, T, rho, species, net_production_rates, concentrations, X

##########################    
# set up the gas object ##
##########################
gas = ct.Solution(scheme)
T = 2000
P = 1 * ct.one_atm
X = "CH4:1, O2:2"
gas.TPX = T, P, X

# set up the t constraints for the simulation and output file
dt_max = 1e-8
t_end = 3e-5

# run the simulation 
t, P, T, rho, species, net_production_rates, concentrations, X = const_vol_adia(gas, dt_max, t_end)

##################################
## test: perturb the gas object ##
###################################

idx = 500
gas_m1 = {  # This dictionary stors the gas information at t(i-1)
        "t": t[idx-1],
        "P": P[idx-1],
        "T": T[idx-1],
        "species": species,
        "concentrations": concentrations[idx-1,:],
        "X": X[idx-1,:],
}

gas_1 = {  # This dictionary stores the gas information at t(i)  
        "t": t[idx],
        "P": P[idx],
        "T": T[idx],
        "species": species,
        "concentrations": concentrations[idx,:],
        "X": X[idx,:],
    }

# perturb gas_m1 object
delta = 0.1
species_idx = 2
T_perturb = gas_m1["T"]    # temperature will not change
P_perturb = gas_m1["P"] * (sum(gas_m1["concentrations"])) / (sum(gas_m1["concentrations"]) + gas_m1["concentrations"][species_idx]*delta) # since the concentration of a species is perturbed, the pressure will change
X = []
for i in range(len(gas_m1["concentrations"])):
    if i == species_idx:
        Xi = max((gas_m1["concentrations"][species_idx]*(1+delta))/ (sum(gas_m1["concentrations"]) + gas_m1["concentrations"][species_idx]*delta),0)
        X.append(Xi)
    else:
        Xi = max(gas_m1["concentrations"][i] / (sum(gas_m1["concentrations"]) + gas_m1["concentrations"][species_idx]*delta), 0)
        X.append(Xi)

X = dict(zip(gas_m1["species"], X))  # convert the list to a dictionary

# given TPX, now we create a after-perturbed gas object
gas_perturb = ct.Solution(scheme)
gas_perturb.TPX = T_perturb, P_perturb, X

dt_perturb = gas_1["t"] - gas_m1["t"]        # set up time constraints for the simulation
t_end_perturb = dt_perturb                        # set up time constraints for the simulation
_, _, _, _, species_perturbed, _, concentrations_perturbed, _ = const_vol_adia(gas_perturb, dt_max, t_end_perturb)

ini_perturb_concentration = concentrations_perturbed[0,:]
perturbed_species = species

## output into a csv file:
data = np.vstack((ini_perturb_concentration, gas_m1["concentrations"]))
data = np.vstack((data, (ini_perturb_concentration-gas_m1["concentrations"])/gas_m1["concentrations"]*100))
df = pd.DataFrame(data, columns=perturbed_species)
df.to_csv("test_perturb_concentration.csv", index=False)

