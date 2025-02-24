I create this task to try  the POLLU problem and apply PCA to the Jacobian matrix.

POLLU problem contains 20 species and 25 reactions.

The description and solution of this problem using stiff_PINN developed by Dr. Sili Deng is documented in [here](POLLU_Deng.pdf).

When the Jacobian matrix is a constant==(implies constant temperature)==, the equation 
					$\underline{\dot{Y}}=\underline{\underline{A}}\cdot\underline{Y}$
analytical solution:
					$\underline{Y(t)}=e^{\underline{\underline{A}}\cdot{}t}\cdot{}\underline{Y(0)}$
Another way to do it is through the Laplace Transform				
