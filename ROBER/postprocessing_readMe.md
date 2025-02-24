*postprocessing helps to reconstruct the neural network from the dictionary form stored in the ".json" files*

# Class FCN:
*This class helps to produce the neural network prediction and to show the information of the neural network.*
### def __init__(self, model, last_activation):
*Read data from the dictionary, an example of witch is showed in [here](PINN_ROBER_readMe.md). *
<span style="color: red;"> NB: the last layer activation is specifically required to be defined within the function. Remember to check it every time using it. </span>
### def forward(self, x):
*output the neural network prediction, in a tensor form, given input "T"*


### def show_info(self):
*This function prints out the information of the model*

# Functions:
## def load_json(dictionary, file_name):
*This function load the json file and return the __training loss__, __validation loss__, __number of the training epoch__, and a list of model dictionary __models__*

## def reconstruct_NN(model):
*This function helps to reconstruct the NN and output an __FCN object__ "NN"*

### def plot_log_loss(array, legends=None, title='plot',plot_save=False):
*This function helps to plot the loss in a log scale and save the plot if "plot_save" is given.*



