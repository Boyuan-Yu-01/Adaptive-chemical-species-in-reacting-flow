import cantera as ct
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

class Homo_Reactor:
    def __init__(self, gas, dt_max, t_end, mode=None, csv_output=None):
        self.gas = gas
        self.dt_max = dt_max
        self.t_end = t_end
        self.mode = mode
        self.csv_name = csv_output
        self.reaction_info = {}
        
        # dispatcher: if mode is defined, use it to select the function to call
        self.dispatch = {
            "const_V": self.const_V,
            "const_P": self.const_P,
            "const_TP": self.const_TP,
        }
        
    def run(self, mode=None):
        mode_to_run = mode or self.mode    # verbose according to chatGPT
        if mode_to_run not in self.dispatch:
            raise ValueError(f"Unknown reactor mode: '{mode_to_run}'")
        return self.dispatch[mode_to_run]()
    
    def const_TP(self):
        '''this function simulates a constant temperature&pressure homogeneous reactor with adiabatic wall
        this function returns the mole fraction of each species at each time step.'''
        
        # grab parameters from "__init__"
        gas = self.gas
        dt_max = self.dt_max
        t_end = self.t_end
        output_file = self.csv_name
        
        # setu up the reactor
        r = ct.IdealGasConstPressureMoleReactor(gas, energy="off", name="isothermal_reactor")
        sim = ct.ReactorNet([r])
        sim.verbose = True
        states = ct.SolutionArray(gas)
        t = [0]  # initialise the time array
        P_ini = gas.P
        T_ini = gas.T
        rho_ini = gas.density
        net_production_rates_ini = gas.net_production_rates
        concentrations_ini = gas.concentrations

        # reaction progression w.r.t. time
        while sim.time < t_end:
            sim.advance(sim.time + dt_max)
            # states.append(r.thermo.state, t=sim.time)
            states.append(r.thermo.state)
            t.append(sim.time)
        
        # extract information that later will be put into the output file
        t = np.array(t).reshape(-1, 1)  # conlumn vector: m by 1
        P = states.P
        P = np.insert(P, 0, P_ini)
        P = P.reshape(-1, 1)  # column vector: m by 1
        T = states.T
        T = np.insert(T, 0, T_ini)
        T = T.reshape(-1, 1)  # column vector: m by 1
        rho = states.D
        rho = np.insert(rho, 0, rho_ini)
        rho = rho.reshape(-1, 1)  # column vector: m by 1
        net_production_rates = np.vstack((net_production_rates_ini, states.net_production_rates))
        concentrations = np.vstack((concentrations_ini, states.concentrations))
        species = np.array(states.species_names)
        result_dic = {
            "t": t,     # m by 1
            "P": P,     # m by 1
            "T": T,     # m by 1
            "rho": rho, # m by 1
            "species": species,     # 1 by n
            "net_production_rates": net_production_rates,   # m by n
            "concentrations": concentrations,               # m by n
        }
        
        # output concentration or mole fraction into a csv file
        if self.csv_name:
            species = np.char.add(species, " [kmol/m^3]")
            titles = np.hstack((['t [s]', 'P [Pa]', 'T [K]', 'rho [kg/m^3]'], species))
            data = np.hstack((t, P, T, rho, concentrations))
            # conclude data into a pandas dataframe
            df = pd.DataFrame(data, columns=titles)
            df.to_csv(output_file, index=False)
        else:
            print("programme continues without output csv file")

        self.reaction_info  = result_dic
    
    def const_P(self):
        '''this function simulates a constant pressure homogeneous reactor with adiabatic wall
        this function returns the mole fraction of each species at each time step.'''
        
        # grab parameters from "__init__"
        gas = self.gas
        dt_max = self.dt_max
        t_end = self.t_end
        output_file = self.csv_name
        
        # setu up the reactor
        r = ct.IdealGasConstPressureMoleReactor(gas)
        sim = ct.ReactorNet([r])
        sim.verbose = True
        states = ct.SolutionArray(gas)
        t = [0]  # initialise the time array
        P_ini = gas.P
        T_ini = gas.T
        rho_ini = gas.density
        net_production_rates_ini = gas.net_production_rates
        concentrations_ini = gas.concentrations
        
        # reaction progression w.r.t. time
        while sim.time < t_end:
            sim.advance(sim.time + dt_max)
            states.append(r.thermo.state)
            t.append(sim.time)
        
        # extract information that later will be put into the output file
        t = np.array(t).reshape(-1, 1)  # conlumn vector: m by 1
        P = states.P
        P = np.insert(P, 0, P_ini)
        P = P.reshape(-1, 1)  # column vector: m by 1
        T = states.T
        T = np.insert(T, 0, T_ini)
        T = T.reshape(-1, 1)  # column vector: m by 1
        rho = states.D
        rho = np.insert(rho, 0, rho_ini)
        rho = rho.reshape(-1, 1)  # column vector: m by 1
        net_production_rates = np.vstack((net_production_rates_ini, states.net_production_rates))
        concentrations = np.vstack((concentrations_ini, states.concentrations))
        species = np.array(states.species_names)
        result_dic = {
            "t": t,     # m by 1
            "P": P,     # m by 1
            "T": T,     # m by 1
            "rho": rho, # m by 1
            "species": species,     # 1 by n
            "net_production_rates": net_production_rates,   # m by n
            "concentrations": concentrations,               # m by n
        }
        
        # output concentration or mole fraction into a csv file
        if self.csv_name:
            species = np.char.add(species, " [kmol/m^3]")
            titles = np.hstack((['t [s]', 'P [Pa]', 'T [K]', 'rho [kg/m^3]'], species))
            data = np.hstack((t, P, T, rho, concentrations))
            # conclude data into a pandas dataframe
            df = pd.DataFrame(data, columns=titles)
            df.to_csv(output_file, index=False)
        else:
            print("programme continues without output csv file")

        self.reaction_info  = result_dic
    
    def const_V(self):
        '''this function simulates a constant volume homogeneous reactor with adiabatic wall
        this function returns the mole fraction of each species at each time step.'''
        
        # grab parameters from "__init__"
        gas = self.gas
        dt_max = self.dt_max
        t_end = self.t_end
        output_file = self.csv_name
        
        # setu up the reactor
        r = ct.IdealGasMoleReactor(gas)
        sim = ct.ReactorNet([r])
        sim.verbose = True
        states = ct.SolutionArray(gas)
        t = [0]  # initialise the time array
        P_ini = gas.P
        T_ini = gas.T
        rho_ini = gas.density
        net_production_rates_ini = gas.net_production_rates
        concentrations_ini = gas.concentrations
        
        # reaction progression w.r.t. time
        while sim.time < t_end:
            sim.advance(sim.time + dt_max)
            states.append(r.thermo.state)
            t.append(sim.time)
        
        # extract information that later will be put into the output file
        t = np.array(t).reshape(-1, 1)  # conlumn vector: m by 1
        P = states.P
        P = np.insert(P, 0, P_ini)
        P = P.reshape(-1, 1)  # column vector: m by 1
        T = states.T
        T = np.insert(T, 0, T_ini)
        T = T.reshape(-1, 1)  # column vector: m by 1
        rho = states.D
        rho = np.insert(rho, 0, rho_ini)
        rho = rho.reshape(-1, 1)  # column vector: m by 1
        net_production_rates = np.vstack((net_production_rates_ini, states.net_production_rates))
        concentrations = np.vstack((concentrations_ini, states.concentrations))
        species = np.array(states.species_names)
        result_dic = {
            "t": t,     # m by 1
            "P": P,     # m by 1
            "T": T,     # m by 1
            "rho": rho, # m by 1
            "species": species,     # 1 by n
            "net_production_rates": net_production_rates,   # m by n
            "concentrations": concentrations,               # m by n
        }
        
        # output concentration or mole fraction into a csv file
        if self.csv_name:
            species = np.char.add(species, " [kmol/m^3]")
            titles = np.hstack((['t [s]', 'P [Pa]', 'T [K]', 'rho [kg/m^3]'], species))
            data = np.hstack((t, P, T, rho, concentrations))
            # conclude data into a pandas dataframe
            df = pd.DataFrame(data, columns=titles)
            df.to_csv(output_file, index=False)
        else:
            print("programme continues without output csv file")

        self.reaction_info  = result_dic
    
    # set up the gas object
scheme = "FFCM2.yaml"
# scheme = "FFCM1_21.yaml"
gas = ct.Solution(scheme)
T = 2000
P = 1 * ct.one_atm
X = "CH4:1, O2:2"
gas.TPX = T, P, X

# set up the t constraints for the simulation and output file
dt_max = 1e-8
t_end = 3e-5
# t_end = 1e-7    # for testing
output_file = "test_TP.csv"

# run the simulation

sim1 = Homo_Reactor(gas=gas, dt_max=dt_max, t_end=t_end, mode="const_P")
sim1.run()
result = sim1.reaction_info