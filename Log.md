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
| Object                                    | Specification                                                 |
| ----------------------------------------- | ------------------------------------------------------------- |
| understand how to use CVODE to solve PDEs | [webpage](https://computing.llnl.gov/projects/sundials/cvode) |
| Try implement policies proposed in the    | [file](/SVD_QSSA/discrete.pdf)                                |
| Stanford CS 224W (2/3)                    |                                                               |

# Apr. 8th
## <span style="color: red;">Done List & Questions</span> ##
##
| Object                               | Specification                                                                                                                                                                                                                                                                       |
| ------------------------------------ | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| .cti to .yaml                        | - reaction 2 & 3<br>- reaction 8 & 9<br>- reaction 33 & 34<br>- (duplicate reaction, meaning of (+M))<br>- [yaml](SVD_QSSA/graph/FFCMy_12_modified.yaml)<br>- [cti](SVD_QSSA/graph/FFCMy_12_modified.cti)                                                                           |
| code converting scheme to graph      | - [code](/SVD_QSSA/graph/model_state.py)<br>-- prerequisite: download [graphviz](https://graphviz.gitlab.io/)<br>-- generating graph: dot -Tpng script.gv -o graph.png<br>- [skeletal](/SVD_QSSA/graph/graphviz/skeletal.png)<br>- [12 species](SVD_QSSA/graph/graphviz/12_mod.png) |
| a very exciting paper                | - [link](https://pubs.acs.org/doi/pdf/10.1021/j100103a028)                                                                                                                                                                                                                          |
| mass conservation when applying QSSA | - discuss during the meeting                                                                                                                                                                                                                                                        |
|                                      |                                                                                                                                                                                                                                                                                     |

# Apr. 15th #

## <span style="color: red;">Done List</span> ##

| Object                                                                             | Specification                                                                                                                                                                                                                                                                     |
| ---------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| directly solve ROBER problem using BDF                                             | - BDF solving ROBER problem: 2.96s<br>- [readme](/SVD_QSSA/BDF_QSSA/README.md)                                                                                                                                                                                                    |
| Code up a solver for constant TP reaction using BDF. It reqires scheme as an input | - [dictionary structure](SVD_QSSA/BDF_QSSA/12_species/mech_structure.md)<br>- [code (contains a class)](/SVD_QSSA/BDF_QSSA/12_species/constant_TP_reaction.py)<br>- [constant TP using 21 species and 12 species reduced model](SVD_QSSA/BDF_QSSA/12_species/model_comparison.md) |
| comparison (ver1 vs ver2) (ver2 vs cantera)                                        | - [ver1vsver2](SVD_QSSA/BDF_QSSA/12_species/plots/version_comparison.jpg)<br>- [ver2vscantera](SVD_QSSA/BDF_QSSA/12_species/plots/self_vs_cantera.jpg)                                                                                                                            |
| Updated discrete analysis                                                          | - [details](/SVD_QSSA/discrete.pdf)                                                                                                                                                                                                                                               |

# Apr. 22nd #
## <span style="color: red;">Done List</span> ##

| Object                                                                                | Specification                                                                                                                                     |
| ------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------- |
| online example of using BDF integration scheme to solve the constant pressure problem | - [Link](https://cantera.org/dev/_downloads/6a24950c616ecb6f605627b4a3648054/custom.py)                                                           |
| Cantera Iterative numerical scheme to solve ODE                                       | - [Link](https://cantera.org/dev/reference/onedim/nonlinear-solver.html)<br>- *Numerical methods for ordinary differential equations*, Chapter 15 |

# Apr. 29th & May 6th
Final exams
# May 14th #

## <span style="color: red;">Done List</span> ##

| Object                                         | Specification                                                                                                                                                                       |
| ---------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| RMG: n-Dodecane example                        | - [mechanism generated using FFCM I](rmg_copy/nDodecane/cantera/chem.cti)<br>- challenge using FFCM II: [README](/rmg_copy/README.md)                                               |
| Use cantera to solve homogeneous reactions     | - [README](cantera_example/README.md)<br>- [python script](cantera_example/reactors.py)                                                                                             |
| Step 1: Find dimensionless net production rate | - [code 1](cantera_example/mu_ranking/mu_ranking.py)<br>- [code 2](cantera_example/mu_ranking/mu_ranking_t_step.py)<br>- ranking $\mu$ [Link](cantera_example/mu_ranking/README.md) |

## Ongoing List
| Object                           | Specification                                  |
| -------------------------------- | ---------------------------------------------- |
| Step 2: Find the Jacobian Matrix | - [code](cantera_example/Jacobian/jacobian.py) |

# May 19th #
## <span style="color: red;">Done List</span> ##

| Object                                         | Specification                                                                                           |
| ---------------------------------------------- | ------------------------------------------------------------------------------------------------------- |
| regenerate: $C_{12}H_{26}$ reaction mechanism  | - [.cti file](rmg_copy/nDodecane/chem.cti)<br>- [annotated .cti](rmg_copy/nDodecane/chem_annotated.cti) |
| redo: net production rate                      | - [README](cantera_example/npr_ranking/README.md)                                                       |
| add: concentration history by 21 species model | - [plots](cantera_example/const_vol_reactions_scheme_comperison/plots_summary.md)                       |
| Jacobian matrix perturbation                   | - [README](cantera_example/Jacobian/README.md)                                                          |

## Problems Observed and solution
### Problem
In revising the "mu_ranking_t_step.py" file, an error is observed. In the script, same name is used to define two variables.
### Solution
summarise __reactors__, __$\mu$ calculation__, and __npr calculation__ into ==class methods== instead of each individual function and scripts.

# May 27th & June 2nd
Travel to China and Germany

# Jun. 10th
## <span style="color: red;">Done List</span> 

| Object                                                                                      | Specification                                                                                                                                                                                                                                                                      |
| ------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| combine previous written classes and functions into a single big class                      | - [script](cantera_example/reduce_reaction.py)                                                                                                                                                                                                                                     |
| Function to replace cantera 'IdealGasConstPressureMoleReactor'<br>(constant P, constant TP) | - [comparison 1](cantera_example/const_pres/CH4_comparison.jpg)<br>- [comparison 2](cantera_example/const_pres/CO2_comparison.jpg)<br>- [comparison 3](cantera_example/const_pres/H2O_comparison.jpg)<br>- [comparison_const_TP](cantera_example/const_TP/const_TP_comparison.jpg) |
| <span style="color: red;">Fail to achieve: constant volume reactor</span>                   | - [code](cantera_example/const_vol/const_V_online.py)<br>- [false_demo](cantera_example/const_vol/false.jpg)                                                                                                                                                                       |
| Discuss: cannot approximate the partial differential by the fraction of time differential   | - [README](cantera_example/Jacobian/README.md)                                                                                                                                                                                                                                     |

# Jun. 17th
## <span style="color: red;">Done List</span> 
| Object                                                                                                                                                                                                                                           | Specification                                                                                                                                                                                                  |
| ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| - homogeneous reactor version 2                                                                                                                                                                                                                  | - [code](cantera_example/reduce_reaction_ver2.py)<br>- [README](cantera_example/README.md)                                                                                                                     |
| - Jacobian Calculation methodology and mathematical derivations (page 6-9)                                                                                                                                                                       | - [details](/SVD_QSSA/discrete.pdf)                                                                                                                                                                            |
| - Programming constant-volume Jacobian (['test.py'](cantera_example/Jacobian/test.py))                                                                                                                                                           | - [code](cantera_example/Jacobian/test.py)<br>- [problem with this approximation method](cantera_example/Jacobian/README.md)<br>- [screenshot](cantera_example/Jacobian/plots/wrong_Jacobian.png)              |
| - Test 2: improved Jacobian Calculation (['test2.py'](cantera_example/Jacobian/test2.py))<br><br>(complete in 8.2s-8.25s)                                                                                                                        | - This time perturbed by 1% of its original concentration, and I can yield reasonable values for perturbing concentrations of reasonable value. However, challenging for extremely small concentration species |
| - Test 2 parallel: Use the same method to calculate the Jacobian matrix as "Test 2" but apply parallel processing in constructing the Jacobian (['test2_p.py'](cantera_example/Jacobian/test2_p.py))<br><br>(complete in 2.3s, use 26 CPU cores) | - Use parallel processing to calculate the Jacobian matrix. This saves 72% of time<br>- The perturbation uses factor 1.01 and yields reasonable results                                                        |
|                                                                                                                                                                                                                                                  |                                                                                                                                                                                                                |
