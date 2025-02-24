import torch
import torch.autograd as autograd         # computation graph
from torch import Tensor                  # tensor node in the computation graph
import torch.nn as nn                     # neural networks
import torch.optim as optim               # optimizers e.g. gradient descent, ADAM, etc.

import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from mpl_toolkits.axes_grid1 import make_axes_locatable
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.ticker
from sklearn.model_selection import train_test_split

import numpy as np
import time
from pyDOE import lhs         #Latin Hypercube Sampling
import scipy.io

## Device configuration
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
# device = 'cpu'  # for testing

####################
## Neural Network ##
####################
class FCN(nn.Module):
    def __init__(self, layers):
        super(FCN, self).__init__()
        self.activation = nn.Tanh()
        self.loss_function = nn.MSELoss(reduction = 'mean')
        self.linears = nn.ModuleList([nn.Linear(layers[i], layers[i+1]) for i in range(len(layers)-1)]) # nn.Linear(in_features, out_features, bias=True)
        self.iter = 0
        
        ## Initialise weights and biases
        for i in range(len(layers)-1):
            nn.init.xavier_normal_(self.linears[i].weight.data, gain=1.0)
            nn.init.zeros_(self.linears[i].bias.data) # initialize bias with zeros
            
    def forward(self,x):
        if torch.is_tensor(x) != True:         
            x = torch.from_numpy(x)                
        a = x.float()
        for i in range(len(layers)-2):  
            z = self.linears[i](a)              
            a = self.activation(z)    
        a = self.linears[-1](a)
        return a
    
    def loss_NN(self, X_NN, Y_NN):
        loss_NN = self.loss_function(self.forward(X_NN), Y_NN)
        return loss_NN
    
    def loss_PDE(self, X_PDE, g):
        X = X_PDE.clone()
        X.requires_grad = True
        NN = self.forward(X)
        NN_x_t = autograd.grad(NN, X, torch.ones_like(NN).to(device), retain_graph=True, create_graph=True)[0]
        NN_xx_tt = autograd.grad(NN_x_t, X, torch.ones_like(NN_x_t).to(device), retain_graph=True, create_graph=True)[0]
        NN_t = NN_x_t[:,[1]]
        NN_xx = NN_xx_tt[:,[0]]
        f = NN_t - NN_xx + torch.exp(-X[:,[1]])*(torch.sin(torch.pi*X[:,[0]])-torch.pi**2 * torch.sin(torch.pi*X[:,[0]]))
        loss_PDE = self.loss_function(f,g)
        return loss_PDE
    
    def loss_PINN(self, X_NN, Y_NN, X_PDE, g):
        loss_NN = self.loss_NN(X_NN, Y_NN)
        loss_PDE = self.loss_PDE(X_PDE, g)
        loss_PINN = loss_NN + loss_PDE
        return loss_PINN

#############################
## Testing Data Generation ##
#############################
print("-------------------------------------------------")
print("Generating Testing Data:")
print("-------------------------------------------------")

## Discretize the domain constrained by ICs & BCs 
X = torch.linspace(-1,1,200)
T = torch.linspace(0,1,100)
x,t = torch.meshgrid(X,T)

## Extract locations for ICs & BCs
X_ic = torch.hstack((x[:,0][:,None],t[:,0][:,None]))
Y_ic = torch.sin(torch.pi * X_ic[:,0])[:,None]
X_bc_u = torch.hstack((x[0,:][:,None],t[0,:][:,None]))
X_bc_l = torch.hstack((x[-1,:][:,None],t[-1,:][:,None]))
Y_bc_u = torch.zeros(X_bc_u.shape[0],1)
Y_bc_l = torch.zeros(X_bc_l.shape[0],1)
X_nn = torch.vstack((X_ic, X_bc_u, X_bc_l))
Y_nn = torch.vstack((Y_ic, Y_bc_u, Y_bc_l))

alpha = 100     # number of training sets for NN
beta  = 10000   # number of training sets for Physics
idx = np.random.choice(X_nn.size(0), alpha, replace=False)
X_train_nn = X_nn[idx,:]                            # training sets for NN (x,t)
Y_train_nn = Y_nn[idx,:]                            # training sets for NN (y)
lb = torch.hstack((x[0][0],t[0][0]))
ub = torch.hstack((x[-1][-1],t[-1][-1]))
X_train_p = lb + (ub-lb)*lhs(2,beta)                # training sets for Physics ONLY
X_train_p = torch.vstack((X_train_nn,X_train_p))    # training sets for Physics (x,t)

## Move training data to GPU
X_train_nn = X_train_nn.float().to(device)
Y_train_nn = Y_train_nn.float().to(device)
X_train_p = X_train_p.float().to(device)
g = torch.zeros(X_train_p.size(0),1).to(device)
print("Data generated and upload to device successfully.")
print("Number of training sets for NN: %d" % (X_train_nn.size(0)))
print("Number of training sets for Physics: %d" % (X_train_p.size(0)))

#############################
## Build an Neural Network ##
#############################
print("\n-------------------------------------------------")
print("Building a Neural Network:")
print("-------------------------------------------------")
layers = torch.tensor([2, 32, 64, 1])
PINN = FCN(layers).to(device)
print("Neural Network constructed and uploaded to device successfully:")
print(PINN) 

##############################
## Train the Neural Network ##
##############################
print("\n-------------------------------------------------")
print("Train the Neural Network:")
print("-------------------------------------------------")
optimizer = optim.Adam(PINN.parameters(), lr=1e-3, amsgrad=False)
number_epochs = 20000
for epoch in range(number_epochs):
    optimizer.zero_grad()
    loss = PINN.loss_PINN(X_train_nn, Y_train_nn, X_train_p, g)
    loss.backward()
    optimizer.step()
    if epoch % 100 == 0:
        print("Epoch: %d, Loss: %.3e" % (epoch, loss.item()))