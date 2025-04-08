'''This script reads reactions from a yaml mechanism, then create a graph representation using graphviz.'''
import cantera as ct
import pandas as pd
import numpy as np
import re
from collections import defaultdict

scheme_path = "/home/boyuan-yu/Documents/USC/research/log/SVD_QSSA/graph"
plot_path = "/home/boyuan-yu/Documents/USC/research/log/SVD_QSSA/graph/graphviz"
scheme = scheme_path+"/"+"FFCM1_skeletal.yaml"
plot_name = "skeletal.gv"

def remove_duplicates(spec, cnt):
    '''This function removes the duplicates from the list of species and add duplicated corresponding coefficients'''
    combined = defaultdict(int)
    for spec, cnt in zip(spec,cnt):
        combined[spec] += cnt
        
    # convert the defaultdict back to 2 lists
    spec = list(combined.keys())
    cnt = list(combined.values())
    
    return spec, cnt
        
def extract_species(reaction):
    '''This function extracts the species from the reaction expressed in string'''
    reaction = reaction.replace("(", "").replace(")", "")
    reac, prod = re.split(r'=>|<=>',reaction)
    reac = [s.strip() for s in reac.split('+') if s.strip()]
    prod = [s.strip() for s in prod.split('+') if s.strip()]
    reac_coef = []
    prod_coef = []
    for s in reac:
        if len(s)>2 and s[1] == ' ':
            num = int(s[0])
            spe = s[2:]
            reac.insert(reac.index(s), spe)
            del reac[reac.index(s)]
            # for i in range(num):
            #     reac.append(spe)  # add multiple time of the species
            reac_coef.append(num)
        else:
            reac_coef.append(1)
    for s in prod:
        if len(s)>2 and s[1] == ' ':
            num = int(s[0])
            spe = s[2:]
            prod.insert(prod.index(s), spe)
            del prod[prod.index(s)]
            # for i in range(num):
            #     prod.append(spe) 
            prod_coef.append(num)
        else:
            prod_coef.append(1)
    
    # remove duplicates from reac and prod and sum the coefficients
    reac, reac_coef = remove_duplicates(reac, reac_coef)
    prod, prod_coef = remove_duplicates(prod, prod_coef)
    return reac, prod, reac_coef, prod_coef

def reaction_in_graph_statement(reac, prod, reac_coef, prod_coef, i):
    '''
    Generate a Graphviz-compatible reaction string
    with coefficients and coloring for non-unity values
    '''
    reac_str = ""

    if reac != "repeat":
        reac_non_one = [j for j, x in enumerate(reac_coef) if x != 1]
        prod_non_one = [j for j, x in enumerate(prod_coef) if x != 1]

        # Reactants with coef == 1
        coef1_species = [reac[j] for j in range(len(reac)) if j not in reac_non_one]
        if coef1_species:
            reac_str += "{" + ",".join(coef1_species) + "}->k" + str(i + 1) + "\t\t\t# reaction " + str(i + 1) + "\n"

        # Reactants with coef ≠ 1
        for j in reac_non_one:
            reac_str += reac[j] + "->k" + str(i + 1) + "[label=" + str(reac_coef[j]) + "][color=\"red\"]\t#reaction " + str(i + 1) + "\n"

        # Products with coef == 1
        coef1_products = [prod[j] for j in range(len(prod)) if j not in prod_non_one]
        if coef1_products:
            reac_str += "k" + str(i + 1) + "->{" + ",".join(coef1_products) + "}\t\t# reaction " + str(i + 1) + "\n"

        # Products with coef ≠ 1
        for j in prod_non_one:
            reac_str += "k" + str(i + 1) + "->" + prod[j] + "[label=" + str(prod_coef[j]) + "][color=\"blue\"]\t#reaction " + str(i + 1) + "\n"

    return reac_str



gas = ct.Solution(scheme)
species_from_cantera = ct.Species.list_from_file(scheme)         # all species in the scheme (list)
reactions = ct.Reaction.list_from_file(scheme,gas)  # all reactions in the scheme (list)

reacs = []  # initialise the list to store the reactions
prods = []  # initialise the list to store the products
reacs_coef = []  # initialise the list to store the coefficients of the reactions
prods_coef = []  # initialise the list to store the coefficients of the products

for reac in reactions:
    rec, prod, rec_coef, prod_coef = extract_species(reac.equation)  # extract the species from the reaction
    if rec in reacs and prod in prods:  # when reaction and product already exist, fill the position with string "repeat"
        reacs.append("repeat")
        prods.append("repeat")
        reacs_coef.append([0])
        prods_coef.append([0])
    else:  # when reaction and product not exist, append the reaction and product to the list
        reacs.append(rec)
        prods.append(prod)
        reacs_coef.append(rec_coef)
        prods_coef.append(prod_coef)

# write the graph plot script for graphviz (.gv)

with open(plot_path+"/"+plot_name, 'w') as f:
    f.write('digraph G {\n')
    for i in range(len(reacs)): # create reaction shaded nodes
        if reacs[i] != "repeat":
            f.write("k"+str(i+1)+"[shape=square, style=filled]"+"\n")
        else:
            f.write("# k"+str(i+1)+"[shape=square, style=dashed]"+"\n")
    f.write("\n")
    
    # create DIRECTED edges between the reactions and products
    for i in range(len(reacs)):
        f.write(reaction_in_graph_statement(reacs[i], prods[i], reacs_coef[i], prods_coef[i], i))
        f.write("\n")
    f.write('}\n') 


