*This paper presents a __two-step method__ to reduce the number of species and elementary reaction.*

*This paper demonstrates the reduction of detailed ethylene oxidation mechanism originally consisting of __70 species, 463 elementary reactions__ to __33 species , 205 elementary reactions__ by first-step, then reduce to __20 species, 16 global reactions__*

## Methods mentioned for order reduction##
#### Skeletal Reduction ####
*Eliminating the unimportant reactions and species based on the application*
- Reaction Rate Analysis
- Jacobian Analysis (requires iterative process)
- ==Computational Singular Perturbation (CSP)==
- ==Directed Relation Graph(DRG)==
#### Partial Equilibrium and Quasi-Steady-State (QSS) ####
*Applying QSS to the skeletal mechanism*
- ==Method of Lifetime Analysis==

## Step 1: Skeletal Reduction Using DRG ##
production rate of species A: 
						$R_A = \sum_{i=1,I} \nu_{A,i} \omega_i$
in which:
						$\omega_i =k_{fi}\sum_{j=1}^k c_j^{v'_{ij}}-k_{bi}\sum_{j=1}^k c_j^{v''_{ij}}$

and the reaction rate:
						$k_{fi} = [A_iT^{n_i}exp(-E_i/RT)]F_i$
<span style="color: red;">NB: In all equations above, i and j designate the i-th elementary reaction and j-th species.</span>

To quantify  the direct influence of one species on another, a normalized contribution of spices B to the production rate of species A,
				$r_{AB}$ is defined as:
							$r_{AB} = \frac{\sum_{i=1,I}|\nu_{A,i}\omega_i\delta_{Bi}|}{\sum_{i=1,I}|\nu_{A,i}\omega_i|}$
	 where $\delta_{Bi}=1$ when i-th elementary reaction involves species B, and 0 otherwise.

In another words, $r_{AB}$ roughly measures the relative error induced in species A due to the removal of species B.

Then select an $\epsilon$ s.t. $r_{AB} < \epsilon$, there is no edge between A and B 
![Lu_1](Lu_2004_1.png)
- DRG can be constructed in linear time proportional to the number of reactions by evaluating the contribution of each elementary reaction to the edges aﬀected by it.
- we select the ‘‘starting set’’ of species (can be just fuel or fuel and NOX)

## Step 2: Further Reduction based on QSS Assumptions ##
*Approximating short time scale species by approximating them to be steady-state*

define:
					$\overline{\tau}_i = \tau_i/\tau_{ch}$, 
where
					$\tau_i = -1/\sum_{r=1}^K \mathbf{R_{ir}\lambda_r}$
			$K$ is the total number of species
			$\mathbf{R_{ir}}$ is the ==radical pointer associated with the i-th mode and the r-th species==,$\lambda_r$ is an eigenvalue of the r-th mode
 
 __==Criteria: reactions with $\overline{\tau}_i < \alpha$ can be considered as SS==__

## Remarks ##
- <span style="color: red;">There is a potential of significant reduction with the method of the DRG for severely restricted parametric range. </span> This statement recognizes the possibility of applying adaptive chemical species.
					
					
