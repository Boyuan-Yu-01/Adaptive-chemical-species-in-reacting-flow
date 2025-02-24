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

tensor_1 = torch.linspace(0, 1, steps=10)
indicies = np.random.choice(len(tensor_1), size=10, replace=False)
indicies_1 = indicies[0:5]
indicies_2 = indicies[5:]
tensor_2 = tensor_1[torch.tensor(indicies_1)].reshape(-1,1)
tensor_3 = tensor_1[torch.tensor(indicies_2)].reshape(-1,1)
print(tensor_1)
print(tensor_2)
print(tensor_3)
print(indicies_1)
