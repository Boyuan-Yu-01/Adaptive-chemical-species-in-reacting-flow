import cantera as ct
import numpy as np
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
scheme = "FFCM2.yaml"
# scheme = "FFCM1_21.yaml"

def const_vol_adia(gas, dt_max, t_end, output_file):
    '''this function simulates a constant pressure homogeneous reactor with adiabatic wall
       this function returns the mole fraction of each species at each time step.'''
    r = ct.IdealGasMoleReactor(gas)
    sim = ct.ReactorNet([r])
    sim.verbose = True
    states = ct.SolutionArray(gas)
    t = []  # initialise the time array

    while sim.time < t_end:
        sim.advance(sim.time + dt_max)
        # states.append(r.thermo.state, t=sim.time)
        states.append(r.thermo.state)
        t.append(sim.time)
    
    # extract information that later will be put into the output file
    t = np.array(t).reshape(-1, 1)  # convert to a column vector
    P = states.P.reshape(-1, 1)  # convert to a column vector
    T = states.T.reshape(-1, 1)  # convert to a column vector
    rho = states.D.reshape(-1, 1)  # convert to a column vector
    species = states.species_names
    titles = np.hstack((['t [s]', 'P [Pa]', 'T [K]', 'rho [kg/m^3]'], species))
    data = np.hstack((t, P, T, rho, states.X))
    
    # conclude data into a pandas dataframe
    df = pd.DataFrame(data, columns=titles)
    df.to_csv(output_file, index=False)
    
    return states    
  
    
# set up the gas object
gas = ct.Solution(scheme)
T = 2000
P = 1 * ct.one_atm
X = "CH4:1, O2:2"
gas.TPX = T, P, X

# set up the t constraints for the simulation and output file
dt_max = 1e-8
t_end = 2e-3
# t_end = 1e-7    # for testing
output_file = "const_vol_adia_exp.csv"

# run the simulation 
states = const_vol_adia(gas, dt_max, t_end, output_file)

