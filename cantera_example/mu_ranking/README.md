All files under this directory are made in attempt to:
    (i) Use constant volume reactor for stoichiometric $CH_4$ and $O_2$ at P = 1 atm and T = 2000 K as an example case
    (ii) find out the net_production_rates at each time step for each species
    (iii) for each time step, rank $\frac{\frac{d[S_i]}{dt}\cdot \delta t}{[S_i]}$ 

## "mu_ranking.py"
- In this script, I chose two sets of species, and plot there dimensionless net production rate ($\mu$.) The x axis is species name, the y axis is time, and the z axis is $\mu$.

__Set 1:__ {"CH4", "CO2", "H2O", "O2", "C2H6", "C2H4", "C2H2", "OH", "H"}
![p](plots/set1_mu.png)
__Set 2:__ {"CH4", "CO2", "H2O", "O2", "C2H2", "OH", "H"}
![p](plots/set2_mu.png)
Problem(s): 
1. Numerical problem, especially for species that will eventually depleted:
Concentration of $C_2H_4$ & $C_2H_6$ eventually goes to 1e-19 level.

# "mu_ranking_t_step.py"
Given some time_step(s) of interest, the function __plotter__ will plot the dimensionless net production rate vs species with a descending order.

## Plots from FFCM II

![p](plots/mu_0.00e+00.png)
![p](plots/mu_4.00e-06.png)
![p](plots/mu_8.00e-06.png)
![p](plots/mu_1.05e-05.png)
![p](plots/mu_1.30e-05.png)
![p](plots/mu_1.41e-05.png)
![p](plots/mu_1.52e-05.png)
![p](plots/mu_1.63e-05.png)
![p](plots/mu_1.74e-05.png)
![p](plots/mu_1.86e-05.png)
![p](plots/mu_1.97e-05.png)
![p](plots/mu_2.08e-05.png)
![p](plots/mu_2.19e-05.png)
![p](plots/mu_2.30e-05.png)
![p](plots/mu_2.44e-05.png)
![p](plots/mu_2.58e-05.png)
![p](plots/mu_2.72e-05.png)
![p](plots/mu_2.86e-05.png)
![p](plots/mu_3.00e-05.png)

__Similar plots are made from 21 species__

## 21 Species

![p](plots/21_species/mu_4.00e-06.png)
![p](plots/21_species/mu_8.00e-06.png)
![p](plots/21_species/mu_1.05e-05.png)
![p](plots/21_species/mu_1.30e-05.png)
![p](plots/21_species/mu_1.41e-05.png)
![p](plots/21_species/mu_1.52e-05.png)
![p](plots/21_species/mu_1.63e-05.png)
![p](plots/21_species/mu_1.74e-05.png)
![p](plots/21_species/mu_1.86e-05.png)
![p](plots/21_species/mu_1.97e-05.png)
![p](plots/21_species/mu_2.08e-05.png)
![p](plots/21_species/mu_2.19e-05.png)
![p](plots/21_species/mu_2.30e-05.png)
![p](plots/21_species/mu_2.44e-05.png)
![p](plots/21_species/mu_2.58e-05.png)
![p](plots/21_species/mu_2.72e-05.png)
![p](plots/21_species/mu_2.86e-05.png)
![p](plots/21_species/mu_3.00e-05.png)

## Observations:
1. $CH_4$ and $O_2$ always have insignificant dimensionless net production rate
2. $H$ also has insignificant dimensionless net production rate
3. Between $1.4e-5$ and $1.5e-5$, some radicals spikes in dimensionless net production rate