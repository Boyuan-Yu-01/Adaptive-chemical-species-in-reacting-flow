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
        
    def const_V_ODE(self, t, y, switch_off_species=None):
        """The ODE function to solve constant volume homogeneous reaction"""
        # State vector is [T, Y_1, Y_2, ... Y_K]
        self.gas.set_unnormalized_mass_fractions(y[1:])
        self.gas.TD = y[0], self.rho
        
        # reaction equations:
        wdot = self.gas.net_production_rates
        if switch_off_species is not None:
            wdot[switch_off_species] = 0  # handle switch off species: when there are switch off species, the n.p.r. of these species is set to be zero.
        
        dTdt = - (np.dot(self.gas.partial_molar_int_energies, wdot) /
                  (self.rho * self.gas.cv))
        dYdt = wdot * self.gas.molecular_weights / self.rho
        return np.hstack((dTdt, dYdt))
    
    def const_P_ODE(self, t, y, energy="on", switch_off_species=None):
        """The ODE function to solve constant pressure homogeneous reaction.
           The 'energy' input decide if it is an isothermal reactor ('off') or an adiabatic reactor ('on')"""
        # State vector is [T, Y_1, Y_2, ... Y_K]
        self.gas.set_unnormalized_mass_fractions(y[1:])
        self.gas.TP = y[0], self.P
        rho = self.gas.density
        
        # reaction equations:
        wdot = self.gas.net_production_rates
        if switch_off_species is not None: # handle switch off species: when there are switch off species, the n.p.r. of these species is set to be zero.
            wdot[switch_off_species] = 0
            
        if energy.lower()=="off":
            dTdt = 0
        else:    
            dTdt = - (np.dot(self.gas.partial_molar_enthalpies, wdot) /
                  (rho * self.gas.cp))
        dYdt = wdot * self.gas.molecular_weights / rho
        return np.hstack((dTdt, dYdt))
    
    def return_ODEs(self):
        return self.sys
    
    
    def reaction_progress(self, dt, t_end, t_start=0.0, method='bdf', switch_off_species=None):
        """Integrate the ODE system from t_start to t_end with time step dt
           Choose reactor type: 'const_V', 'const_P', or 'const_TP'
           
           It adds a 'self.states' attribute to the class, which is a SolutionArray that stores the states at each time step.
           """
        # define the ODE solver
        
        # step 1: check if there are switch off species
        if switch_off_species is None:
            solver = scipy.integrate.ode(self.sys)
        else:
            # when there are switch off species, the ODE system needs to be redefined, s.t. the n.p.r. of the switch off species is zero. However, these new defined systems ARE NOT CLASS LEVEL ATTRIBUTES.
            if self.reactor_type.lower() == "const_v":
                sys = lambda t,y: self.const_V_ODE(t, y, switch_off_species=switch_off_species)
                solver = scipy.integrate.ode(sys)
            elif self.reactor_type.lower() == "const_p":
                sys = lambda t,y: self.const_P_ODE(t, y, switch_off_species=switch_off_species, energy='on')
                solver = scipy.integrate.ode(sys)
            elif self.reactor_type.lower() == "const_tp":
                sys = lambda t,y: self.const_P_ODE(t, y, switch_off_species=switch_off_species, energy='off')
                solver = scipy.integrate.ode(sys)
            
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
    
