"""
Integrating constant pressure ignition using SciPy
The code is copied and modified from: https://cantera.org/dev/_downloads/6a24950c616ecb6f605627b4a3648054/custom.py

The code will be compared with cantera "ct.IdealGasConstPressureMoleReactor"
==================================================

Solve a constant pressure ignition problem where the governing equations are
implemented in Python.

This demonstrates an approach for solving problems where Cantera's reactor
network model cannot be configured to describe the system in question. Here,
Cantera is used for evaluating thermodynamic properties and kinetic rates while
an external ODE solver is used to integrate the resulting equations. In this
case, the SciPy wrapper for VODE is used, which uses the same variable-order BDF
methods as the Sundials CVODES solver used by Cantera.

Requires: cantera >= 2.5.0, scipy >= 0.19, matplotlib >= 2.0

.. tags:: Python, combustion, reactor network, ignition delay, user-defined model, plotting
"""

import cantera as ct
import numpy as np
import scipy.integrate
import pandas as pd


class ReactorOde:
    def __init__(self, gas):
        # Parameters of the ODE system and auxiliary data are stored in the
        # ReactorOde object.
        self.gas = gas
        self.P = gas.P
        self.T = gas.T

    def __call__(self, t, y):
        """the ODE function, y' = f(t,y) """
        # State vector is [Y_1, Y_2, ... Y_K]
        self.gas.set_unnormalized_mass_fractions(y)
        self.gas.TP = self.T, self.P
        rho = self.gas.density

        wdot = self.gas.net_production_rates
        dYdt = wdot * self.gas.molecular_weights / rho

        return np.array(dYdt)


scheme = 'FFCM2.yaml'

# Initial condition
gas = ct.Solution(scheme)
T = 2000
P = 1 * ct.one_atm
X = "CH4:1, O2:2"
gas.TPX = T, P, X
y0 = np.array(gas.Y)

t = [0.0]

# Set up objects representing the ODE and the solver
ode = ReactorOde(gas)
solver = scipy.integrate.ode(ode)
solver.set_integrator('vode', method='bdf', with_jacobian=True)
solver.set_initial_value(y0)

# Integrate the equations, keeping T(t) and Y(k,t)
t_end = 0.002
states = ct.SolutionArray(gas, 1)
dt = 1e-8
t = [0.0]
while solver.successful() and solver.t < t_end:
    solver.integrate(solver.t + dt)
    gas.TPY = T, P, solver.y
    states.append(gas.state, t=solver.t)
    t.append(solver.t)
    
rho = np.array(states.D).reshape(-1, 1)  # column vector: m by 1
T = np.array(states.T).reshape(-1, 1)  # column vector: m by 1
t = np.array(t).reshape(-1, 1)  # column vector: m by 1
# include some species of interest
species_of_interest = ['OH', 'H2O', 'CO2', 'CH4']
soi_idx = [list(states.species_names).index(item) for item in species_of_interest]
concentrations = np.array(states.concentrations)[:, soi_idx]


# output t, rho, T into a csv file
titles = ["t [s]", "rho [kg/m^3]", "T [K]"] + species_of_interest
data = np.hstack((t, rho, T, concentrations))
df = pd.DataFrame(data, columns=titles)
df.to_csv("online_const_P.csv", index=False)

# # Plot the results
# try:
#     import matplotlib.pyplot as plt
#     # L1 = plt.plot(states.t, states.T, color='r', label='T', lw=2)
#     L1 = plt.plot(states.t, states.density_mass, label='density', lw=2)
#     plt.xlabel('time (s)')
#     # plt.ylabel('Temperature (K)')
#     plt.ylabel('density')
#     plt.twinx()
#     L2 = plt.plot(states.t, states('OH').Y, label='OH', lw=2)
#     plt.ylabel('Mass Fraction')
#     plt.legend(L1+L2, [line.get_label() for line in L1+L2], loc='lower right')
#     plt.show()
# except ImportError:
#     print('Matplotlib not found. Unable to plot results.')
