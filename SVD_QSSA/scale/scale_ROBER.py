import numpy as np
import sys
from tqdm import tqdm
import pandas as pd

## edit input parameters from bash script
# timeStep = float(sys.argv[1])
# output = sys.argv[2]
timeStep = 0.0001 # for testing

## Define the reaction coefficients and reaction matrix
k1 = 0.04
k2 = 3e7
k3 = 1e4
A = [[-k1, k3, 0],[k1, -k3, -k2],[0, 0, k2]]
alpha = 1e-3
# beta = 4e5
# gamma = 1
beta = 448998.89
gamma = 8064.0
coefs = np.array([alpha, beta, gamma])

## Construct A_prime
D1 = [[alpha,0,0],[0,beta,0],[0,0,gamma]]
D2 = [[1/alpha, 0, 0],[0, 1/(beta*gamma), 0],[0, 0, 1/beta**2]]
A_prime = np.dot(D1,np.dot(A,D2))
val, vec = np.linalg.eig(A_prime)

## Define the initial conditions 
species_0 = np.array([[1.0], [1e-6], [1e-6]])
species_0_prime = np.array([[1.0*alpha], [1e-6*beta], [1e-6*gamma]])
# species_0_prime = np.array([[1.0*alpha], [0*beta], [0*gamma]])

## Define time series & initialise the solution vector
t = np.arange(0,5*10e4, timeStep)
x = species_0[:,0].copy()[:,None]
x_prime = species_0_prime[:,0].copy()[:,None]

## Reaction Progression
for i in tqdm(range(1,len(t))):
    reaction = [[x_prime[0,i-1]],[x_prime[1,i-1]*x_prime[2,i-1]],[x_prime[1,i-1]**2]]  # CALCULATION PROCEEDS WITHIN SCALED DOMAIN.
    delta_x_prime = np.dot(A_prime, reaction) * timeStep
    new_x_prime = np.maximum(x_prime[:, i-1] + delta_x_prime[:, 0], 0)  # ensure non-negative values
    new_x = new_x_prime * np.reciprocal(coefs)  # scale back to real domain
    x_prime = np.hstack((x_prime, new_x_prime[:, None]))
    x = np.hstack((x, new_x[:, None]))
    if max(new_x) > 1e3:
        sys.exit('Concentration values are too high. Exiting...')

## save the results to a csv file
t = t[:,None]
data = np.hstack((t, x.T))
indices = np.linspace(0, data.shape[0]-1, num=300, dtype=int)
data = data[indices]
df = pd.DataFrame(data, columns=['time', '[A]', '[B]', '[C]'])
df.to_csv('output.csv', index=False)