##########################################################
## Reaction Forward in an Adaptive Chemical Species way ##
##########################################################
class Adaptive_Chemical_Reaction:
    """ This class progress reaction in an adaptive way:
        Based on states at t(0) and t(-1), this class decides species to be 'switched off' and progress for n steps.
        After n steps, this class will evaluate the result and decide whether 
            1) some species can not be 'switched off' and go back
        or  2) keep going """
    
    def __init__(self, gas, scheme, t_start, t_end, dt_max, reactor_type, epsilon=1e-3, step = 300):
        self.gas = gas
        self.scheme = scheme
        self.t_start = t_start
        self.t_end = t_end
        self.dt_max = dt_max
        self.reactor_type = reactor_type
        self.reactor_ODE = Homo_Reaction_ODE(gas, reactor_type)
        self.states = ct.SolutionArray(self.gas, 1, extra={'t':[t_start]})
        self.epsilon = epsilon  # This is a hyper-parameter. It desceibes after the reduced reaction progress for n steps, the abs. rel. error should be no more than epsilon
        self.step = step
    
    def adaptively_progress (self, concentration_threshold=1e-5, matrix_threshold=0.01):
        """ this function progress the reaction adaptively"""
        ## step 1: reaction progress for two steps, then store it to 'self.states'
        ## step 2: pick up candidates using policy I: Species that assumed to be QSS in n step interval should have relative error no more than "epsilon"
        ## step 3: applying policy II to choose from the candidates, and decide the steps that we are going to advance within this interval
        ## step 4: advance the reduced reaction for n steps
        ## step 5: check if previous steps are valid: if not, remove invalid reducable species, and go back to step 3
        while self.states.t[-1] < self.t_end:
            # step1
            states_step1 = self.reactor_ODE.reaction_progress(dt=self.dt_max, t_start=self.states.t[-1], t_end=np.min(self.states.t[-1]+self.dt_max, self.t_end), method='bdf')
            self.states.append(states_step1[1:])
            
            # step2  
            state_0 = self.states[-2]
            state_1 = self.states[-1]
            
            concentrations_1 = state_1.concentrations
            scs = np.where(concentrations_1 <= concentration_threshold)[0]  # small concentration species
            scs_w = state_1.net_production_rates[scs]                       # the net production rates of the small concentration species
            mu = state_1.net_production_rates / state_1.concentrations      # the reduced net production rates
            candidates = np.where(np.abs(mu) <= self.epsilon / ((1-self.epsilon)*self.dt_max*self.step))[0]  # species that have the reduced net production rates no more than epsilon/[(1-epsilon)*dt*step)] 
                                                                                                             # and can be considered as candidates for switching off
            candidates_mu = mu[candidates]
            
            # step3
            importance_matrix = importance_matrix(state_0, state_1, self.scheme, self.reactor_type, perturb_factor=1.01)
            switch_off_species = np.concatenate((scs, candidates))
            reduced_importance_matrix = np.delete(importance_matrix, switch_off_species, axis=0)    # delete rows of the importance matrix that correspond to the switch off species
            switch_off_species = filter_indices_by_threshold(reduced_importance_matrix, switch_off_species, threshold=matrix_threshold)
            adapt_t_end = self.states.t[-1] + np.epsilon / ((1-np.epsilon)*np.max(np.abs(mu[switch_off_species])))
            def filter_indices_by_threshold(A, col_indices, threshold=0.01):
                """
                Filters a given set of column indices in a matrix based on their relative contribution to each row.

                Parameters:
                -----------
                A : np.ndarray
                    A 2D NumPy array of shape (m, n), where each row represents a data sample and each column a variable.
                
                col_indices : list or array-like
                    A list of column indices to monitor. The goal is to retain only those indices such that, for every row,
                    the sum of the values in these columns is greater than a specified fraction (threshold) of the total row sum.

                threshold : float, optional
                    A value between 0 and 1. Each row must satisfy that the monitored sum is greater than `threshold * row_sum`.
                    Default is 0.01 (1%).

                Returns:
                --------
                filtered_col_indices : np.array
                    A reduced array of column indices. Major contributors (columns with highest overall sums) are iteratively 
                    removed until the threshold condition is satisfied for every row.
                """
                A = np.array(A)
                col_indices = list(col_indices)
                
                while True:
                    # Row sums: shape (m,)
                    total_row_sum = A.sum(axis=1)
                    
                    # Monitored sums per row (only from selected columns)
                    monitored_sum = A[:, col_indices].sum(axis=1)
                    
                    # Compute the condition: monitored_sum must be > threshold * total
                    valid = monitored_sum > threshold * total_row_sum
                    
                    if np.all(valid):
                        break  # All rows satisfy the condition
                    
                    # If not valid, remove the column with highest total contribution
                    col_sums = A[:, col_indices].sum(axis=0)
                    worst_col_idx = np.argmax(col_sums)
                    col_indices.pop(worst_col_idx)
                    
                    if not col_indices:
                        break

                return np.array(col_indices)
            
            # step4 & step5
            states_step4 = self.reactor_ODE.reaction_progress(dt=self.dt_max, t_start=self.states.t[-1], t_end=np.min(adapt_t_end,self.t_end), method='bdf', switch_off_species=switch_off_species)
            if states_step4.t[-1] >= self.t_end:
                self.states.append(states_step4[1:]) 
            else:
                state_step5 = 
            
            
            
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
t_end = 10e-8

obj = Homo_Reaction_ODE(gas, reactor_type)
switch_off_species = ["N2", "AR","IC3H7O2", "C3H5"]
states = obj.reaction_progress(dt=dt_max, t_end=5e-8, t_start=0.0, method='bdf', switch_off_species=switch_off_species)
# states = obj.reaction_progress(dt=dt_max, t_end=t_end, t_start=5e-8, method='bdf', switch_off_species=switch_off_species)

# prepare the data for output
concentrations_output = np.array(states.concentrations)
titles = np.hstack((['t [s]', 'P [Pa]', 'T [K]', 'rho [kg/m^3]'], states.species_names))
t = np.array(states.t).reshape(-1, 1)
P = np.array(states.P).reshape(-1, 1)
T = np.array(states.T).reshape(-1, 1)
rho = np.array(states.D).reshape(-1, 1)
data = np.hstack((t, P, T, rho, concentrations_output))
# conclude data into a pandas dataframe
df = pd.DataFrame(data, columns=titles)
# output to csv file
df.to_csv("switch_off.csv", index=False)

# state_0 = states[1500]
# state_1 = states[1501]

# matrix = importance_matrix(state_0, state_1, scheme, reactor_type)

# df = pd.DataFrame(matrix, columns=obj.gas.species_names, index=obj.gas.species_names)
# df.index.name = "ID"
# df.to_csv("test_P.csv")



    
 
    

    
        