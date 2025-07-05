from Homo_ODE_ver3 import *

##########################################################
## This is a test file to test functions and classes in ##
## script "Homo_ODE_ver2.py"--------------------------- ##
##########################################################

scheme = "FFCM2.yaml"
gas = ct.Solution(scheme)
T = 2000
P = 1 * ct.one_atm
X = "CH4:1, O2:2"
gas.TPX = T, P, X
reactor_type = "const_P"

dt_max = 1e-8
t_end = 5e-5

##########################################################
## Test 1: test the species selection system ---------- ## 
## Giving state 0 and state1, find -------------------- ## 
## 1) switch off species ------------------------------ ##
## 2) how long will it last -(constrain to 300) ------- ##
##########################################################

# obj1 = Homo_Reactor(gas=gas, reactor_type=reactor_type, scheme=scheme)
# obj1.reaction_progress(dt=dt_max, t_end=t_end)
# idxs = [0, 500, 1000, 1500, 2000, 3000, 4000]

# def species_idx_reader(states, species_idxs):
#     """
#     Given a list of species indexes, return the species names.
#     """
#     return [states.species_names[idx] for idx in species_idxs]

# for idx in idxs:
#     print(f"The index is {idx}")
#     scs1, scs_w1, candidates1, candidates_mu1, adapt_t_end1 = obj1.decide_off_species(obj1.states[idx], obj1.states[idx+1])
#     print("Small concentration species:", species_idx_reader(obj1.states, scs1))
#     print("Candidate species:", species_idx_reader(obj1.states,candidates1))
#     print("The start time is {:.2e}s".format(obj1.states[idx].t))
#     print("The end time is {:.2e}s".format(adapt_t_end1))
#     print("------------------------------------------------------------")

##########################################################
## Test 2: run the system ----------------------------- ## 
##########################################################
# obj2 = Homo_Reactor(gas, reactor_type, scheme)
# obj2.adaptive_reaction_progress(dt_max, t_end=t_end)
# obj2.to_csv("ver3_test.csv")

obj3 = Homo_Reactor(gas, reactor_type, scheme, step=100)
obj3.adaptive_reaction_progress(dt_max, t_end=t_end)
obj3.to_csv("ver3_2test.csv")