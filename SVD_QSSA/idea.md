start from ROBER PROBLEM:

$$
\begin{equation}
\frac{d[A]}{dt} = -k_1[A] + k_3[B][C]
\end{equation}
\tag{1}
$$$$
\begin{equation}
\frac{d[B]}{dt} = k_1[A] - k_2[B]^2 - k_3[B][C]
\end{equation}
\tag{2}
$$
$$
\begin{equation}
\frac{d[C]}{dt} = k_2[B]^2
\end{equation}
\tag{3}
$$

Summarize above into a matrix format:
$$
\begin{bmatrix}
\dot{[A]} \\ \dot{[B]} \\ \dot{[C]}
\end{bmatrix} = 
\begin{bmatrix}
-k_1 & k_3 & 0 \\ k_1 & -k_3 & -k_2 \\ 0 & 0 & k_2
\end{bmatrix} \cdot 
\begin{bmatrix}
[A] \\ [B][C] \\ [B]^2
\end{bmatrix}
\tag{4}
$$
The eigenvalue of the __K__-matrix has extremely significant dominant mode and therefore difficult to numerically solve it. Therefore, a scaling should be considered:
$$
\begin{equation}
	\tilde{[A]} = \alpha \cdot [A]
\end{equation}
\tag{5}
$$
$$
\begin{equation}
	\tilde{[B]} = \beta \cdot [B]
\end{equation}
\tag{6}
$$
$$
\begin{equation}
	\tilde{[C]} = \gamma \cdot [C]
\end{equation}
\tag{7}
$$
By conducting chain rule, the equation (4) can be written as:
$$
\begin{equation}
\begin{bmatrix}
1/\alpha & 0 & 0 \\ 0 & 1/\beta & 0 \\ 0 & 0 & 1/\gamma
\end{bmatrix} \cdot 
\begin{bmatrix}
\dot{[\tilde{A}]} \\ \dot{[\tilde{B}]} \\ \dot{[\tilde{C}]}
\end{bmatrix} = 
\begin{bmatrix}
-k_1 & k_3 & 0 \\ k_1 & -k_3 & -k_2 \\ 0 & 0 & k_2
\end{bmatrix} \cdot 
\begin{bmatrix}
\frac{1}{\alpha}[\tilde{A}] \\ \frac{1}{\beta}\frac{1}{\gamma}[\tilde{B}][\tilde{C}] \\ \frac{1}{\beta^2}[\tilde{B}]^2
\end{bmatrix}
\tag{8}
\end{equation}
$$
Consider eigen-decompose the __K__-matrix, s.t. $K=QDQ^{-1}$
$$
\begin{equation}

\begin{bmatrix}
\dot{[\tilde{A}]} \\ \dot{[\tilde{B}]} \\ \dot{[\tilde{C}]}
\end{bmatrix} = 
\begin{bmatrix}
\alpha & 0 & 0 \\ 0 & \beta & 0 \\ 0 & 0 & \gamma
\end{bmatrix} \cdot
\begin{bmatrix}
-k_1 & k_3 & 0 \\ k_1 & -k_3 & -k_2 \\ 0 & 0 & k_2
\end{bmatrix}
 \cdot 
\begin{bmatrix}
1/\alpha & 0 & 0\\ 0 & 1/\beta \gamma& 0 \\ 0 & 0 & 1/\beta^2
\end{bmatrix} \cdot
\begin{bmatrix}
[\tilde{A}] \\ [\tilde{B}][\tilde{C}] \\ [\tilde{B}]^2
\end{bmatrix}
\tag{8}
\end{equation}
$$
We can __tune__ $\alpha$, $\beta$, and $\gamma$ s.t. eigenvalues can be comparable and therefore the simulation can be conducted in a more accurate/fast way.
__The eigenvalues of this matrix is__: $0, \frac{\gamma}{\beta^2}k_2, and -k_1-\frac{k_3}{\gamma}$


## Questions associate with this method ##
1. For most reactions, the number of reactions is larger than the number of species. __SVD decomposition or POD__ should be considered. The target is to __reduce species__
	- Latent SVD
2. Identify __QSSA__ species using __SVD__: By deleting the reacting species, we are effectively assuming that the species is not reacting. i.e. $[\dot{A}] = 0$ or  $\dot{[\tilde{A}]}=0$ both means that species A at current time step is assume to be QSS.