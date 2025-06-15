import cantera as ct
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib.colors import Normalize
import scipy.integrate
import numpy as np
import pandas as pd
scheme = "FFCM2.yaml"

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
    
def importance_matrix(state1, state2, scheme):
    """This function evaluats and returns the importance matrix"""
    
    def concentration_perturbation(state1, state2, idx, dt, scheme):
        """ This function perturbs the concentration of the gas at state1
            'idx' is the index of the species to be perturbed
            'dt' is the time step from state1 to state2"""
        P = state1.P.copy()
        T = state1.T.copy()
        concentrations = state1.concentrations.copy()
        
        # perturb the concentration of species[idx], create states_p to record the perturbed state
        concentrations_p = concentrations.copy()  # make a copy of the concentrations to perturb
        concentrations_p[idx] += state1.net_production_rates[idx] * dt
        P_p = P * np.sum(concentrations_p) / np.sum(concentrations)  # adjust pressure to keep the total moles constant
        X = concentrations_p / np.sum(concentrations_p)  # normalize concentrations to get mole fractions
        gas_p = ct.Solution(scheme)
        gas_p.TPX = T, P_p, X     # set up the perturbed gas state
        
        reactor_p = Homo_Reaction_ODE(gas_p)
        states_p = reactor_p.reaction_progress(reactor="const_v", dt=dt,
                                               t_end=state2.t, t_start=state1.t)
        ith_col = (states_p[-1].concentrations - state2.concentrations)/dt # The ith column of the importance matrix
        return ith_col      # this is a 1D array
        
    size = np.array(state1.speices_names).size  # size of m
    matrix = np.zeros((size, size)) # initialise the importance matrix of size m by m
    dt = state2.t = state1.t 
    for i in range(size):   # this loop iterates through each species
        # perturb the concentration of species i by its n.p.r * dt
        ith_col = concentration_perturbation(state1, state2, i, dt, scheme)
        matrix[:,i] = ith_col
    return matrix
    

## set up initial gas composition
gas = ct.Solution(scheme)
T = 2000
P = 1 * ct.one_atm
X = "CH4:1, O2:2"
gas.TPX = T, P, X

## set up the t constraints for the simulation
dt_max = 1e-8
t_end = 3e-5

## setup reactor
reactor_ODE = Homo_Reaction_ODE(gas).const_V_ODE
states = ct.SolutionArray(gas, 1, extra={'t':[0.0]})
print(isinstance(states.concentrations, np.ndarray))
