import cantera as ct
import numpy as np
import matplotlib.pyplot as plt
import scipy.integrate
import pandas as pd

class Homo_Reaction_ODE:
    def __init__(self, gas):
        self.gas = gas
    
    def const_V_ODE(self, t, y):
        """The ODE function to solve constant volume homogeneous reaction"""
        # State vector is [T, Y_1, Y_2, ... Y_K]
        self.gas.set_unnormalized_mass_fractions(y[1:])
        self.gas.TD = y[0], self.rho
        
        # reaction equations:
        wdot = self.gas.net_production_rates
        dTdt = - (np.dot(self.gas.partial_molar_int_energies, wdot) /
                  (self.rho * self.gas.cv))
        dYdt = wdot * self.gas.molecular_weights / self.rho
        return np.hstack((dTdt, dYdt))
    
    def const_P_ODE(self, t, y, energy="on"):
        """The ODE function to solve constant pressure homogeneous reaction.
           The 'energy' input decide if it is an isothermal reactor ('off') or an adiabatic reactor ('on')"""
        # State vector is [T, Y_1, Y_2, ... Y_K]
        self.gas.set_unnormalized_mass_fractions(y[1:])
        self.gas.TP = y[0], self.P
        rho = self.gas.density
        
        # reaction equations:
        wdot = self.gas.net_production_rates
        if energy.lower()=="off":
            dTdt = 0
        else:    
            dTdt = - (np.dot(self.gas.partial_molar_enthalpies, wdot) /
                  (rho * self.gas.cp))
        dYdt = wdot * self.gas.molecular_weights / rho
        return np.hstack((dTdt, dYdt))
    
    def reaction_progress(self, reactor, dt, t_end, t_start=0.0, method='bdf',energy='on'):
        """Integrate the ODE system from t_start to t_end with time step dt
           Choose reactor type: 'const_V' or 'const_P'
           """
        # choose equation system to solve
        if reactor.lower() == "const_v":
            sys = self.const_V_ODE
            self.rho, _ = self.gas.DP
        elif reactor.lower() == "const_p":
            sys = lambda t, y: self.const_P_ODE(t, y, energy=energy)
            self.P = self.gas.P
        
        # set up the ODE solver
        solver = scipy.integrate.ode(sys)
        solver.set_integrator('vode', method=method, with_jacobian=True)
        y0 = np.hstack((self.gas.T, self.gas.Y))
        solver.set_initial_value(y0, t_start)
        
        # prepare to store results
        states = ct.SolutionArray(self.gas, 1, extra={'t':[t_start]})
        while solver.successful() and solver.t < t_end:
            solver.integrate(solver.t + dt)
            if reactor.lower() == "const_v":
                self.gas.TDY = solver.y[0], self.rho, solver.y[1:]
            elif reactor.lower() == "const_p":
                self.gas.TPY = solver.y[0], self.P, solver.y[1:]
            states.append(self.gas.state, t=solver.t)
            
        return states
        
        
            

