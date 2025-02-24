*NB: "PINN_ROBER.py" has last layer activation function as tanh
    "PINN_ROBER_2.py" has last layer activation function as softplus* 
	 continuously monitoring the GPU usage: =="watch -n 1 nvidia-smi"==
## Device configuration: ##
- Using GPU ('cuda') if available, otherwise use CPU
- To check GPU usage, type 'watch -n 1 nvidia-smi' to monitor the GPU usage

## Define the neural network ##
*The neural network is defined by the class FCN that has parent function nn*
### def__init__(self, layers)
- define the fully connected neural network
- This method determines:
	- activation function to be ==tanh function==
	- loss function to be ==Mean Square Error==
- parameters for the FCN class:
	- activation
	- loss_function
	- linears
	- iter
	- layers

### forward(self, x)
*forward function helps to pass the information forward and yield the prediction $NN(\underline{x})$.*
- $\underline{x}$ should be a $n \times p$ matrix where $p$ is the number of input each time goes into the FCN

### loss_NN(self, X_NN, Y_NN)
*loss_NN gives the MSE of the neural network error. loss_NN penalize  the difference between given value $y(\underline{x})$ and the forward output $NN(\underline{x})$*

### loss_PDE(self, X_NN, Y_NN)
*loss_PDE gives the MSE of the physics represented by PDEs. loss_PDE penalize the difference between the 'physics' $Phy(NN(\underline{x}))$calculated using the neural network and the 'real physics' $Phy(y(\underline{x}))$ 
- The first derivative are stored in a $n \times p$ matrix given they are only a function of time.
- Each column represents a parameter and row represents the *__time evolution__* of the variable

### loss_PINN(self, X_NN,Y_NN, X_PDE, g)
*loss_PINN calls loss_PDE(...) and loss_NN(...) and take the sum.* 
*==In future, if necessary, a tuning parameter can be added so that loss_PDE and loss_NN have different weight==*

## main
*main part __(1)__ generates the training datasets and validation dataset, __(2)__ transfer data to GPU, __(3)__ build the FCN, and __(4)__ train the neural network.*

### Generate the Test Dataset and Validation Dataset##
- In this problem, only T (time) is the input, so we discretize the time
- Only initial condition (__initial concentration of each species__) presents
- stack the initial conditions s.t. they forms a $(p\times 1)$ matrix.
- $\alpha$, $\beta$, $\gamma$ are parameters for number of __training sets for NN__, __training sets for Physics__, and __validation sets__. 
- Randomly selected $\alpha$, $\beta$, and $\gamma$ parameters in time series (T) for the training and the validation purpose. $\alpha$ is one in this case corresponding to the only-existing initial condition.
- __Vertically stack__ the T variable and the expected value for $\underline{}ic$, $\underline{}bc$, and$\underline{}p(hysics)$
- All variables will move to __GPU__ for next step calculation

### Build an Neural Network ###
- use layers to define the FCN. For example,
```python
layers = torch.tensor([1, 128, 128, 128, 3])
PINN   = FCN(layers).to(device)
```
*This snippet constructed a $\underline{3}$ layer fully connected neural network that has $\underline{1}$ input and $\underline{3}$ output. Each neural layer contains $\underline{128}$ neurons.*

### Train the Neural Network 
- Using Adam optimizer, having 2e6 training epoches
- Create __'loss_train'__, __'loss_validate'__, and __'NN_selected'__ to store __training loss__, __validation loss__, and __selected neural networks__. stored neural networks are ones with good performance
- Every 100 step print the __1.__ number of epoch, __2.__ training loss, and __3.__ validation loss

### Outputs
The output, as one dictionary, contains three item-pairs: "loss_train", "loss_validate", and "NN_selected". First two are 1D list that contains the training loss and validation loss per 100 epoches.

"NN_selected" contained a list of dictionary objects. An example of this kind of dictionary that has three layers (one input with 3 neurons, one hidden with three neurons, and one output layer with three neurons) is demonstrated in the following section:
```json
dic_one = {
    "epoch": "epoch_10",
    "params": {
        "linears.0.weight": [
            [0.2, -0.5, 0.3], 
            [0.1, 0.7, -0.2], 
            [-0.3, 0.4, 0.6]
        ],
        "linears.0.bias": [0.1, -0.2, 0.05],
        
        "linears.1.weight": [
            [0.5, -0.1, 0.4], 
            [-0.3, 0.8, 0.2], 
            [0.6, -0.7, 0.3]
        ],
        "linears.1.bias": [0.05, -0.1, 0.2],
        
        "linears.2.weight": [
            [0.3, -0.2, 0.5], 
            [-0.6, 0.4, 0.1], 
            [0.2, 0.7, -0.3]
        ],
        "linears.2.bias": [0.0, 0.1, -0.05]
    },
    "min_train_loss": 0.0123,
    "min_validate_loss": 0.0345
}
```