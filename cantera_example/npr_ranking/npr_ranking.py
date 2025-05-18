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

#############################
## output mu to a csv file ##
#############################
csv_name = "npr.csv"
t = t.reshape(-1, 1)  # reshape t to be a column vector
data = np.hstack((t, net_production_rates))
species_output = np.char.add(species, "_[kmol/m^3/s]")
headers = np.hstack(("t", species_output))
df = pd.DataFrame(data, columns=headers)
df.to_csv(csv_name, index=False)

######################################################################
## evenly choose 10 time steps, and select 9 species to plot out mu ##
######################################################################
# species_interest = ["CH4", "CO2", "H2O", "O2", "C2H6", "C2H4", "C2H2", "OH", "H"]
species_interest = ["CO2", "C2H6", "C2H4", "C2H2", "OH", "H"]
number_of_time_steps = 20
column_indicies = [np.where(species == s)[0][0] for s in species_interest]     # get the indicies of the species of interest in "species"
npr_trimmed = net_production_rates[:,column_indicies]
row_indicies = np.linspace(0, npr_trimmed.shape[0]-1, number_of_time_steps, dtype=int)  # get the indicies of the time steps
npr_trimmed = npr_trimmed[row_indicies, :]  # select the rows of interest
t_trimmed = t[row_indicies]  # select the time steps of interest
t_trimmed = t_trimmed.flatten()  # flatten t_trimmed to be a 1D array

npr_trimmed = np.abs(npr_trimmed)  # take the absolute value of npr_trimmed
# from this section, we get "species_interest", "t_trimmed", and "npr_trimmed"


############################
## plot the contour
############################

##################################################################################
# Create a 3D bar plot
# Setup 3D plot
fig = plt.figure(figsize=(10, 6))
ax = fig.add_subplot(111, projection='3d')

# Positions
x_indices = np.arange(len(species_interest))
y_indices = np.arange(len(t_trimmed))
_xx, _yy = np.meshgrid(x_indices, y_indices)
x, y = _xx.ravel(), _yy.ravel()
z = np.zeros_like(x)
dz = npr_trimmed.ravel()
dx = dy = 0.8

# Normalize values for colormap
norm = Normalize(vmin=dz.min(), vmax=dz.max())
colors = cm.plasma(norm(dz))  # Choose a colormap (e.g., viridis, plasma, etc.)

# Plot colored bars
ax.bar3d(x, y, z, dx, dy, dz, color=colors, shade=True)

# Tick labels
ax.set_xticks(x_indices + 0.4)
ax.set_xticklabels(species_interest)
ax.set_yticks(y_indices)
ax.set_yticklabels([f"{ti:.1e}" for ti in t_trimmed])

# Axis labels
ax.set_xlabel("Species")
ax.set_ylabel("Time")
ax.set_zlabel("net production rate (abs) [kmol/m^2/s]")

# Color bar
mappable = cm.ScalarMappable(norm=norm, cmap=cm.viridis)
mappable.set_array([])
fig.colorbar(mappable, ax=ax, label="mu value")

plt.title("3D Bar Plot of npr (abs) vs Species and Time")
# plt.tight_layout()
plt.show()
##################################################################################

##################################################################################
# ## Create a 3D log scale plot

# # avoid log(0)
# safe_matrix = np.clip(mu_trimmed, 1e-4, None) # avoid log(0)
# mu_trimmed_log = np.log10(safe_matrix)

# # Create a 3D bar plot
# fig = plt.figure(figsize=(10, 6))
# ax = fig.add_subplot(111, projection='3d')

# # Grid positions
# x_indices = np.arange(len(species_interest))
# y_indices = np.arange(len(t_trimmed))
# _xx, _yy = np.meshgrid(x_indices, y_indices)
# x, y = _xx.ravel(), _yy.ravel()
# z = np.zeros_like(x)
# dz = mu_trimmed_log.ravel()
# z = np.full_like(dz, dz.min())  # bottom starts from lowest log10(mu)
# dx = dy = 0.8

# # Colormap based on log values
# norm = Normalize(vmin=dz.min(), vmax=dz.max())
# colors = cm.magma(norm(dz))  # or cm.inferno, cm.viridis, etc.

# # Plot 3D bars
# ax.bar3d(x, y, z, dx, dy, dz, color=colors, shade=True)

# # Tick labels
# ax.set_xticks(x_indices + 0.4)
# ax.set_xticklabels(species_interest)
# ax.set_yticks(y_indices)
# ax.set_yticklabels([f"{ti:.1e}" for ti in t_trimmed])

# # Axis labels
# ax.set_xlabel("Species")
# ax.set_ylabel("Time")
# ax.set_zlabel("log10(mu)")

# # Color bar
# mappable = cm.ScalarMappable(norm=norm, cmap=cm.magma)
# mappable.set_array([])
# fig.colorbar(mappable, ax=ax, label="log10(mu)")

# plt.title("3D Bar Plot of log10(mu) vs Species and Time")
# plt.tight_layout()
# plt.show()
##################################################################################
