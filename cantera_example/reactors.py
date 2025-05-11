import cantera as ct
import numpy as np
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

class Reactor:
    def __init__(self, gas, dt_max, t_end, output_file, mode=None):
        self.gas = gas
        self.dt_max = dt_max
        self.t_end = t_end
        self.output_file = output_file
        self.mode = mode
        
        # dispatcher: if mode is defined, use it to select the function to call
        self.dispatch = {
            "const_vol_adia": self.const_vol_adia,
            "const_pres_adia": self.const_pres_adia,
            "const_TP_adia": self.const_TP_adia
        }
        
    def run(self, mode=None):
        mode_to_run = mode or self.mode    # verbose according to chatGPT
        if mode_to_run not in self.dispatch:
            raise ValueError(f"Unknown reactor mode: '{mode_to_run}'")
        return self.dispatch[mode_to_run]()
    
    def const_TP_adia(self):
        '''this function simulates a constant temperature&pressure homogeneous reactor with adiabatic wall
        this function returns the mole fraction of each species at each time step.'''
        
        # grab parameters from "__init__"
        gas = self.gas
        dt_max = self.dt_max
        t_end = self.t_end
        output_file = self.output_file
        
        # setu up the reactor
        r = ct.IdealGasConstPressureMoleReactor(gas, energy="off", name="isothermal_reactor")
        sim = ct.ReactorNet([r])
        sim.verbose = True
        states = ct.SolutionArray(gas)
        t = []  # initialise the time array
        P = []  # initialise the pressure array

        # reaction progression w.r.t. time
        while sim.time < t_end:
            sim.advance(sim.time + dt_max)
            # states.append(r.thermo.state, t=sim.time)
            states.append(r.thermo.state)
            t.append(sim.time)
            P.append(r.thermo.P)
        
        # extract information that later will be put into the output file
        t = np.array(t).reshape(-1, 1)  # convert to a column vector
        P = np.array(P).reshape(-1, 1)  # convert to a column vector
        T = states.T.reshape(-1, 1)  # convert to a column vector
        rho = states.D.reshape(-1, 1)  # convert to a column vector
        species = states.species_names
        titles = np.hstack((['t [s]', 'P [Pa]', 'T [K]', 'rho [kg/m^3]'], species))
        data = np.hstack((t, P, T, rho, states.X))
        
        # conclude data into a pandas dataframe
        df = pd.DataFrame(data, columns=titles)
        df.to_csv(output_file, index=False)
        
        return states    
    
    def const_pres_adia(self):
        '''this function simulates a constant pressure homogeneous reactor with adiabatic wall
        this function returns the mole fraction of each species at each time step.'''
        
        # grab parameters from "__init__"
        gas = self.gas
        dt_max = self.dt_max
        t_end = self.t_end
        output_file = self.output_file
        
        # setu up the reactor
        r = ct.IdealGasConstPressureMoleReactor(gas)
        sim = ct.ReactorNet([r])
        sim.verbose = True
        states = ct.SolutionArray(gas)
        t = []  # initialise the time array
        P = []  # initialise the pressure array
        
        # reaction progression w.r.t. time
        while sim.time < t_end:
            sim.advance(sim.time + dt_max)
            # states.append(r.thermo.state, t=sim.time)
            states.append(r.thermo.state)
            t.append(sim.time)
            P.append(r.thermo.P)
        
        # extract information that later will be put into the output file
        t = np.array(t).reshape(-1, 1)  # convert to a column vector
        P = np.array(P).reshape(-1, 1)  # convert to a column vector
        T = states.T.reshape(-1, 1)  # convert to a column vector
        rho = states.D.reshape(-1, 1)  # convert to a column vector
        species = states.species_names
        titles = np.hstack((['t [s]', 'P [Pa]', 'T [K]', 'rho [kg/m^3]'], species))
        data = np.hstack((t, P, T, rho, states.X))
        
        # conclude data into a pandas dataframe
        df = pd.DataFrame(data, columns=titles)
        df.to_csv(output_file, index=False)
        
        return states    
    
    def const_vol_adia(self):
        '''this function simulates a constant volume homogeneous reactor with adiabatic wall
        this function returns the mole fraction of each species at each time step.'''
        
        # grab parameters from "__init__"
        gas = self.gas
        dt_max = self.dt_max
        t_end = self.t_end
        output_file = self.output_file
        
        # setu up the reactor
        r = ct.IdealGasMoleReactor(gas)
        sim = ct.ReactorNet([r])
        sim.verbose = True
        states = ct.SolutionArray(gas)
        t = []  # initialise the time array
        P = []  # initialise the pressure array
        
        # reaction progression w.r.t. time
        while sim.time < t_end:
            sim.advance(sim.time + dt_max)
            # states.append(r.thermo.state, t=sim.time)
            states.append(r.thermo.state)
            t.append(sim.time)
            P.append(r.thermo.P)
        
        # extract information that later will be put into the output file
        t = np.array(t).reshape(-1, 1)  # convert to a column vector
        P = np.array(P).reshape(-1, 1)  # convert to a column vector
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
scheme = "FFCM2.yaml"
gas = ct.Solution(scheme)
T = 2000
P = 1 * ct.one_atm
X = "CH4:1, O2:2"
gas.TPX = T, P, X

# set up the t constraints for the simulation and output file
dt_max = 1e-8
t_end = 2e-3
# t_end = 1e-7    # for testing
output_file = "class_test.csv"

# run the simulation

## Method 1: 
# sim1 = Reactor(gas=gas, dt_max=dt_max, t_end=t_end, output_file=output_file)
# sim1.run(mode="const_vol_adia")
## Method 2:
sim2 = Reactor(gas=gas, dt_max=dt_max, t_end=t_end, output_file=output_file, mode="const_vol_adia")
sim2.run()