class Homo_Reactor:
    def __init__(self, gas, dt_max, t_end, t_start=0.0, mode=None, csv_output=None, output_species=[]):
        self.gas = gas
        self.dt_max = dt_max
        self.t_start = t_start
        self.t_end = t_end
        self.mode = mode
        self.csv_name = csv_output
        self.output_species = output_species
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
        t_start = self.t_start
        t_end = self.t_end
        
        # reaction progress:
        r = Homo_Reaction_ODE(gas)
        states = r.reaction_progress(reactor="const_P", dt=dt_max, t_start=t_start, t_end=t_end, energy='off')
        self.states = states
        
        # extract information that later will be put into the dictionary file
        t = np.array(states.t).reshape(-1, 1)  # conlumn vector: m by 1
        P = np.array(states.P).reshape(-1, 1)  # column vector: m by 1
        T = np.array(states.T).reshape(-1, 1)  # column vector: m by 1
        rho = np.array(states.D).reshape(-1, 1)  # column vector: m by 1
        net_production_rates = np.array(states.net_production_rates)
        concentrations = np.array(states.concentrations)
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
            self.csv_output(csv_name=self.csv_name,
                            species_of_interest=self.output_species)
        else:
            print("programme continues without output csv file")

        self.reaction_info  = result_dic
          # store states for later use, e.g., csv output
    
    def const_P(self):
        '''this function simulates a constant pressure homogeneous reactor with adiabatic wall
        this function returns the mole fraction of each species at each time step.'''
        
        # grab parameters from "__init__"
        gas = self.gas
        dt_max = self.dt_max
        t_start = self.t_start
        t_end = self.t_end
        
        #  reaction progress:
        r = Homo_Reaction_ODE(gas)
        states = r.reaction_progress(reactor="const_P", dt=dt_max,t_start=t_start, t_end=t_end)
        self.states = states  # store states for later use, e.g., csv output
        
        # extract information that later will be put into the output file
        t = np.array(states.t).reshape(-1, 1)  # conlumn vector: m by 1
        P = np.array(states.P).reshape(-1, 1)  # column vector: m by 1
        T = np.array(states.T).reshape(-1, 1)  # column vector: m by 1
        rho = np.array(states.D).reshape(-1, 1)  # column vector: m by 1
        net_production_rates = np.array(states.net_production_rates)
        concentrations = np.array(states.concentrations)
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
            self.csv_output(csv_name=self.csv_name,
                            species_of_interest=self.output_species)
        else:
            print("programme continues without output csv file")
            
        self.reaction_info  = result_dic
        
    def const_V(self):
        '''this function simulates a constant volume homogeneous reactor with adiabatic wall
        this function returns the mole fraction of each species at each time step.'''
        
        # grab parameters from "__init__"
        gas = self.gas
        dt_max = self.dt_max
        t_start = self.t_start
        t_end = self.t_end
        
        # reaction progress:
        r = Homo_Reaction_ODE(gas)
        states = r.reaction_progress(reactor='const_V', dt=dt_max, t_start=t_start, t_end=t_end)
        self.states = states  # store states for later use, e.g., csv output
        # extract information that later will be put into the output file
        t = np.array(states.t).reshape(-1, 1)  # conlumn vector: m by 1
        P = np.array(states.P).reshape(-1, 1)  # column vector: m by 1
        T = np.array(states.T).reshape(-1, 1)  # column vector: m by 1
        rho = np.array(states.D).reshape(-1, 1)  # column vector: m by 1
        net_production_rates = np.array(states.net_production_rates)
        concentrations = np.array(states.concentrations)
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
            self.csv_output(csv_name=self.csv_name,
                            species_of_interest=self.output_species)
        else:
            print("programme continues without output csv file")

        self.reaction_info  = result_dic
    
    def csv_output(self, csv_name=None, species_of_interest=None):
        """This function outputs the reaction information into a csv file.
           If species_of_interest is provided, it will only output the specified species."""
        if csv_name is None and self.csv_name is None:
            raise ValueError("No csv file name provided for output.")
        elif csv_name is None:
            csv_name = self.csv_name
        
        if species_of_interest is not None:
            soi_idx = [list(self.states.species_names).index(item) for item in species_of_interest]
            concentrations_output = np.array(self.states.concentrations)[:, soi_idx]
            species_output = np.char.add(species_of_interest, " [kmol/m^3]")
        else:
            concentrations_output = np.array(self.states.concentrations)
            species_output = np.array(self.states.species_names)
        # prepare the data for output
        titles = np.hstack((['t [s]', 'P [Pa]', 'T [K]', 'rho [kg/m^3]'], species_output))
        t = np.array(self.states.t).reshape(-1, 1)
        P = np.array(self.states.P).reshape(-1, 1)
        T = np.array(self.states.T).reshape(-1, 1)
        rho = np.array(self.states.D).reshape(-1, 1)
        data = np.hstack((t, P, T, rho, concentrations_output))
        # conclude data into a pandas dataframe
        df = pd.DataFrame(data, columns=titles)
        # output to csv file
        df.to_csv(csv_name, index=False)
    
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
output_file = "test.csv"

# run the simulation

sim1 = Homo_Reactor(gas=gas, dt_max=dt_max, t_end=t_end, mode="const_V", csv_output=output_file, output_species=['CH4','CO2'])
sim1.run()
result = sim1.reaction_info

