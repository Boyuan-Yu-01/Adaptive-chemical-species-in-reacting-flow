The shape of the mechanism:
```json
Mechanism: { 'species': {'H2':{'initial_concentration': None,
						 'net_reaction_rate': [[..., factor_j,...]
											   [..., rate_const_j, ...]
											   [..., [species_multiplier_jk],                                                    ...]
											   [..., [species_exponent_jk], ...]
											  ]
												 
							   }
						 }
			 'reactions': { 'reaction 1': {'reactants': ['H': 1, 'O2': 1]
										   'products': ['O': 1, 'OH': 1]
										   'forward_rate': 123
										   'backward_rate': 321
										  }
										 
						  }

		   }
```
The net reaction rate is calculated by: 
$$
\begin{equation}
\dot{[A_i]} = \sum_{j=1}^{m}\nu_j\cdot k_{->or<-} \cdot \prod_{k=1}^{n}[A_k]^{exp_k}
\end{equation}
$$
	For ==VERSION 2==, an additional step is applied to keep the total number of the molecules as a constant.

At each time step, there will be n molecules generated from the reaction s.t. 
$$
\begin{equation}
n = \sum_{j=1}^{m} \dot{A} \cdot t_{step}
\end{equation}
$$
For constant temperature and pressure, the total number of molecule should be conserved. Therefore, there will be n number of molecules diffused away. The diffused-away gas will have the same composition as the gas remained within the "confined space."

Therefore, an extra term will be add to the end of each equation expressing $[A_i]$:
$$
Term_i = -(\sum_{j=1}^{m}\dot{A} \cdot t_{step}) \cdot \frac{[A_i]}{\sum_{k=1}^{m}[A_i]}
$$
The first term is aforementioned "n", the denominator of the second term will be a constant "$n_0$" s.t. $n_0 = \frac{R_0T}{P}$ 

The extra term can therefore be expressed as:
$$
Term_i = -(n) \cdot \frac{[A_i]}{n_0}
$$