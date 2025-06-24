import cantera as ct
import numpy as np
import scipy.integrate
import pandas as pd
import multiprocessing as mp

class Homo_Reaction:
    def __init__(self, scheme, gas, dt_max, t_end, t_start=0.0, mode=None, csv_output=None, output_species=[]):
        # define reaction related class level parameters
        self.gas = gas
        self.scheme = scheme
        self.dt_max = dt_max
        self.t_start = t_start
        self.t_end = t_end
        self.mode = mode
        self.csv_name = csv_output
        self.output_species = output_species
        self.states = ct.SolutionArray(self.gas, 1, extra={'t': [t_start]})
        
        # initialise solver related class level parameters
        self.solver = None
        
        # define dispatcher: use the following function to call different mode
        self.dispatch = {
            "const_V": self.const_V,
            "const_P": self.const_P,
            "const_TP": self.const_TP,
        }
        
    def run(self, mode=None):
        """run different mode: const_V, const_P, or const_TP"""
        mode_to_run = mode or self.mode    # verbose
        if mode_to_run not in self.dispatch:
            raise ValueError(f"Unknown reactor mode: '{mode_to_run}'")
        return self.dispatch[mode_to_run]()
        
    def const_V_ODE(self, t, y):
        """ODE function: solve constant volume homogeneous reaction"""
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
        """ODE function: solve constant pressure homogeneous reaction.
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
    
    def reaction_progress(self, dt, t_end, t_start=0.0, method='bdf',energy='on'):
        """Integrate the ODE system from t_start to t_end with time step dt
           Choose reactor type: 'const_V' or 'const_P'
           """
        # choose equation system to solve
        if self.mode.lower() == "const_v":
            sys = self.const_V_ODE
            self.rho, _ = self.gas.DP
        elif self.mode.lower() == "const_p":
            sys = lambda t, y: self.const_P_ODE(t, y, energy="on")
            self.P = self.gas.P
        elif self.mode.lower() == "const_tp":
            sys = lambda t, y: self.const_P_ODE(t, y, energy="off")
            self.P = self.gas.P
            self.T = self.gas.T
        
        # set up the ODE solver
        if self.solver is None:
            self.solver = scipy.integrate.ode(sys)
            self.solver.set_integrator('vode', method=method, with_jacobian=True)
        y0 = np.hstack((self.gas.T, self.gas.Y))
        self.solver.set_initial_value(y0, t_start)
        
        # prepare to store results
        while self.solver.successful() and self.solver.t < t_end:
            self.solver.integrate(self.solver.t + dt)
            if self.mode.lower() == "const_v":
                self.gas.TDY = self.solver.y[0], self.rho, self.solver.y[1:]
            elif self.mode.lower() == "const_p":
                self.gas.TPY = self.solver.y[0], self.P, self.solver.y[1:]
            elif self.mode.lower() == "const_tp":
                self.gas.TPY = self.T, self.P, self.solver.y[1:]
            self.states.append(self.gas.state, t=self.solver.t)
            
        return None        
    
    def const_TP(self):
        """This function simulates a constant temperature & pressure homogeneous reactor with adiabatic wall conditions."""
        # grab parameters from "__init__"
        dt_max = self.dt_max
        t_start = self.t_start
        t_end = self.t_end
        # reaction progress:
        self.reaction_progress(dt=dt_max, t_end=t_end, t_start=t_start, method='bdf', energy='off')
        
    def const_P(self):
        """this function simulates a constant pressure homogeneous reactor with adiabatic wall conditions."""
        # grab parameters from "__init__"
        dt_max = self.dt_max
        t_start = self.t_start
        t_end = self.t_end
        
        #  reaction progress:
        self.reaction_progress(dt=dt_max, t_end=t_end, t_start=t_start, method='bdf', energy='on')
        
    def const_V(self):
        """this function simulates a constant volume homogeneous reactor with adiabatic wall conditions."""
        # grab parameters from "__init__"
        dt_max = self.dt_max
        t_start = self.t_start
        t_end = self.t_end
        
        # reaction progress:
        self.reaction_progress(dt=dt_max, t_end=t_end, t_start=t_start, method='bdf')     
            
        
    
def importance_matrix_parallel(state0, state1, scheme, mode, perturb_factor=1.01, num_cpu=mp.cpu_count()-1):
    """This function evaluats and returns the importance matrix"""
    size = np.array(state0.species_names).size  # size of m
    matrix = np.zeros((size, size)) # initialise the importance matrix of size m by m
    dt = state1.t - state0.t 
    
    ## convert state1 and state2 into NumPy-compatible data
    T0, P0, X0 = state0.TPX
    state0_data = [T0, P0, X0]
    T1, P1, X1 = state1.TPX
    state1_data = [T1, P1, X1]
    
    args = [(i,state0.t, state1.t, state0_data, state1_data, dt, scheme, mode, perturb_factor) for i in range(size)]
    num_cpu = mp.cpu_count() - 1
    with mp.Pool(processes=num_cpu) as pool:
        results = pool.starmap(compute_column, args)
    
    for i, col in results:
        matrix[:, i] = col
        
    return matrix
        
def compute_column(i, t0, t1, state0_data, state1_data, dt, scheme, mode, perturb_factor):
    gas0 = ct.Solution(scheme)
    gas0.TPX = state0_data[0], state0_data[1], state0_data[2]
    gas1 = ct.Solution(scheme)
    gas1.TPX = state1_data[0], state1_data[1], state1_data[2]
    return i, concentration_perturbation(gas0, gas1, t0, t1, i, dt, scheme, mode, perturb_factor)

def concentration_perturbation(state0, state1, t0, t1, idx, dt, scheme, mode, perturb_factor):
    """ This function perturbs the concentration of the gas at state1
        'idx' is the index of the species to be perturbed
        'dt' is the time step from state1 to state2"""
    P = state0.P
    T = state1.T
    concentrations = state0.concentrations.copy()
    
    concentrations_p = concentrations.copy()  # make a copy of the concentrations to perturb

    concentrations_p[idx] *= perturb_factor  # perturb the concentration of species[idx]
    P_p = P * np.sum(concentrations_p) / np.sum(concentrations)  # adjust pressure to keep the total moles constant
    X = concentrations_p / np.sum(concentrations_p)  # normalize concentrations to get mole fractions
    gas_p = ct.Solution(scheme)
    gas_p.TPX = T, P_p, X     # set up the perturbed gas state
    
    reactor_p = Homo_Reaction(scheme = scheme, gas=gas_p, dt_max=dt, t_end=t1, t_start=t0, mode=mode)
    reactor_p.reaction_progress(dt=dt, t_end=t1, t_start=t0)
    states_p = reactor_p.states
    nominator = (states_p[-1].concentrations - state1.concentrations) * state0.net_production_rates
    denominator = states_p[-1].concentrations[idx] - concentrations[idx]
    denominator = np.clip(denominator, 1e-12, None)
    return nominator/denominator      # this is a 1D array

        
## set up initial gas composition
scheme = "FFCM2.yaml"
gas = ct.Solution(scheme)
T = 2000
P = 1 * ct.one_atm
X = "CH4:1, O2:2"
gas.TPX = T, P, X

## set up the t constraints for the simulation
dt_max = 1e-8
t_end = 3e-5
reactor = Homo_Reaction(scheme=scheme, gas=gas, dt_max=dt_max, t_end=t_end, t_start=0.0, mode='const_TP', csv_output='test.csv', output_species=['CH4','CO2'])
reactor.run()

matrix = importance_matrix_parallel(reactor.states[1500], reactor.states[1501], scheme=scheme, mode="const_TP")

# save the matrix to a csv file:
df = pd.DataFrame(matrix, columns=reactor.gas.species_names, index=reactor.gas.species_names)
df.index.name = "ID"
df.to_csv("test_matrix.csv")