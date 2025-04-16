'''This script convert POLLU problem into a dictionary'''
import cantera as ct
import pandas as pd
import numpy as np
import json
from scipy.integrate import solve_ivp
# scheme = "FFCMy_12_modified.yaml"
scheme = "FFCM2.yaml"

class constant_TP_reaction:
    """Use BDF to solve the constant TP reaction problem given a mechanism"""
    
    def __init__(self, mechanism):
        self.mechanism = mechanism
        self.IC = None                  # evaluate IC in get_initial_condition
        self.solution = None            # evaluate solution in reaction_progress
        
    def build_mechanism(scheme, T, P, X):
        """Build the mechanism given the scheme, T, P, X for the constant TP reaction."""
        gas = ct.Solution(scheme)
        gas.TPX = T, P, X
        species_from_cantera = ct.Species.list_from_file(scheme)         # all species in the scheme (list)
        species_extracted = [str(s).split()[1][:-1] for s in species_from_cantera]  # all species in the scheme (list)
        del species_from_cantera
        reactions_from_cantera = ct.Reaction.list_from_file(scheme,gas)  # all reactions in the scheme (list)

        # Create a dictionary to store the mechanism
        mechanism = {
            "species": {},
            "reactions": {},
        }

        for i, reaction in enumerate(reactions_from_cantera):    # add reactions into the mechanism
            # Store the reaction in the dictionary
            mechanism["reactions"]["reaction "+str(i+1)] = {
                "reactants": gas.reaction(i).reactants,
                "products": gas.reaction(i).products,
                "forward_rate": gas.forward_rate_constants[i],
                "reverse_rate": gas.reverse_rate_constants[i],
            }
            
        for species in species_extracted:  # add species into the mechanism
            # get the net_reaction_rate of this species
            reaction_invo = [i+1 for i,r in enumerate(gas.reactions()) if species in r.reactants or species in r.products] # get the index of the reactions that involve this species
            factor = []             # factor is omega or -omega, depends on whether it is destruction or production
            rate_const = []         # rate constant of the reaction
            species_multiplier = [] # for reaction H + O2 <=> O + OH, species_multiplier = [H, O2] for the forward reaction
            species_exponent = []   # for reaction H + O2 <=> O + OH, species_exponent = [1, 1] for the forward reaction
            
            
            for i in reaction_invo:
                reaction = mechanism["reactions"]["reaction "+str(i)]
                # fill in the forward reaction rate
                if species in reaction["reactants"]:
                    factor.append(-1 * reaction["reactants"][species])
                    rate_const.append(reaction["forward_rate"])
                    species_multiplier.append(list(reaction["reactants"].keys()))
                    species_exponent.append(list(reaction["reactants"].values()))
                else:
                    factor.append(reaction["products"][species])
                    rate_const.append(reaction["forward_rate"])
                    species_multiplier.append(list(reaction["reactants"].keys()))
                    species_exponent.append(list(reaction["reactants"].values()))
                # fill in the backward reaction rate
                if reaction["reverse_rate"] != 0:
                    if species in reaction["reactants"]:
                        factor.append(reaction["reactants"][species])
                        rate_const.append(reaction["reverse_rate"])
                        species_multiplier.append(list(reaction["products"].keys()))
                        species_exponent.append(list(reaction["products"].values()))
                    else:
                        factor.append(-1 * reaction["products"][species])
                        rate_const.append(reaction["reverse_rate"])
                        species_multiplier.append(list(reaction["products"].keys()))
                        species_exponent.append(list(reaction["products"].values()))
            species_net_reaction_rate = [factor, rate_const, species_multiplier, species_exponent]
            # Store the species in the dictionary
            mechanism["species"][species] = {
                "initial_concentration": 0,
                "net_reaction_rate": species_net_reaction_rate,
            }
        return mechanism # example and elaboration see: "/SVD_QSSA/BDF_QSSA/12_species/mech_structure.md"
       
    def get_initial_condition(self, X0, P0):
        """This function plug initial conditions into the mechanism dictionary"""
        n0 = P0/ (ct.gas_constant * T)  # number of moles per unit volume
        X0_dict = {k.strip(): float(v.strip()) for k, v in (item.split(":") for item in X0.split(","))}
        X_sum = sum(X0_dict.values())
        for key, value in X0_dict.items():
            value = value / X_sum * n0
            X0_dict[key] = value
            
        for key in X0_dict.keys():
            if key in self.mechanism["species"].keys():
                self.mechanism["species"][key]["initial_concentration"] = X0_dict[key]
            else:
                print(f"Species {key} not found in the mechanism. However, the programme will still run.")

        self.IC = []
        for key in self.mechanism["species"].keys():
            self.IC.append(self.mechanism["species"][key]["initial_concentration"])
            
    def reaction_progress(self, t_span, t_step, metod="BDF"):
        """This function solve the ODE system using BDF method"""
        species_dict = self.mechanism["species"]
        t_eval = np.arange(t_span[0], t_span[1], t_step)
        def chemical_reaction(t, y, species_dict):
            """This function defines the chemical reaction rate from species_dict"""
            sys_eqns = []
            species_list = list(species_dict.keys())
            for species in species_dict.keys():   # i is the ith species
                func_i = 0
                for j in range(len(species_dict[species]["net_reaction_rate"][0])):    # j corresponds to each individual reaction that relates to ith species
                    func_j = species_dict[species]["net_reaction_rate"][0][j] * species_dict[species]["net_reaction_rate"][1][j]
                    for k in range(len(species_dict[species]["net_reaction_rate"][2][j])):    # for each species, there are species concentration as multiplier, these multiplier species are represneted by k
                        index = species_list.index(species_dict[species]["net_reaction_rate"][2][j][k])
                        func_j *= y[index] ** species_dict[species]["net_reaction_rate"][3][j][k]
                    func_i += func_j
                sys_eqns.append(func_i)
            return sys_eqns        
        sol = solve_ivp(fun=lambda t, y: chemical_reaction(t, y, species_dict), t_span=t_span, y0=self.IC, t_eval=t_eval, method=metod)
        self.solution = sol
        return sol
    
    def get_species_list(self):
        """This function returns the species list"""
        return list(self.mechanism["species"].keys())
    
## use cantera to load mechanism from a .yaml file
gas = ct.Solution(scheme)
T = 2000            # K
P = 1 * ct.one_atm  # 1 atm
X = "C2H6:1, O2: 2"  # stoichiometric mixture (x does not matter. It is only here to complete
                    # gas initialization s.t. we can get reaction rate out of it.)
                    
                    
mechanism = constant_TP_reaction.build_mechanism(scheme=scheme, T=T, P=P, X=X)
obj = constant_TP_reaction(mechanism=mechanism)
obj.get_initial_condition(X0=X, P0=P)
# species = list(obj.mechanism["species"].keys())
# index = species.index(obj.mechanism["species"]["H2"]["net_reaction_rate"][2][0][1])
# print(index)

# # save the mechanism into a json file
# with open("methane_oxygen_12.json","r") as f:
#     json.dump(mechanism, f, indent=4)
    
    
solution = obj.reaction_progress(t_span=(0, 0.002), t_step=1e-9)

data = np.vstack((solution.t,solution.y))
data = data.T
data = pd.DataFrame(data, columns=['t'] + obj.get_species_list())
data = data.iloc[::10000]
data.to_csv("ver_1.csv", index=False)










