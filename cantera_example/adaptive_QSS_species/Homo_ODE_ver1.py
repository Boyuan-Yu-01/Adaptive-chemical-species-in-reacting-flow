import cantera as ct
import numpy as np
import scipy.integrate
import pandas as pd
import multiprocessing as mp

class Homo_Reaction_ODE:
    """ This class returns a system of ODEs for different reactor_types:
        'reactor_types' includes:
            const_V:     constant volume, adiabatic wall
            const_P:     constant pressure, adiabatic wall
            constant_TP, constant temperature and temperature """
            
    def __init__(self, gas, reactor_type):
        self.gas = gas
        self.reactor_type = reactor_type
        if self.reactor_type.lower() == "const_v":
            self.sys = lambda t,y: self.const_V_ODE(t, y)
            self.rho,_ = self.gas.DP
        elif self.reactor_type.lower() == "const_p":
            self.sys = lambda t,y: self.const_P_ODE(t, y, energy='on')
            self.P = self.gas.P
        elif self.reactor_type.lower() == "const_tp":
            self.sys = lambda t,y: self.const_P_ODE(t, y, energy='off')
            self.T, self.P = self.gas.TP
        else:
            raise ValueError(f"Unknown reactor type: '{reactor_type}'")
        
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
    
    def return_ODEs(self):
        return self.sys
    
    def reaction_progress(self, dt, t_end, t_start=0.0, method='bdf'):
        """Integrate the ODE system from t_start to t_end with time step dt
           Choose reactor type: 'const_V', 'const_P', or 'const_TP'
           
           It adds a 'self.states' attribute to the class, which is a SolutionArray that stores the states at each time step.
           """
        # define the ODE solver
        solver = scipy.integrate.ode(self.sys)
        solver.set_integrator('vode', method=method,with_jacobian=True)
        y0 = np.hstack((self.gas.T, self.gas.Y))
        solver.set_initial_value(y0, t_start)
        
        self.states = ct.SolutionArray(self.gas, 1, extra={'t':[t_start]})
        
        while solver.successful() and solver.t < t_end:
            solver.integrate(solver.t + dt)
            if self.reactor_type.lower() == "const_v":
                self.gas.TDY = solver.y[0], self.rho, solver.y[1:]
                
            elif self.reactor_type.lower() == "const_p":
                self.gas.TPY = solver.y[0], self.P, solver.y[1:]
                
            elif self.reactor_type.lower() == "const_tp":
                self.gas.TPY = solver.y[0], self.P, solver.y[1:]
            self.states.append(self.gas.state, t=solver.t)
        
        return self.states
                
                
###############################################################
## calculate the importance matrix using parallel processing ##
###############################################################
def importance_matrix(state0, state1, scheme, reactor_type, perturb_factor=1.01, num_cpu = mp.cpu_count()-1):
    """ Calculate the importance matrix using parallel processing."""
    
    size = np.array(state1.species_names).size   # size of m (number of species)
    matrix = np.zeros((size, size))             # size of m by m (initialize the importance matrix)
    
    # convert state0 and state1 into NumPy-compatible data types for parallel processing
    T0, P0, X0 = state0.TPX
    T1, P1, X1 = state1.TPX
    state0_data = [T0, P0, X0]
    state1_data = [T1, P1, X1]
    
    # Use multiprocessing to execute the perturbation
    num_cpu = min(mp.cpu_count(), num_cpu)  # Ensure we don't use more CPUs than available
    args = [(j, state0.t, state1.t, state0_data, state1_data, scheme, reactor_type, perturb_factor) for j in range(size)]
    with mp.Pool(processes=num_cpu) as pool:
        results = pool.starmap(compute_column, args)
        
    for j, jth_col in results:
        matrix[:,j] = jth_col
    return matrix
        
        
def compute_column(j, t0, t1, state0_data, state1_data, scheme, reactor_type, perturb_factor):
    """ Compute a single column of the importance matrix using perturbation method.
        parameters:
            i:                  the index of the column to compute and also the index of the species to perturb
            t0:                 t at state0
            t1:                 t at state1
            state0_data:        (T0, P0, X0), will be used to redeine state0
            state1_data:        (T1, P1, X1), will be used to redeine state1
            scheme:             the mechanism (e.g. "FFCM2.yaml")
            perturb_factor:     factor to perturb the species concentration)"""
    # Placeholder implementation
    gas0 = ct.Solution(scheme)
    gas1 = ct.Solution(scheme)
    gas_p = ct.Solution(scheme)  # Initialize the perturbed gas object
    gas0.TPX = state0_data[0], state0_data[1], state0_data[2]   # restore state0 from TPX in state0_data: type: cantera.Solution
    gas1.TPX = state1_data[0], state1_data[1], state1_data[2]   # restore state1 from TPX in state1_data: type: cantera.Solution

    # construct the perturbed gas object
    concentrations = gas0.concentrations
    concentrations_p = concentrations.copy()
    concentrations_p[j] *= perturb_factor  # Perturb the j-th species concentration
    X = concentrations_p / np.sum(concentrations_p)  # normalize the perturbed concentrations
    P_p = state0_data[1] * np.sum(concentrations_p) / np.sum(concentrations)  # adjust pressure to keep the total moles constant
    gas_p.TPX = state0_data[0], P_p, X
    
    # Integrate 'gas_p' by one step
    dt_max = t1 - t0
    pert_obj = Homo_Reaction_ODE(gas=gas_p, reactor_type=reactor_type)  # create an instance of Homo_Reaction_ODE with perturbed gas object
    gas1_p = pert_obj.reaction_progress(dt=dt_max, t_end=t1, t_start=t0, method='bdf')[-1]  # advance gas_p by one step to yield 'gas1_p': type: cantera.Solution
    with np.errstate(divide='ignore', invalid='ignore'):
        jth_col = (gas1_p.concentrations - gas1.concentrations) / (gas_p.concentrations - gas0.concentrations) * gas0.net_production_rates
    return j, jth_col
    

## set up initial gas composition
scheme = "FFCM2.yaml"
gas = ct.Solution(scheme)
T = 2000
P = 1 * ct.one_atm
X = "CH4:1, O2:2"
gas.TPX = T, P, X
reactor_type = "const_P"

## set up the t constraints for the simulation
dt_max = 1e-8
t_end = 3e-5

obj = Homo_Reaction_ODE(gas, reactor_type)
states = obj.reaction_progress(dt=dt_max, t_end=t_end, t_start=0.0, method='bdf')

# state_0 = states[1500]
# state_1 = states[1501]

# matrix = importance_matrix(state_0, state_1, scheme, reactor_type)

# df = pd.DataFrame(matrix, columns=obj.gas.species_names, index=obj.gas.species_names)
# df.index.name = "ID"
# df.to_csv("test_P.csv")



    
 
    

    
        