'''This code helps to discover the eigenvalue, eigenvector, and spectrum of the scaled reaction 
matrix A_tilde.
    - This code read the data from .csv file, use the current concentration as the scaling factor.
    - The output will be saved to a .csv file.'''

import numpy as np
import pandas as pd
import csv

## functions
def scaled_species_matrix(alpha, beta, gamma):
    '''This function returns the species scaling matrix'''
    m_s = np.array([[1/alpha, 0, 0], [0, 1/beta, 0], [0, 0, 1/gamma]])
    return m_s

def scaled_reaction_matrix(alpha, beta, gamma):
    '''This function returns the reaction scaling matrix'''
    m_r = np.array([[1/alpha, 0, 0], [0, 1/(beta * gamma), 0], [0, 0, 1/(beta * beta)]])
    return m_r

def tilde_matrix(alpha, beta, gamma):
    '''This function returns the scaled reaction matrix'''
    x_tilde = scaled_species_matrix(alpha, beta, gamma)
    reac_tilde = scaled_reaction_matrix(alpha, beta, gamma)
    A = [[-k1, k3, 0],[k1, -k3, -k2],[0, 0, k2]]
    A_tilde = np.dot(np.linalg.inv(x_tilde), np.dot(A, reac_tilde))
    return A_tilde

def eigen(A_tilde):
    '''This function returns the eigenvalues of the scaled reaction matrix'''
    val, vec = np.linalg.eig(A_tilde)
    vec_inv = np.linalg.inv(vec)
    return val, vec, vec_inv

## define all coefficients
k1 = 0.04
k2 = 3e7
k3 = 1e4

## read the concentration and time from the .csv file
t = 7600
path = '/home/boyuan-yu/Documents/USC/research/log/SVD_QSSA/unscale/'
# fileName = "unscale_ini.csv"      # file contains from 0-1 s
fileName = "unscale_00001.csv"          # file contains from 0 to 7,900 s
df = pd.read_csv(path + fileName)
df = df.values                      # df is now a n by 5 numpy array, columns are:  
                                    # time, logt, [A], [B], [C]
index = np.abs(df[:,0] - t).argmin() # find the index of the time closest to t
if index == 0 or index == len(df) - 1:
    print("\n\n\tThe time is out of range, you may consider to change a file.\n\n")
species = df[index, 2:]              # get the species concentration at time t
species = np.maximum(species, 1e-6) # avoid scale by a very small number: cutoff value is 1e-6
alpha = 1/species[0]
beta = 1/species[1]
gamma = 1/species[2]

## calculate the scaled reaction matrix
A_tilde = tilde_matrix(alpha, beta, gamma)
val, vec, vec_inv = eigen(A_tilde)
print("The eigenvalues of the scaled reaction matrix are:\n ", val, "\n")
print("The eigenvectors of the scaled reaction matrix are:\n ", vec, "\n")
print("The inverse of eigenvectors of the scaled reaction matrix are:\n ", vec_inv, "\n")

