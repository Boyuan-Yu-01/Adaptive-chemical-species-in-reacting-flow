'''This programme is established to process the data from the json file(s) under the directory 'trained_NN_result'. 
Main taskes include:    1. plot the training and validation loss
                        2. plot the species concentration using selected NN model'''

# Import libries
import json
import torch
import torch.nn as nn
import matplotlib.pyplot as plt
import numpy as np

directory = 'result_t_json/'
directory_plot = 'result_t_plot/'
file_name_0 = 'QSSA_t.json'
file_name_1 = '128_5_softplus.json'

######################
## define functions ##
######################
class FCN_reconstructed(nn.Module):
    '''This class helps to reconstruct the FCN model from a dictionary.
    This class contains methods to forward pass the model and calculate the NN prediction given the input data.'''
    
    def __init__(self,model, last_activation = None):
        super(FCN_reconstructed, self).__init__()
        # Attributes of the model
        self.epoch = model["epoch"]  # Fetch 'epoch' from the dictionary
        self.params = model["params"]  # Fetch 'params' from the dictionary
        self.min_train_loss = model["min_train_loss"]  # Fetch 'min_train_loss'
        self.min_validate_loss = model["min_validate_loss"]  # Fetch 'min_validate_loss'
        self.activation = nn.Tanh()
        if last_activation:
            self.last_layer_activation = last_activation
        else:
            self.last_layer_activation = self.activation
        self.linears = nn.ModuleList()
        layer_sizes = []
        layer_names = sorted([key for key in self.params.keys() if "weight" in key], key=lambda x: int(x.split(".")[1]))  # Extracts correct layer index

        for layer in layer_names:
            weight_matrix = self.params[layer]
            input_size = len(weight_matrix[0])
            output_size = len(weight_matrix)
            layer_sizes.append((input_size, output_size))
        
        for input_size,output_size in layer_sizes:
            self.linears.append(nn.Linear(input_size, output_size))
        
    
    def forward(self, T): ## x should be a n by 1 tensor. Output is a n by 3 tensor
        ABC = torch.empty((0,3))
        if torch.is_tensor(T) != True:         
            T = torch.tensor(T, dtype=torch.float)
        num_layers = int(len(self.params.items())/2)
        for t in T:
            x = t
            for i in range(num_layers-1):
                if torch.is_tensor(x) != True:
                    x = torch.Tensor(x)
                A = torch.tensor(self.params[f"linears.{i}.weight"])
                b = torch.tensor(self.params[f"linears.{i}.bias"])
                z = torch.matmul(A, x) + b
                x = self.activation(z)
            A = torch.tensor(self.params[f"linears.{num_layers-1}.weight"])
            b = torch.tensor(self.params[f"linears.{num_layers-1}.bias"])
            z = torch.matmul(A, x) + b
            x = self.last_layer_activation(z)
            x = x[None,:]
            ABC = torch.vstack((ABC, x))
        return ABC
            
    def show_info(self):
        '''Print the information of the model'''
        print(f"Epoch: {self.epoch}")
        print(f"The training loss: {self.min_train_loss}")
        print(f"The validation loss: {self.min_validate_loss}")
        
def load_json(directory, file_name):
    '''Load the json file and return the training loss, validation loss, epoch and models'''
    # Load the json file
    with open(directory+file_name, "r") as file:
        data = json.load(file)
        train_loss = data['train_loss']
        train_loss = np.array(train_loss)
        validate_loss = data['validate_loss']
        validate_loss = np.array(validate_loss)
        models = data['NN_parameters']
        epoch = [i * 100 for i in range(len(train_loss))]
        epoch = np.array(epoch)
        train_loss = train_loss.reshape(-1, 1)
        validate_loss = validate_loss.reshape(-1, 1)
        epoch = epoch.reshape(-1, 1)
    return train_loss, validate_loss, epoch, models
    
def reconstruct_NN(model, last_activation = None):
    ''' This function reconstruct the FCN model from the model, a dictionary as illustrated in 
    "PINN_ROBER_readMe", dic_one.
    This function returns an object that is an instance of the class FCN_reconstructed.'''
    params = model["params"]
    state_dict = {key:torch.tensor(value, dtype=torch.float) for key, value in params.items()} 
    NN = FCN_reconstructed(model, last_activation)
    NN.load_state_dict(state_dict)   
    return NN

def plot_log_loss(array, legends=None, title='plot',plot_save=False):
    '''Plot a dataset with a logarithmic y-scale. arrays is a n by 3 numpy array, where n is he number of data points.'''
    plt.figure(figsize=(16, 12))
    x, y1, y2 = array[:, 0], array[:, 1], array[:, 2]
    label1 = legends[0] if legends else f"(y1)"
    label2 = legends[1] if legends else f"(y2)"
    plt.plot(x, y1, 'b-', label=label1)
    plt.plot(x, y2, 'r--', label=label2)
    plt.yscale("log")  # Set y-axis to log scale
    plt.xlabel("epoches")
    plt.ylabel("loss")
    plt.legend()
    plt.grid(True, which="both", linestyle="--", linewidth=0.5)
    plt.title(title)
    plt.savefig(plot_save)
    # plt.show()
    plt.close()

def plot_concentration(T, concentration, legend, title, plot_save=False):
    '''Plot the concentration of the species using the NN model'''
    plt.figure(figsize=(16, 12))
    plt.plot(T, concentration)
    plt.legend(legend, loc="upper right")
    plt.xscale("log")
    plt.xlabel("Time[s]")
    plt.ylabel("Concentration")
    plt.title(title)
    plt.savefig(plot_save)
    # plt.show()
    plt.close()

tl, vl, ep, md =  load_json(directory, file_name_0) # call the function to load the json file

NN = reconstruct_NN(md[-1], last_activation=nn.Softplus()) # reconstruct the NN model from the last model in the list
print(NN.show_info()) # print the information of the model
plot_log_loss(np.hstack((ep, tl, vl)), legends=[("train loss"), ("validation loss")], title = "NN: 128 x 3, lr=1e-6", plot_save=directory+"128_5_tanh_loss.png")

## given time, get the concentration of the species using "forward" method
T = torch.linspace(0, 10000, 1000)[:, None].reshape(-1,1)
ABC = NN.forward(T)
ABC = ABC.detach().numpy()
B = ABC[:,1]
plot_concentration(T, ABC, legend=["[A]","[B]","[C]"], title="Species Concentration using forward NN: 64 x 5 \nlast layer has Tanh activation", plot_save=directory_plot+"QSSA_t.png")

plot_concentration(T, B, legend=["[B]"], title="Species Concentration using forward NN: 64 x 5 \nB", plot_save=directory_plot+"QSSA_t_B.png")