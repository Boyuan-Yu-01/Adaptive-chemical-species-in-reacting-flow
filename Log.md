# Jan. 14th 2025 
## Summary ##
- Start to consider using __neural network approach__ to constructing __adaptive combustion chemical kinetic model__.

## Literature Review ##
### Sili Deng (ML in Combustion)(closely review her papers after ==2021==): ###
- [link to Google Scholar](https://scholar.google.com/citations?hl=en&user=l-IHllAAAAAJ&view_op=list_works&sortby=pubdate)
- [Deng_literature 1](Sili_Deng/2021_Ji_JPCA_CRNN.pdf)

### Tianfeng Lu (combustion chemistry model reduction): ###
- [link to Google Scholar](https://scholar.google.com/citations?user=w6h7R3oAAAAJ&hl=en&oi=ao)
- [Lu_literature 1](Tianfeng_Lu/2004_Lu_CNF_DRG.pdf)
- [Lu_literature 2](Tianfeng_Lu/2006_Lu_CNF_DRG.pdf)

### Rui Xu ###
- [HyChem 1](Rui_Xu/2018_CNF_Wang_HyChem1.pdf)
- [HyChem 2](Rui_Xu/2018_CNF_Xu_HyChem2.pdf)
- [with Yue Zhang](/Rui_Xu/2023_Zhang_CNF_NNRS.pdf)
### Tarek Echekki ###
- [link to Google Scholar](https://scholar.google.com/citations?user=F1fVUP8AAAAJ&hl=en&oi=ao)

## Candidate Machine Learning Models ##
1. PINN
2. Decision Tree
3. Embedding hard physical constraints
4. Convolutional autoencoder
5. Graph Neural Network

## Problem to be Considered
1. Adapt the number of species at different BCs and/or ICs
2. This might require utilizing sensitivity analysis [link](https://scholar.google.com/scholar?hl=en&as_sdt=0%2C5&q=Accelerate+Global+Sensitivity+Analysis+using+Artificial+Neural+Network+Algorithm%3A+Case+Studies+for+Combustion+%3D%3DKinetic+Model%3D%3D&btnG=)
3. How to preserve mass conservation when we reduce the number of species?
		- some thought of it: the *__master species list__* carries maximum amount of species. At each condition, the species that is not listed in the *__adapted species list__* remains constant
4. Use ==methane== as the example to start with

## Time Line ##
1. January: brainstorm, learn different machine learning models
2. April 20th (around): __AFOSR YIP__ proposal draft submission (around 4-5 pages, rough idea)
3. June 20th (around):  __AFOSR YIP__ proposal submission (full proposal)

==*NB: Winning YIP (Young Investigator Research Programme) can bring some grant to the group.*==

## <span style="color: red;">Done List</span> ##

| Object                                               | Specification                                                                                                                                                                                                                         |
| ---------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| PINN                                                 | - Build the neural network running on GPU by following [Juan Toscano](https://www.youtube.com/watch?v=AXXnSzmpyoI)<br>- [Problem description and interpretation](/PINN_practice/PINN_example.pdf)<br>- [Code](/PINN_practice/PINN.py) |
| [Deng_literature 1](Sili_Deng/2021_Ji_JPCA_CRNN.pdf) | - [Summary](Sili_Deng/Summary_2021_Ji_JPCA_CRNN.md)                                                                                                                                                                                   |
| [Lu_literature 1](Tianfeng_Lu/2004_Lu_CNF_DRG.pdf)   | - [Summary](/Tianfeng_Lu/Summary_2004_Lu_CNF_DRG.md)                                                                                                                                                                                  |
| Graph Neural Network                                 | - [Web-page dedicated in explaining the GNN](https://distill.pub/2021/gnn-intro/)<br>- [Note](GNN_note.pdf)<br>- <span style="color: red;"> HAVEN'T DONE ANY EXAMPLE CODING and the understanding to the GNN is limited</span>   |

## <span style="color: red;">To Do List</span> ##
| Object   | Specification                                     |
| -------- | ------------------------------------------------- |
| GNN Book | [Graph Representation Learning](GNN/GRL_Book.pdf) |

# Jan. 21st 2025 #
## Summary##
- Continue working on GNN
- Reviewing Sili Deng's papers on PINN, etc.
## Logistics ##
- Does fellowship support student with a travel grand? ==NO==
	- A combustion meeting during the Spring break (March) 
- 2025 14th US National Combustion Meeting ###
	- __NO TRAVEL GRANT__ from the fellowship
	- student non-member:   $420 (*NB: $75 dollar discount for early bird or stay at the Westin Copley Place*)-
	- student member:           $400
	- membership price:         $80/ 2yrs
## To Do List ##

| Object            | Specification                                                                                                            |
| ----------------- | ------------------------------------------------------------------------------------------------------------------------ |
| GNN Book          | [Graph Representation Learning](GNN/GRL_Book.pdf)                                                                        |
| Lu's Literature   | [Lu_literature 2](Tianfeng_Lu/2006_Lu_CNF_DRG.pdf)                                                                       |
| Deng's Literature | [link to Google Scholar](https://scholar.google.com/citations?hl=en&user=l-IHllAAAAAJ&view_op=list_works&sortby=pubdate) |


## <span style="color: red;">Done List</span> ##

| Object                                                                                        | Specification                                                                                                                                                                                                                      |
| --------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [Stiff-PINN Chemical Kinetics](/Sili_Deng/stiff_PINN_chem_kinetics.pdf)                       | - [Summary](/Sili_Deng/Summary_stiff_Pinn_chem_kinetics.md)                                                                                                                                                                        |
| [Stiff_NN_ODE](/Sili_Deng/stiff_neural_ODE.pdf)                                               | - [Summary](/Sili_Deng/Summary_stiff_neural_ODE.md)                                                                                                                                                                                |
| [Lu Literature 2](/Tianfeng_Lu/2006_Lu_CNF_DRG.pdf)<br><span style="color: red;"> *** </span> | - This literature provides in detail analysis of DRG in QSSA and PE condition and give example of analyzing using the eigenvalue and eigenvectors of the Jacobian matrix<br>- <span style="color: red;">Summary in progress</span> |
| DRG Tutorial                                                                                  | - [Video link](/Tianfeng_Lu/drg_tutorial/5-24-22_drgSession.mp4)                                                                                                                                                                   |
| GNN                                                                                           | - <span style="color: red;"> IN PROGRESS </span><br>- [Link](GNN/GRL_note.md)                                                                                                                                                      |
| some random thoughts                                                                          | - [random thoughts](randomThought.pdf)                                                                                                                                                                                             |

# Jan. 28th 2025#
## Summary ##
- Continuing working on the GNN
- Gathering data for 0D/1D simulation from Cantera
- How to find out the QSSA species?
## Logistics ##
- Does fellowship covers the summer stipend?                      __YES__
- Membership of Combustion Institute:                                   $20/2yrs for student
- Register for *14th U.S. National Combustion Meeting*:          $475 [confirmation](conference_conf.png)
- ==Stay during the conference==

## <span style="color: red;">Done List</span> ##

| Object             | Specification                          |
| ------------------ | -------------------------------------- |
| flame from Cantera | [Link](/flame/readMe/readMe_master.md) |

# Feb. 5th 2025

## <span style="color: red;">Done List</span> ##

| Object                         | Specification                                                                                                                                                                               |
| ------------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Baseline PINN to ROBER problem | - [Code](ROBER/PINN_ROBER.py)<br>- [readMe_PINN](/ROBER/PINN_ROBER_readMe.md) <br>- [readMe_postprocessing](/ROBER/postprocessing_readMe.md)<br>-[training summary](/ROBER/TrainSummary.md) |
| Stanford Data Validation       | - mean abs error: 0.207 cm/s<br>- max abs error: 1.244 cm/s<br>- min abs error: 0.0003 cm/s                                                                                                 |
| some thoughts                  | SVD-based Model Reduction                                                                                                                                                                   |
# Feb.  11th 2025 & Feb. 18th 2025
*No meeting on Feb. 18th since I caught flu*

## Summary 

__FLAME OBJECT REGENERATION__
	- Restart from the  current generated flame object and refine the flame object with using ==multicomponent== and ==Soret Effect==
	- Compare the regenerated flame object with __Stanford Experiment  Data__
	- Use Tianfeng  Lu's reduced skeletal model  to generate the flame object and compare the result with the  *__full model result__* and *__Stanford Result__*
	- Plot the error with respect to the  PTX

__PINN ROBER PROBLEM__
	- Problem 1: under/over-train the result: the number of parameters exceeds the number of training data points
	- Problem 2: penalize over-training by adding a loss term
	- Problem 3: another physical constraint: law of mass action
another side of PINN: use PINN to predict the QSS species
	eqn1 = y/x^2 *- Use gradient,second gradient chemistry, etc. as references to predict the QSS species

__SVD REACTION MATRIX FOR QSSA PREDICTION__ [Link](/SVD_QSSA/idea.md)

## <span style="color: red;">Done List</span> ##

| Object                                                        | Specification                                                                                                                                                                                                                                       |
| ------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Baseline PINN to ROBER problem                                | -[training summary](/ROBER/TrainSummary.md)<br>- [training scripts](/ROBER/bash/run_scripts.sh)<br>- Not able to solve ROBER problem                                                                                                                |
| Improved Flame Objects                                        | - mean abs error: 0.238 cm/s (0.207 cm/s before)<br>- max abs error: 1.519 cm/s     (1.244 cm/s before)<br>- min abs error: 0.002 cm/s     (0.0003 cm/s before)<br>(<span style="color: red;">all abs error both increases </span>)                 |
| Compare the fls using reduced skeletal species and full model | - [plots](flame/Stanford_fls/sim_exp/allPlots.md)                                                                                                                                                                                                   |
| Directly Solve ROBER Problem                                  | - [code](/SVD_QSSA/unscale/unscale_ROBER.py)                                                                                                                                                                                                        |
| SVD Idea                                                      | - [introduction](/SVD_QSSA/idea.md)<br>- [No go to directly solve it](/SVD_QSSA/unscale/readme.md)                                                                                                                                                  |
| Direct Solve                                                  | - [concentration of A and C](/SVD_QSSA/unscale/plots/A_C.jpg)<br>- [concentration of B](/SVD_QSSA/unscale/plots/B.jpg)                                                                                                                              |
| Immersion Cooling (Two-phase)                                 | -[US-20250063686-A1](https://ppubs.uspto.gov/dirsearch-public/print/downloadBasicPdf/20250063686?requestToken=eyJzdWIiOiIyNDQ3MTM3YS1jODljLTQzNTktOTRhYS1lN2M0OTViZTNmZGMiLCJ2ZXIiOiI3ZWFlYmE0MS03ODcwLTQ1OGQtOTUzOS0xZjY2MDBiYmUxZjkiLCJleHAiOjB9) |

# Feb.  25th
## <span style="color: red;">Done List</span> ##

| Object                                                                                                  | Specification                                                                    |
| ------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------- |
| Obtain the analytical solution to the ROBER problem by assuming species B is in QSS                     | -[introduction](/SVD_QSSA/idea.md)<br>- [steps](/SVD_QSSA/QSSA_B_analytical.pdf) |
| Try to implement QSSA at different time steps by implementing the analytical solutions                  | - [summary](/SVD_QSSA/unscale/plots/summary.md)                                  |
| Try to implement the "scale by the current concentration" and see how eigenvalue and eigenvectors works | - [summary](SVD_QSSA/Scaled_eigen_analysis.pdf)                                  |

# Mar.  4th, 11th, 18th, and 25th
*Conference, spring break, and mid-term*

# Apr. 1st #

## <span style="color: red;">Done List</span> ##
| Object                                                                                                 | Specification                     |
| ------------------------------------------------------------------------------------------------------ | --------------------------------- |
| Stanford [CS224W](https://www.youtube.com/watch?v=JAB_plj2rbA&list=PLoROMvodv4rPLKxIpqhjhPgdQy7imNkDn) | 22/60                             |
| Discrete Analysis of the ROBER problem and extensions                                                  | [details](/SVD_QSSA/discrete.pdf) |
## To Do List for Apr. 8th 
| Object                                                                | Specification                                                 |
| --------------------------------------------------------------------- | ------------------------------------------------------------- |
| understand how to use CVODE to solve PDEs                             | [webpage](https://computing.llnl.gov/projects/sundials/cvode) |
| Try implement policies proposed in the [file](/SVD_QSSA/discrete.pdf) |                                                               |
| Stanford CS 224W (2/3)                                                |                                                               |

