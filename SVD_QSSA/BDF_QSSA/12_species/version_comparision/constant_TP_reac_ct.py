import numpy as np
import cantera as ct

scheme = "FFCM2.yaml"
gas = ct.Solution(scheme)
T = 2000
P = 1 * ct.one_atm
X = "C2H6:1, O2: 2"
gas.TPX = T, P, X
r = ct.IdealGasConstPressureReactor(contents=gas, energy='off', name="isothermal")
sim = ct.ReactorNet([r])
sim.verbose = True
dt_max = 1e-8
t_end = 0.002
states = ct.SolutionArray(gas, extra=['t'])
species_print = ["H", "O", "O2", "OH", "H2O", "CO", "CO2", "C2H6"]
output_file = "ver_cantera.csv"


while sim.time<t_end:
    sim.advance(sim.time + dt_max)
    states.append(r.thermo.state, t=sim.time)
    
states.save(fname=output_file, overwrite =True, basis = "X")