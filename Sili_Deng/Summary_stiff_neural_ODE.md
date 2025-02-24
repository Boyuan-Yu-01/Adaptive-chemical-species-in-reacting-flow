*This paper includes a theoretical and practical methods to relax the stiffness of the ODE that is solved by neural networks.*

*This paper utilizes the example of __ROBER__ (3 species, 3 reactions) and   __POLLU__ (20 species, 25 reactions) to demonstrate how PINN fails due to stiffness that may be solved by scaling.*

*This paper ==resolve the stiffness by scaling==, whereas another paper, purposed by the same author [summary link](Summary_stiff_PINN_chem_kinetics.md) ==resolve the stiffness by employing QSSA.==*

## Theory Explanation ##

- The stiffness relates to the eigenvalues of the Jacobin matrix:
	- resolving fast processes $\xrightarrow{}$ low stiffness
	- resolving slow processes $\xrightarrow{}$ high stiffness
	- ==Stiff_PINN solution==: QSSA
	- ==Stiff_NN_ODE==: scaling

__Methods Reducing Computational Cost:__
- ==QuadratureAdjoint:==
	- many solvers contain a scheme known as dense output for generating a high order interpolation by reusing the internal computations of the steps.
	- many solvers contain a scheme known as dense output for generating a high order interpolation by reusing the internal computations of the steps.
- ==IMEX (implicit-explicit ODE solver):==
	- $f = f_i + f_e$

__Equation Scaling__
					$\frac{dy(t)}{dt} = NN\big(y(t), t\big) \frac{y_\text{scale}}{t_\text{scale}}$
					$y_\text{scale} = y_\text{max} - y_\text{min}$
					$t_\text{scale} = t_1 - t_0$
The loss function is expressed as:
					$L(\theta) = MAE\left(\frac{y(t)^{\text{model}}}{y_\text{scale}}, \frac{y(t)^{\text{obs}}}{y_\text{scale}}\right)$
