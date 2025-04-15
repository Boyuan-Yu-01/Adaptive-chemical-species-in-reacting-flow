import cantera as ct
import pandas as pd
import numpy as np
import re
from collections import defaultdict
from constant_TP_reaction import constant_TP_reaction
scheme = "FFCMy_12_modified.yaml"
gas = ct.Solution(scheme)
T = 2000            # K
P = 1 * ct.one_atm  # 1 atm
X = "CH4:1, O2: 2"  # stoichiometric mixture (x does not matter. It is only here to complete
                    # gas initialization s.t. we can get reaction rate out of it.)
mechanism = constant_TP_reaction.build_mechanism(scheme=scheme, T=T, P=P, X=X)
obj = constant_TP_reaction(mechanism=mechanism)
obj.get_initial_condition(X0=X, P0=P)
print(obj.mechanism["species"].keys())

def chemical_reaction(t, y, species_dict):
    sys_eqns = []
    species = list(species_dict.keys())
    for species in species_dict.keys():   # i is the ith species
        func_i = 0
        for j in len(species_dict[species]["net_reaction_rate"][0]):    # j corresponds to each individual reaction that relates to ith species
            func_j = species_dict[species]["net_reaction_rate"][0][j] * species_dict[species]["net_reaction_rate"][1][j]
            for k in len(species_dict[species]["net_reaction_rate"][2]):    # for each species, there are species concentration as multiplier, these multiplier species are represneted by k
                index = species.index(species_dict[species]["net_reaction_rate"][2][j][k])
                func_j *= y[index] ** species_dict[species]["net_reaction_rate"][3][j][k]
            func_i += func_j
        sys_eqns.append(func_i)
    return sys_eqns


    

#####################################################
## setup initial conditions #########################
y0 = []
for species, species_info in obj.mechanism["species"].items():
    y0.append(species_info["initial_concentration"])

t_span = (0, 2)
t_eval = np.arange(t_span[0], t_span[1], 1e-8)
# print(len(t_eval))
for i, species in enumerate(obj.mechanism["species"].keys()):
    print(f"{i}: {species}")