'''This file differ from the "PINN_ROBER_2.py" in the way that
the input is the log of time.
        - physical loss function need to be modified to account for the log of time
        - the input should be change to the log of time, and the number of time chosen should
        be no less than 10^6'''
## import libraries
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

import json
import time
from tqdm import tqdm
import sys

##############################################################################
##                Edit input parameters from bash script                    ##
##############################################################################
layers = torch.tensor([], dtype=torch.int64)                                ## input layers                              ##           
for i in range(1, len(sys.argv)-1):                                         ##                                 
    int_temp = int(sys.argv[i])                                             ##                   
    layers = torch.hstack((layers, torch.tensor([int_temp])))               ##
output_name = sys.argv[-1]                                                  ##
dir = "result_logt_json/"                                                   ##
##############################################################################                                                         
print(layers)
## Device configuration
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
# device = 'cpu'  # for testing

#################################
## Define Neural Network Class ##
#################################
class FCN(nn.Module):
    def __init__(self, layers):
        super(FCN, self).__init__()
        self.activation = nn.Tanh()
        self.last_layer_activation = nn.Softplus()   # activation function for the last layer is softplus
        self.loss_function = nn.MSELoss(reduction = 'mean')
        self.linears = nn.ModuleList([nn.Linear(layers[i], layers[i+1]) for i in range(len(layers)-1)]) # nn.Linear(in_features, out_features, bias=True)
        self.iter = 0
        self.layers = layers
        
        ## Initialise weights and biases
        for i in range(len(layers)-1):
            nn.init.xavier_normal_(self.linears[i].weight.data, gain=1.0)
            nn.init.zeros_(self.linears[i].bias.data) # initialize bias with zeros
    
    def forward(self, x):
        if torch.is_tensor(x) != True:         
            x = torch.from_numpy(x)                
        a = x.float()
        for i in range(len(self.linears)-1):
            z = self.linears[i](a)
            a = self.activation(z)
        z = self.linears[-1](a)
        a = self.last_layer_activation(z)
        return a
    
    def loss_NN(self, X_NN, Y_NN):  
        '''Calculate loss for Neural Network: penalize the difference between predicted and actual values'''
        loss_NN = self.loss_function(self.forward(X_NN), Y_NN)
        return loss_NN
    
    def loss_PDE(self, X_PDE, g):
        '''Calculate loss for Physics: penalize the difference between the predicted and actual values'''
        X = X_PDE.clone()
        X.requires_grad = True
        NN = self.forward(X)        # NN have size n*3
        NN_x = torch.zeros_like(NN, dtype=torch.float32)    # NN_x have size n*3
        # Calculate the gradient for each column in NN
        for i in range(NN.shape[1]):  # Iterate over columns (0, 1, 2)
            temp = autograd.grad(NN[:, i], X, torch.ones_like(NN[:, i]), 
                                    retain_graph=True, create_graph=True)[0]
            temp *= (1/10**X) * (1/np.log(10)) # chain rule for the log of time
            NN_x[:, i] = temp.squeeze() 
        f1 = NN_x[:,[0]] + 0.04 * NN[:,[0]] - 10**4 * NN[:,[1]] * NN[:,[2]]
        f2 = NN_x[:,[1]] - 0.04 * NN[:,[0]] + 3 * 10**7 * NN[:,[1]]**2 + 10**4 * NN[:,[1]] * NN[:,[2]]
        f3 = NN_x[:,[2]] -3*10**7 * NN[:,[1]]**2
        f = torch.hstack((f1,f2,f3))   # f have size n*3, each column represents the PDE for [A], [B], [C]
        loss_PDE = self.loss_function(f,g)
        return loss_PDE
    
    def loss_PINN(self, X_NN, Y_NN, X_PDE, g):
        loss_NN = self.loss_NN(X_NN, Y_NN)
        loss_PDE = self.loss_PDE(X_PDE, g)
        loss_PINN = loss_NN + loss_PDE
        return loss_PINN
    

##############################
## Training Data Generation ##
##############################
print("-------------------------------------------------")
print("Generating Testing Data:")
print("-------------------------------------------------")

## Discretize the domain constrained by ICs
T_log = torch.linspace(-5,5,10**7)

## ICs
A_ic = torch.tensor([1.0])
B_ic = torch.tensor([0.0])  
C_ic = torch.tensor([0.0])
T_log_ic = torch.tensor([10**(-5)])[:,None]
ABC_ic = torch.hstack((A_ic,B_ic,C_ic))[None,:]    # tensor([1.], [0.], [0.]])

