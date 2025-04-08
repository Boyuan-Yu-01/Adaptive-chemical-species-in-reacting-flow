'''This script generates the statictical information of a given model.
 This script is used to draw a graphical representation of a model.'''
   
import cantera as ct
import numpy as np
import pandas as pd
import re
scheme = "FFCMy_12_modified.yaml"

def extract_species(reaction):
    '''This function extracts the species from the reaction string'''
    reaction = reaction.replace("(", "").replace(")", "")
    reac, prod = re.split(r'=>|<=>',reaction)
    reac = [s.strip() for s in reac.split('+') if s.strip()]
    prod = [s.strip() for s in prod.split('+') if s.strip()]
    for s in reac:
        if len(s)>2 and s[1] == ' ':
            num = int(s[0])
            spe = s[2:]
            del reac[reac.index(s)]
            # for i in range(num):
            #     reac.append(spe)  # add multiple time of the species
            reac.append(spe)
    for s in prod:
        if len(s)>2 and s[1] == ' ':
            num = int(s[0])
            spe = s[2:]
            del prod[prod.index(s)]
            # for i in range(num):
            #     prod.append(spe)
            prod.append(spe)
    print (reac, prod)
    return reac, prod
    

gas = ct.Solution(scheme)
species_from_cantera = ct.Species.list_from_file(scheme)         # all species in the scheme (list)
reactions = ct.Reaction.list_from_file(scheme,gas)  # all reactions in the scheme (list)

species  = []  # list to store the species
for i in range(len(species_from_cantera)):
    species.append(species_from_cantera[i].name)  # append the species to the list
species.append("M")
statistics = np.zeros((3,len(species))) # 2D array to store the statistics of species

for reac in reactions:  # find species as reactant or product
    reac, prod = extract_species(reac.equation)
    for s in reac:
        position = species.index(s)
        statistics[0,position] += 1
    for s in prod:
        position = species.index(s)
        statistics[1,position] += 1
    
for i in range(len(statistics[0])):
    statistics[2,i] = statistics[0,i] + statistics[1,i]

df = pd.DataFrame(statistics, columns=species)
df.to_csv("species_statistics.csv", index=False)  # save the statistics to a csv file