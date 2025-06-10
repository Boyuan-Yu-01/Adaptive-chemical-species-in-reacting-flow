
## Using Perturbation Method to Approximate the Jacobian Matrix

Element at i-th row, j-th column has value:
$$
\frac{\partial S_i^{t}}{\partial S_j^{t-1}}
$$
This value can be approximated by perturbing species j's concentration at the last time step, and then advance one time step. The original concentration is $S_j^t$, and the after perturbed concentration is $S_j^{\prime, t}$. The Jacobian can be approximated as:
$$
\frac{\partial S_i^{t}}{\partial S_j^{t-1}} \approx \frac{S_i^{\prime, t}-S_i^{t}}{S_j^{\prime, t-1}-S_j^{t-1}}=\frac{S_i^{\prime, t}-S_i^{t}}{(1+\delta)S_j^{t-1}} 
$$
Notice that __perturbing each individual species helps to calculate a column in the Jacobian Matrix__. Therefore, this perturbation process is required to iterate # of species times.

## Perturbation Method
__Cantera__ utilises TPX to define the reaction gas. Given a constant temperature, to perturb, i.e., to increase $S_j$'s concentration by small amount ($\delta S_j$,) the pressure will be varied to:
$$
P_{perturbed} = \frac{n_{org}+\delta \cdot S_j}{n_{org}} \cdot P_{org}
$$
The composition of each species will also be changed:
$$
X_{i}^{\prime} =
\begin{cases}
\displaystyle \frac{S_i}{\sum_{k=1}^m S_k + \delta S_j}, & i \ne j \\[1.5ex]
\displaystyle \frac{(1 + \delta) S_j}{\sum_{k=1}^m S_k + \delta S_j}, & i = j
\end{cases}
$$

By these, we can defined a ==perturbed gas object==, execute __one step forward__, then approximate the Jacobian matrix.

## Detail Treatment: Extremely small concentration
Observation: when the concentration of a species is __effectively zero,__ the perturbation can have *divide by zero error*, but it is __still necessary to conduct it.__

The typical machine error (or machine epsilon) is ~$2.22 \times 10^{-16}.$ Therefore, for any species that has concentration less than $1 \times 10^{-16},$ the perturbation will no longer follow rules above. 

Instead:
$$
P_{perturbed} = \frac{n_{org}+\eta}{n_{org}} \cdot P_{org}
$$
$$
X_{i}^{\prime} =
\begin{cases}
\displaystyle \frac{S_i}{\sum_{k=1}^m S_k + \eta}, & i \ne j \\[1.5ex]
\displaystyle \frac{S_j+\eta}{\sum_{k=1}^m S_k + \eta}, & i = j
\end{cases}
$$
where,
$$\eta = 1 \times 10^{-16}$$

## Approximation Methodology
*Approximate $\frac{\partial S^t_i}{\partial S^{t-1}_j}$ as $\dot{S^t_i}/\dot{S^{t-1}_j}$ may not be a good approximation.*

To begin with, the change in concentration of species "i" can be approximated by:
$$
S^{t+1}_i - S^{t}_i = \sum\frac{\partial S_i^t}{\partial S_j^{t-1}} \dot{S^{t-1}_j} \cdot \delta_t
$$
<span style="color: red;">if we approximate the partial term by:</span>
$$
\frac{\partial S_i^{t}}{\partial S_j^{t-1}} \approx \frac{dS^t_i}{dt} / \frac{dS^{t-1}}{dt}
$$
i.e.
$$
\frac{\partial S_i^{t}}{\partial S_j^{t-1}} \approx \dot{S^t_i}/\dot{S^{t-1}_j}
$$

The change in concentration of species "i" then will be written as:
$$
S^{t+1}_i - S^{t}_i = \sum\frac{\dot{S_i^t}}{\dot{S_j^{t-1}}} \dot{S^{t-1}_j} \cdot \delta_t
$$
which is 
$$
S^{t+1}_i - S^{t}_i = \dot{S_i^t}\cdot \delta_t \cdot n
$$
where n is the number of species. 

From this, I believe that <span style="color: red;">we can not approximate the partial differential by the fraction of time differential</span>