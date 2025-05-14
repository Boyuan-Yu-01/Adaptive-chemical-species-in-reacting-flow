import cantera as ct
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib.colors import Normalize
import numpy as np
import pandas as pd
# scheme = "FFCM2.yaml"
scheme = "FFCM1_21.yaml"

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
    concentrations = np.vstack((concentrations_ini, states.concentrations))                                  # concentrations, have size m*n
    
    return t, P, T, rho, species, net_production_rates, concentrations

def individual_plot(t_array, mu, species_list, S):
    """This function plots the individual species mu history"""
    idx = species_list.tolist().index(S)
    mu_S = mu[:,idx]
    
    # Plot the mu history of species S
    plt.plot(t_array, mu_S)
    plt.xlabel('Time (s)')
    plt.ylabel('dimensionless net production rate (abs)')
    plt.grid(True)
    plt.title(f'Species {S} mu history')
    # plt.show()
    plt.savefig(f"mu_{S}.png", dpi=300, bbox_inches='tight')
    plt.close()
    


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
t, P, T, rho, species, net_production_rates, concentrations = const_vol_adia(gas, dt_max, t_end)

# get the dimensionless net production rates named "mu"
mu = np.zeros_like(net_production_rates)
for i in range(1, len(mu)):         # we skip the INITIAL time step since t^j - t^(j-1) does not exist
    for j in range(len(species)): 
        mu[i][j] = abs(net_production_rates[i][j] / concentrations[i][j] * (t[i] - t[i-1])) # this is the dimensionless net production rate
        np.seterr(invalid='ignore')  # suppress warning

# Plot the mu history of species of interest
highlight_major = ["O2", "H2O", "CO2", "CH4"]
highlight_minor = ["H", "OH", "C2H4", "C2H2", "C2H6"]

for S in highlight_major:
    individual_plot(t, mu, species, S)
for S in highlight_minor:
    individual_plot(t, mu, species, S)
