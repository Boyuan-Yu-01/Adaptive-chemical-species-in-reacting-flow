import cantera as ct
import numpy as np
import scipy.integrate
import pandas as pd
import multiprocessing as mp

class Homo_Reactor:
    """ The class contains the following functions:
            __init__:                   initialise parameters.
            const_V_ODE:                Output the ODE system for constant volume reaction. Capable to switch off reaction given species index.
            const_P_ODE:                Output the ODE system for constant pressure reaction. Capable to switch off energy equation. Capable to switch off reaction given species index.
            reaction_progress:          this function integrate the system from t_start to t_end
            decide_off_species:         given switch off criteria specified in __init__, this function will return switch off species, their FEATURES, and the t_end of the batch
            adaptive_reaction_progress: switch off some species in some batch
            write_to_csv:               output t, P, T, rho, and species concentration into a csv file
    """
    def __init__(self, gas, reactor_type, scheme, dt, epsilon=0.1, step=300, concentration_threshold=1e-7, matrix_threshold=0.1, tol=0.1):
        self.gas = gas
        self.states = []
        self.reactor_type = reactor_type
        self.scheme = scheme
        self.dt = dt
        self.epsilon=epsilon
        self.step = step
        self.concentration_threshold = concentration_threshold
        self.matrix_threshold = matrix_threshold
        self.tol = tol
        
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
        """The ODE function decribes constant volume homogeneous reaction."""
        # State vector is [T, Y_1, Y_2, ... Y_K]
        self.gas.set_unnormalized_mass_fractions(y[1:])
        self.gas.TD = y[0], self.rho
        
        # reaction equations:
        wdot = self.gas.net_production_rates
        if switch_off_species is not None and len(switch_off_species) > 0:
            wdot[switch_off_species] = 0  # handle switch off species: when there are switch off species, the n.p.r. of these species is set to be zero.
        
        dTdt = - (np.dot(self.gas.partial_molar_int_energies, wdot) /
                  (self.rho * self.gas.cv))
        dYdt = wdot * self.gas.molecular_weights / self.rho
        return np.hstack((dTdt, dYdt))
    
    def const_P_ODE(self, t, y, energy="on", switch_off_species=None):
        """The ODE function describs constant pressure homogeneous reaction.
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
    
    def reaction_progress(self, dt, t_end, t_start=0.0, method='bdf', switch_off_species=None):
        """Integrate the ODE system from t_start to t_end with time step dt
           Choose reactor type: 'const_V', 'const_P', or 'const_TP'
           It adds a 'self.states' attribute to the class, which is a SolutionArray that stores the states at each time step.
           """
        # define the ODE solver
        # step 1: check if there are switch off species
        if switch_off_species is None or len(switch_off_species)==0:
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
        
        # step 2: define the solver, and setup the initial conditions    
        solver.set_integrator('vode', method=method,with_jacobian=True)
        y0 = np.hstack((self.gas.T, self.gas.Y))
        solver.set_initial_value(y0, t_start)
        
        # step 3: if no states is recorded, initialise the states with the first state
        if self.states == []:
            self.states = ct.SolutionArray(self.gas, 1, extra={'t':[t_start]})
        
        # step 4: integrate the ODE system from t_start to t_end
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
    
    def decide_off_species(self, state_0, state_1):
        """
        Determine species to be switched off based on two adaptive filtering policies:
        (I) a concentration threshold and (II) their relative contribution to system dynamics.
        
        Parameters:
        -----------
        state_0 : ct.SolutionArray
            Cantera SolutionArray representing the state at the beginning of the current adaptive step.

        state_1 : ct.SolutionArray
            Cantera SolutionArray representing the state at the end of the current adaptive step.

        Returns:
        --------
        scs : np.ndarray
            Indices of species with concentrations below the user-defined concentration threshold.

        scs_w : np.ndarray
            Net production rates of species identified in `scs`.

        candidates : np.ndarray
            Indices of species satisfying the reduced net production rate condition (Policy I).

        candidates_mu : np.ndarray
            Net production rates of species in `candidates`.

        adapt_t_end : float
            Adaptively calculated end time of the current simulation segment, based on Policy I dynamics.

        Notes:
        ------
        - Policy I identifies species with both small concentrations and low net production rates.
        - Policy II filters candidates further by removing species whose relative contribution,
        based on an importance matrix, exceeds a threshold.
        - Species selected for switch-off are those satisfying both policies.
        - The adaptive time `adapt_t_end` is computed to ensure net production rates remain below
        the tolerance (`epsilon`) for selected species throughout the adaptive step.
        """
        
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
                    valid = monitored_sum <= threshold * total_row_sum
                    
                    if np.all(valid):
                        break  # All rows satisfy the condition
                    
                    # If not valid, remove the column with highest total contribution
                    col_sums = A[:, col_indices].sum(axis=0)
                    worst_col_idx = np.argmax(col_sums)
                    col_indices.pop(worst_col_idx)
                    
                    if not col_indices:
                        break

                return np.array(col_indices)
        
        concentrations_1 = state_1.concentrations
        # small concentration species
        scs = np.where(concentrations_1 <= self.concentration_threshold)[0]  # small concentration species
        
        # species that satisfies policy I
        with np.errstate(divide='ignore', invalid='ignore'):    # avoid division by zero
            mu = np.divide(state_1.net_production_rates, state_1.concentrations)
            mu = np.nan_to_num(mu, nan=0.0)

        candidates = np.where(np.abs(mu) <= self.epsilon / ((1-self.epsilon)*self.dt*self.step))[0]  # species that have the reduced net production rates no more than epsilon/[(1-epsilon)*dt*step)] 
        
        # check policy II
        importance_matrix = importance_matrix_calc(state_0, state_1, self.scheme, self.reactor_type, perturb_factor=1.01)
        switch_off_species = np.unique(np.concatenate((scs, candidates)))
        reduced_importance_matrix = np.delete(importance_matrix, switch_off_species, axis=0)    # delete rows of the importance matrix that correspond to the switch off species
        switch_off_species = filter_indices_by_threshold(reduced_importance_matrix, switch_off_species, threshold=self.matrix_threshold)    # filter the switch off species based on the importance matrix
        scs = scs[np.isin(scs, switch_off_species)]
        scs_w = state_1.net_production_rates[scs]                       # the net production rates of the small concentration species
        candidates = candidates[np.isin(candidates, switch_off_species)]  # filter the candidates based on the importance matrix
        candidates_mu = mu[candidates]
        # if len(candidates) != 0:
        #     adapt_t_end = state_1.t + self.epsilon / ((1-self.epsilon)*np.max(np.abs(mu[candidates])))  # given t_start (state_1.t)), we calculate the end time of this batch of adaptive reaction progress
        # else:
        #     adapt_t_end = state_1.t + 300 * self.dt  # if no switch off species, we set the end time to be t_start + 300 * dt, which is a default value.
        
        adapt_t_end = state_1.t + 300 * self.dt
        return scs, scs_w, candidates, candidates_mu, adapt_t_end,     # return 1) small concentration species, 2) n.p.r. of small concentration species 3) policy I species, 4) reduced n.p.r. of policy I species, 5) adaptive end time
    
def importance_matrix_calc(state0, state1, scheme, reactor_type, perturb_factor=1.01, num_cpu = mp.cpu_count()-1):
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
            perturb_factor:     factor to perturb the species concentration"""
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
    dt = t1 - t0
    pert_obj = Homo_Reactor(gas=gas_p, reactor_type=reactor_type, scheme=scheme)  # create an instance of Homo_Reaction_ODE with perturbed gas object
    gas1_p = pert_obj.reaction_progress(dt=dt, t_end=t1, t_start=t0, method='bdf')[-1]  # advance gas_p by one step to yield 'gas1_p': type: cantera.Solution
    with np.errstate(divide='ignore', invalid='ignore'):
        jth_col = (gas1_p.concentrations - gas1.concentrations) / (gas_p.concentrations - gas0.concentrations) * gas0.net_production_rates
    return j, jth_col

    