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

def Calculate_Jacobian(t, P, T, species, net_production_rate, concentrations, idx):
    """ This function use perturbation method to approximate the Jacobian matrix of the system."""
    
    # Step 1: strip off t(i-1), P(i-1), T(i-1), X(i-1), net_production_rate(i-1), concentrations(i-1) 
    #               and t(i),   P(i),   T(i),   X(i),   net_production_rate(i),   concentrations(i), STORE EACH OF THESE INFORMATION INTO A DICTIONARY
    
    
    # Step 2: Stack Species, X, Concentrations of the same time step together, then reorder them using the descending order of the net_production_rate(i-1)
    
    # Step 3: Evaluate the perturbed system evolving from t(i-1) to t(i)
        # 3.1: looping over each species, perturb its concentration, advance the system to t(i), so that we can get the perturbed CONCENTRATIONS (by perturbing S_i)
        # 3.2: For each perturbed concentration, we can solve a COLUMN of the Jacobian matrix
    
    # Step 4: Return the Jaconbian matrix at t[i]
    


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
