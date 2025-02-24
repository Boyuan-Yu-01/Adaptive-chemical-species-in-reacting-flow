Two NN with different number of layers and neurons per layer are trained. Ir = 1e-3:
	1. 3 middle layers, each layers contain 128 neurons 
	2. 5 middle layers, each layers contain 64 neurons

Training result:
![128_128_128](result_t_plot/128_1_tanh_loss.png)
![plot](result_t_plot/128_1_tanh_concentration.png)
		*Training loss using NN: 128 x 3; last layer activation is tanh*
## Observations ##
1. Both FCNs have __NOT BEEN OVER-TRAINED__: for both $128\times3$ and $64\times 5$ FCN, their training loss is of same trend of the validation loss.
2. __Training step is too large__: both cases do not have steady state even until $2\times10^6th$ epoch.
3. Minimum validation loss: 
				a. $128\times3$ FCN: ~$10^{-7}$
				b. $64\times5$  FCN: ~$10^{-4}$

training takes 3 hrs 37 mins

## <span style="color: red;"> PROBLEM with CURRENT TRAINING</span>
- ==Negative concentration== appears: __lack physical constraints that penalize the negative concentration

![plot](result_t_plot/ill_condition.jpg)
		*Negative concentration appears when the last layer activation function is tanh*
- Training data is from $0s$ to $10^7s$, whereas in [Deng's paper](stiff_PINN_chem_kinetics.pdf), time span from $10^{-5}s$ to $10^{4}s$.
![ill_conditioned](result_t_plot/trained_NN_result/ill_condition.jpg)
			*NN: "64_2.json" --> "NN_parameters" --> last set of parameters*
__potential solution__: 
				1. use functions such as __ReLU__, __logistic sigmoid__, or __softplus__, etc. for the last layer <span style="color: red;"> (FCN structure change) </span>
				2. add a __loss function__ that penalize the negative value
		ReLU:                       $a= max(0,x)$
		logistic sigmoid:      $a = \frac{1}{1+e^{-x}}$
		softplus:                   $a = ln(1+e^x)$


## Training Result Using Softplus and Reduce lr to $1e-6$
### NN: 128 x 3; Last layer activation: Softplus

![plot](result_t_plot/128_2_softplus_concentration.png)
		*Training result using NN: 128 x 3; Last activation function is softplus*
![plot](result_t_plot/64_2_softplus_concentration.png)
		*Training result using NN: 64 x 5; Last activation function is softplus*
![plot](result_t_plot/128_5_softplus_concentration.png)
		*Training result using NN: 128 x 5; last activation function is softplus*
![plot](result_t_plot/128_2_softplus_loss.png)
		*Training loss NN: 128 x 3; last activation function is softplus*
![plot](result_t_plot/64_2_softplus_loss.png)
		*Training loss NN: 64 x 5; last activation function is softplus*
![plot](result_t_plot/128_5_softplus_loss.png)
		*Training loss NN: 128 x 5; last activation function is softplus*

## <span style="color: red;">Improvements </span>
- <span style="color: red;"> MASS CONSERVATION  (not applicable to ROBER problem)</span>
- Fourier-PINN?
- Deng's feed input: log(t)

## After Improvements ##
- avoid over-fitting: there are ~$10^5$ parameters within the neural network, this time we train the neural network with ~ $5 \times 10^5$ number of data. __why didn't choose more?__ My GPU cannot support more data.
- Input has been changed to log(t) s.t. more data has been chosen at the initial state
- $lr = 1e-5$
- total epoches is $5 \times 10^5$

![plot1](result_logt_plot/20_3_logt_loss.png)
![plot1](result_logt_plot/20_3_logt_pred.png)
		*Training result using NN: 20 x 3; Last activation function is softplus
				time spent for training: ==3:46:55==*


![plot1](result_logt_plot/64_5_logt_loss.png)
![plot1](result_logt_plot/64_5_logt_pred.png)
		*Training result using NN: 64 x 5; Last activation function is softplus
				time spent for training: ==20:26:39==*


![plot1](result_logt_plot/128_3_logt_loss.png)
![plot1](result_logt_plot/128_3_logt_pred.png)
		*Training result using NN: 128 x 5; Last activation function is softplus
				time spent for training: ==17:32:47==*

![plot1](result_logt_plot/128_5_logt_loss.png)
![plot1](result_logt_plot/128_5_logt_pred.png)
		*Training result using NN: 128 x 5; Last activation function is softplus
				time spent for training: ==33:28:21==*


## Employ QSSA assumption:
![plot](/ROBER/result_t_plot/QSSA_t.png)
![plot](/ROBER/result_t_plot/QSSA_t_B.png)
		*Training result using NN: 64x 5; Last activation function is softplus
				time spent for training: ==about 17 hrs==*