alpha = 1       # number of training sets for NN
beta = 5 * 10**5    # number of training sets for Physics
gamma = 200      # number of validation sets for physics

indices = np.random.choice(len(T_log), size=beta+gamma, replace=False)
indices_beta = indices[0:beta+1]        # training seeds for Physics
indices_gamma = indices[beta+1:]         # validation seeds for Physics
T_log_p = T_log[torch.tensor(indices_beta)].reshape(-1,1)
T_log_p = torch.vstack((T_log_ic,T_log_p))
T_log_validate = T_log[torch.tensor(indices_gamma)].reshape(-1,1)   # validation sets for Physics
T_log_validate = torch.vstack((T_log_ic, T_log_validate))

## Move training data to GPU
T_log_ic = T_log_ic.float().to(device)
T_log_p = T_log_p.float().to(device)
T_log_validate = T_log_validate.float().to(device)
ABC_ic = ABC_ic.float().to(device)
g = torch.zeros(T_log_p.shape[0],3).float().to(device)
g_validate = torch.zeros(T_log_validate.shape[0],3).float().to(device)
print("Data generated and upload to device successfully.")
print("Number of training sets for NN: %d" % (T_log_ic.size(0)))
print("Number of training sets for Physics: %d" % (T_log_p.size(0)))

#############################
## Build an Neural Network ##
#############################
print("\n-------------------------------------------------")
print("Building a Neural Network:")
print("-------------------------------------------------")

PINN = FCN(layers).to(device)
print("Neural Network constructed and uploaded to device successfully:")
print(PINN) 

##############################
## Train the Neural Network ##
##############################
print("\n-------------------------------------------------")
print("Train the Neural Network:")
print("-------------------------------------------------")
optimizer = optim.Adam(PINN.parameters(), lr=1e-5, amsgrad=False)
# number_epochs = 2000000
number_epochs = 500000
loss_train = []     # store training loss
loss_validate = []  # store validation loss
NN_selected = []        # store NN parameters
cnt = 0     # count the number of stored NN parameters to 'NN_dict'
train_start = time.time()
for epoch in tqdm(range(number_epochs)):
    optimizer.zero_grad()
    loss = PINN.loss_PINN(T_log_ic, ABC_ic, T_log_p, g)
    loss.backward()
    optimizer.step()
    if epoch % 100 == 0:
        loss_validate_temp = PINN.loss_PINN(T_log_ic, ABC_ic, T_log_validate, g_validate)
        loss_train.append(loss.item())
        loss_validate.append(loss_validate_temp.item())
        if cnt == 0:
            value = f"epoch_{epoch}"
            PINN_dict = PINN.state_dict()
            json_PINN = {key: tensor.detach().cpu().tolist() for key, tensor in PINN_dict.items()}     # convert NN paramems to json-recordable format
            dict_temp = {}
            dict_temp['epoch'] = value
            dict_temp['params'] = json_PINN
            dict_temp['min_train_loss'] = loss.item()
            dict_temp['min_validate_loss'] = loss_validate_temp.item()
            NN_selected.append(dict_temp)
            cnt += 1
        elif loss.item() < NN_selected[-1]['min_train_loss'] or loss_validate_temp.item() < NN_selected[-1]['min_validate_loss']:
            value = f"epoch_{epoch}"
            PINN_dict = PINN.state_dict()
            json_PINN = {key: tensor.detach().cpu().tolist() for key, tensor in PINN_dict.items()}     # convert NN paramems to json-recordable format
            dict_temp = {}
            dict_temp['epoch'] = value 
            dict_temp['params'] = json_PINN
            dict_temp['min_train_loss'] = loss.item()
            dict_temp['min_validate_loss'] = loss_validate_temp.item()
            NN_selected.append(dict_temp)
            cnt += 1
        # print("Epoch: %d, Training Loss: %.3e, Validation Loss: %.3e" % (epoch, loss.item(), loss_validate_temp.item()))
train_end = time.time()
training_summary = {}
training_summary['train_loss'] = loss_train
training_summary['validate_loss'] = loss_validate
training_summary['NN_parameters'] = NN_selected

with open(dir+output_name, "w") as f:
    json.dump(training_summary, f, indent=4)
        
print("-------------------------------------------------")
print(f"Training Completed:\n\t{cnt} NN parameters are stored in "+output_name+".\n--\t{train_end-train_start} seconds are taken to train {number_epochs} epochs.")