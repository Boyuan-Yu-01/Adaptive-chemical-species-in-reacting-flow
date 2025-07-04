from Homo_ODE_ver2 import *

##########################################################
## This is a test file to test functions and classes in ##
## script "Homo_ODE_ver2.py"--------------------------- ##
##########################################################

##########################################################
## Test 1: run full model reaction using---------------- ## 
## 'Homo_Reaction_ODE'---------------------------------- ##
###########################################################
scheme = "FFCM2.yaml"
gas = ct.Solution(scheme)
T = 2000
P = 1 * ct.one_atm
X = "CH4:1, O2:2"
gas.TPX = T, P, X
reactor_type = "const_P"

dt_max = 1e-8
t_end = 5e-5

# obj1 = Homo_Reaction_ODE(gas, reactor_type)
# obj1.reaction_progress(dt=dt_max, t_end=t_end)
# obj1.to_csv("result_csv/const_V_full.csv")

##########################################################
## Test 2: run full model reaction with 3 steps-------- ## 
## step1: switch off CO2, CH4, O2 --------------------- ## 
## step2: full mode ----------------------------------- ##
## step3: switch off O2, CH4 and CO2 ------------------ ##
## O2: idx 3, CO2: idx 18, CH4: idx 16 ---------------- ##
##########################################################
# obj2 = Homo_Reaction_ODE(gas, reactor_type)
# obj2.reaction_progress(dt=dt_max, t_end=1e-5, t_start=0.0, switch_off_species=[16, 3, 18])
# obj2.reaction_progress(dt=dt_max, t_end=2e-5, t_start=1e-5)
# obj2.reaction_progress(dt=dt_max, t_end=3e-5, t_start=2e-5, switch_off_species=[16, 3, 18])
# obj2.to_csv("result_csv/const_P_test2_1.csv")

##########################################################
## Test 3: importance matrix -------------------------- ## 
## test if the output of the importance matrix is ----- ##
## reasonable by outputing the matrix. ---------------- ##
## Check: --------------------------------------------- ##
## ------ 1) Is value within one row always the same? - ##
## ------ 2) Is there very large value? --------------- ##
##########################################################
# obj3 = Homo_Reaction_ODE(gas, reactor_type)
# obj3.reaction_progress(dt=dt_max, t_end=t_end)
# states = obj3.states
# species_names = states.species_names

# def print_out_matrix(matrix, species_names, output_name):
#     df = pd.DataFrame(matrix, columns=species_names, index=species_names)
#     df.index.name = "species"
#     df.to_csv(output_name)
    
# Jacobian1 = importance_matrix_calc(states[1], states[2], scheme, reactor_type)
# Jacobian2 = importance_matrix_calc(states[1000], states[1001], scheme, reactor_type)
# Jacobian3 = importance_matrix_calc(states[2000], states[2001], scheme, reactor_type)
# Jacobian4 = importance_matrix_calc(states[3000], states[3001], scheme, reactor_type)
# Jacobian5 = importance_matrix_calc(states[4000], states[4001], scheme, reactor_type)

# print_out_matrix(Jacobian1, species_names, "IM_test3_1.csv")
# print_out_matrix(Jacobian2, species_names, "IM_test3_2.csv")
# print_out_matrix(Jacobian3, species_names, "IM_test3_3.csv")
# print_out_matrix(Jacobian4, species_names, "IM_test3_4.csv")
# print_out_matrix(Jacobian5, species_names, "IM_test3_5.csv")

##########################################################
## Test 4: test the species selection system ---------- ## 
## Giving state 0 and state1, find -------------------- ## 
## 1) switch off species ------------------------------ ##
## 2) how long will it last -(constrain to 300) ------- ##
##########################################################
obj4 = Adaptive_Chemical_Reaction(gas, scheme, t_end, dt_max, reactor_type, epsilon=0.1, matrix_threshold=0.1, concentration_threshold=1e-7)
obj4.reactor_ODE.reaction_progress(dt=dt_max, t_end=t_end)
idxs = [0, 500, 1000, 1500, 2000, 3000, 4000]

def species_idx_reader(states, species_idxs):
    """
    Given a list of species indexes, return the species names.
    """
    return [states.species_names[idx] for idx in species_idxs]

for idx in idxs:
    print(f"The index is {idx}")
    scs1, scs_w1, candidates1, candidates_mu1, adapt_t_end1 = obj4.decide_off_species(obj4.reactor_ODE.states[idx], obj4.reactor_ODE.states[idx+1])
    print("Small concentration species:", species_idx_reader(obj4.reactor_ODE.states, scs1))
    print("Candidate species:", species_idx_reader(obj4.reactor_ODE.states,candidates1))
    print("The start time is {:.2e}s".format(obj4.reactor_ODE.states[idx].t))
    print("The end time is {:.2e}s".format(adapt_t_end1))
    print("------------------------------------------------------------")

##########################################################
## Test 5: test the adaptive_reaction_progress -------- ##
##########################################################
