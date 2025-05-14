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

def plotter(t_array, mu, concentrations, species, t_step):
    '''this function plots the dimensionless net production rates for each species at a given time step with decending order.'''
    # Given the time step, find the closest time_step and its index in t_array
    idx = np.argmin(np.abs(t_array - t_step))   # find the index of the closest time_step in the array
    t_step = t_array[idx]                       # get the value
    
    # Sort the mu and species arrays in the decending order of mu
    mu_idx = mu[idx,:]
    concentrations_idx = concentrations[idx,:]
    combined = sorted(zip(mu_idx, concentrations_idx, species), key=lambda x: x[0], reverse=True)
    mu_idx, concentrations_idx, species = map(np.array, zip(*combined))
    
    # Give warning message if the concentrations are effectively zero
    danger_level = 1e-12    # this parameter needs to be tuned
    indicies = np.where(concentrations_idx < danger_level)[0]
    
    # highlight some species
    hightlight_major = ["O2", "H2O", "CO2", "CH4"]
    hightlight_minor = ["H", "OH", "C2H4", "C2H2", "C2H6"]
    colours = []
    for s in species:
        if s in hightlight_major:
            colours.append('red')
        elif s in hightlight_minor:
            colours.append('blue')
        else:
            colours.append('black')

    # Plot
    spacing = 1.5
    x = np.arange(len(mu_idx)) * spacing
    fig, ax = plt.subplots(figsize=(20,10))
    # bars = ax.bar(x, mu_idx, edgecolor='black')
    bars = ax.bar(x, mu_idx, color=colours, edgecolor='black')

    # Set custom x-ticks and labels with spacing
    ax.set_xticks(x)
    ax.set_xticklabels(species, color='black', rotation=90)

    # Highlight selected labels
    for idx in indicies:
        ax.get_xticklabels()[idx].set_color('red')

    # Axis labels and title
    plt.ylabel(r'$\mu$')
    plt.title(rf'$\mu$ at t = {t_step:.2e} s')

    # Save figure
    plt.savefig(f'mu_{t_step:.2e}.png', dpi=300, bbox_inches='tight')

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


## Plot mu at the time step of interest
t_1 = np.linspace(0, 8e-6, 3)               # Nothing seems to happen
t_2 = np.linspace(8e-6, 1.3e-5, 3)[1:]      # Some radicals seems to be formed
t_3 = np.linspace(1.3e-5, 2.3e-5, 10)[1:]   # Reaction quickly happens
t_4 = np.linspace(2.3e-5, 3e-5, 6)[1:]      # Nothing seems to happen
t = np.hstack((t_1, t_2, t_3, t_4))


for t_step in t:
    plotter(t, mu, concentrations, species, t_step)
    print(f"Plotting mu at t = {t_step:.2e} s")
