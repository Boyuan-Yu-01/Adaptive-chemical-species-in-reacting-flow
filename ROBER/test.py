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

        
#################################
## Define Neural Network Class ##
#################################

# def plot_log_loss(array, legends=None, title='plot',plot_save=False):
#     '''Plot a dataset with a logarithmic y-scale. arrays is a n by 3 numpy array, where n is he number of data points.'''
#     plt.figure(figsize=(16, 12))
#     x, y1, y2 = array[:, 0], array[:, 1], array[:, 2]
#     label1 = legends[0] if legends else f"(y1)"
#     label2 = legends[1] if legends else f"(y2)"
#     plt.plot(x, y1, 'b-', label=label1)
#     plt.plot(x, y2, 'r--', label=label2)
#     plt.yscale("log")  # Set y-axis to log scale
#     plt.xlabel("epoches")
#     plt.ylabel("loss")
#     plt.legend()
#     plt.grid(True, which="both", linestyle="--", linewidth=0.5)
#     plt.title(title)
#     plt.savefig(plot_save)
#     # plt.show()
#     plt.close()
    
# def reconstruct_NN(model):
#     ''' This function reconstruct the FCN model from the model, a dictionary as illustrated in 
#     "PINN_ROBER_readMe", dic_one.
#     This function returns an object that is an instance of the class FCN_reconstructed.'''
#     params = model["params"]
#     state_dict = {key:torch.tensor(value, dtype=torch.float) for key, value in params.items()} 
#     NN = FCN_reconstructed(model)
#     NN.load_state_dict(state_dict)   
#     return NN

# def load_json(directory, file_name):
#     '''Load the json file and return the training loss, validation loss, epoch and models'''
#     # Load the json file
#     with open(directory+file_name, "r") as file:
#         data = json.load(file)
#         train_loss = data['train_loss']
#         validate_loss = data['validate_loss']
#         models = data['NN_parameters']
#         epoch = [i * 100 for i in range(len(train_loss))]
#     return train_loss, validate_loss, epoch, models

# directory = 'result_json/'
# file_name = '128_5_softplus.json'

#################################################################################################################################################
## Test the the structure of the model dictionary stored in the json file
# train_loss, validate_loss, epoch, models = load_json(directory, file_name)

# model_1 = models[-1]["params"]
# print(len(model_1.items()))
# model_1_keys= model_1.keys()
# layer_names = sorted([key for key in model_1.keys() if "weight" in key], key=lambda x: int(x.split(".")[1]))  # Extracts correct layer index
# print(model_1_keys)

# for i in range(int(len(model_1.items())/2)):
#     layer = model_1[layer_names[i]]
#     layer_size = [len(layer), len(layer[0])]
#     print(f"Layer {i}: {layer_size[0]} x {layer_size[1]}")
#################################################################################################################################################

# ## DIY the forward function using the model dictionary
# T = torch.linspace(0, 200, 1000)[:, None]
# T = T.reshape(-1, 1)
# ABC = torch.empty((0,3))
# _, _, _, models = load_json(directory, file_name)
# model = models[-1]["params"]
# num_layers = int(len(model.items())/2)
# for t in T:
#     x = t
#     for i in range(num_layers-1):
#         if torch.is_tensor(x) != True:
#             x = torch.Tensor(x)
#         A = torch.tensor(model[f"linears.{i}.weight"])
#         b = torch.tensor(model[f"linears.{i}.bias"])
#         z = torch.matmul(A, x) + b
#         x = nn.Tanh()(z)
#     A = torch.tensor(model[f"linears.{num_layers-1}.weight"])
#     b = torch.tensor(model[f"linears.{num_layers-1}.bias"])
#     z = torch.matmul(A, x) + b
#     x = nn.Softplus()(z)
#     # x = nn.Tanh()(z)
#     x = x[None,:]
#     ABC = torch.vstack((ABC, x))

# ABC = ABC.numpy()
# print(ABC.shape)
# A = ABC[:,0]
# B = ABC[:,1]
# C = ABC[:,2]
# print(max(B))
# plt.plot(T,ABC)
# # plt.xscale("log")   
# plt.legend(["[A]","[B]","[C]"], loc="upper right")
# plt.xlabel("Time[s] in log scale")
# plt.ylabel("Concentration")
# plt.title("Species Concentration using forward NN: 64 x 5 \nlast layer has Softplus activation")
# plt.show()

