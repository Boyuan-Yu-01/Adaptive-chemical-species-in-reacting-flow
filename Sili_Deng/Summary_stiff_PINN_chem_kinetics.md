----*The authors relax the stiffness of the PINN by employing the Quasi-Steady_State-Assumptions.*

## Comparison between PINN and Stiff-PINN ##
![PINN](PINN.png)
<u>PINN</u>: example of building a PINN is in [here](../PINN_practice/PINN_example.pdf)
![Stiff_PINN](Stiff_PINN.png)
<u>Stiff-PINN</u>

Consider ROBER problem: 
					$A \xrightarrow{\text{k1}} B$ , where $k_1 =0.04$ 
					$B + B \xrightarrow{\text{k2}} C + B$ , where $k_2 = 3 \times 10^7$-----
					$B+C \xrightarrow{\text{k3}} A + C$ , where $k_3 = 10^4$
$Y_A(0) = 1$, $Y_B(0) = 0$, $Y_c(0) = 0$

The evolution of the species can be described by the following ODE set:
					$\frac{dY_A}{dt} = -k_1Y_A + k_3Y_BY_C$
					$\frac{dY_B}{dt} = k_1Y_A - k_2Y_B^2 - k_3Y_BY_C$
					$\frac{dY_C}{dt} = k_2Y_B^2$
The stiffness comes from: $k_2/k_1 ~ 10^9$, this causes great trouble in solving the ODEs using PINN

__Introducing QSSA to relax the PINN:__
__QSSA prerequisites:__
					$\frac{dY_k}{dt} = \omega_k^+ - \omega_k^-$
which means: 
					$\left| \frac{dY_k}{dt} \right| \ll (\omega_k^+, \omega_k^-)$
so that:
					$\omega_k^+ - \omega_k^- \approx 0$
					
$Y_2$ is likely to be the Quasi-Steady_State (QSS) species, which implies:
					$0 = k_1Y_1 - k_2Y_2^2 - k_3Y_2Y_3$
This function makes $Y_2$ (a fast evolving, unstable intermediate) an infer-able quantity s.t. $Y_2 = f(Y_1,Y_3)$

## Advantages of Using Stiff-PINN ##
- The loss of Stiff-PINN is ==4 orders== of the magnitude smaller than that of the regular PINN
-  The ODE part of the Neural Network is informed by the reduced system (system without QSS species)
- NN only output the non-QSS species, and QSS species are inferred
- QSS species are excluded from the loss functions of the initial conditions and the loss function residuals

## Disadvantages and Challenges of Using Stiff-PINN ##
- Handling the fast timescales associated with linear combinations of __several species__ rather than __single species__
- The QSSA formula and species are derived manually, a problematic process for complex chemical system
- The stiffness in complex systems may not be eliminated, and the reduced system may still show mild stiffness

## Other insights (stiff removal approaches)##
- Computational singular perturbation __(CSP)__ [Link 1](https://www.sciencedirect.com/science/article/abs/pii/S008207848980102X) [Link 2](https://scholar.google.com/scholar?hl=en&as_sdt=0%2C5&q=Lam%2C+S.+H.%3B+Goussis%2C+D.+A.+The+CSP+Method+for+Simplifying+Kinetics.+Int.+J.+Chem.+Kinet.+1994%2C+26%2C+461%E2%88%92486.&btnG=)
- Intrinsic low-dimensional manifolds __(ILDM)__ [Link 1](https://pdf.sciencedirectassets.com/271463/1-s2.0-S0010218000X0209X/1-s2.0-001021809290034M/main.pdf?X-Amz-Security-Token=IQoJb3JpZ2luX2VjEEcaCXVzLWVhc3QtMSJGMEQCIFSkjipVYfNNZDVBp76o9rCU5IcsJ6W5a7oLN%2FYga8qaAiB%2BZRDUNWrTR1GraZaFmPHYBSRIw7gxGmTXwqk2v8TfOCqzBQhQEAUaDDA1OTAwMzU0Njg2NSIMSC93IEzo7zOsWiM2KpAFGqizPQmzPDlCYWjehv0gHCTzvhBeUHHUcrlpqTjydNEp%2F3Mhix1ZY6dng1TUSxxddg2yuvI66DRh10ZdWIR8S178PDj%2FhjjKCDoxroGhlN11oTrkBQdc9ILJ4I7J3DYFKRc7mVFoA4AB5rZndH8j4ZbjzGNdhQkwvGbdxga4GiOErezPAh62SiaWlGqiwMFj9StjI9y3BbCRYXPIvhbczWAvgP7FSAPj1brHk3mXPsn2ImvoJR5Ren%2FiP%2F11F4EAHS%2FCn%2BlDMdOOUHSnfS39FrBdeS4fOI8iXK0x3cfnr%2FiYNNy37pgucz3zmczJZEb%2FyFC8mu0HhWi4A6DRkNg2O%2F7Y3nw36L6g5T04sBNqABuwv1uPONts8qKQ2hZyF%2Fpdw4f%2Bc5VhsUA00f199LvMMhWBHOvzcmBrQ8qIVm%2BeUtq1sFv0IEfOgvC68eqWcV1rWXvvlPeY6ynAM32EAdtWqWf4OuqW7Ah95Do5nH19AVJet%2FUcBAik8a%2BtuIKFHJ3ZxGpQxoTjIo3TQPx9jfBziPshiXp4I6UarQ8%2Fbp38tloS9JyUdmMlS%2BR1fKrBsXvuVG%2FPDqZCJ%2BIwClaO7N5iYw2cr7mWWsmFDGBW%2FYqPsWdILf6AzYfOjMHV7Gwindw8noiYM3ql93oV83UI8KgnpzXthiMf%2BgfNeOL7dG2HrIwQA%2FY2naep8tvgsM1%2BM9%2BwOGkcpY2Qf05i5KbftJ2Gpe9fMvcKYhhzJ2ccX8EzTdMzLup1UAByzqqrq4p%2BX%2FyJNkZKi99z6lVYuXVsD2rRKqp8gVQDFPpwea2odCztCSVPKjtgMsBcnoDsgdRVDM4HuotmSRb4%2BYyT9sjkZPEUiItSTon6%2BY6ztg2eW9e0dAgwyu3avAY6sgFsP7BEe0bGHXwROua6MYqoUDykkajJ6%2BCki0yxLSth8woBqbdr%2B92dCSElc3fsdOQUcH7zFloiwtaaQ9oXKlD0hrAcF94tYIIUIeJd346bXEt8kdTbJUvdgugiGxjDYyYLH3rkgzuynonpPZoRKbPqxxnT2JyuXn6p9BgEOUDJmi2HfBcYmVhYHrllFEvfh%2Bn4wjyrGLWV7DWoD%2Bi5KaO%2BJNoElotJ6YhOKGdiz40qR4ku&X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Date=20250127T000647Z&X-Amz-SignedHeaders=host&X-Amz-Expires=300&X-Amz-Credential=ASIAQ3PHCVTYYNEGD74H%2F20250127%2Fus-east-1%2Fs3%2Faws4_request&X-Amz-Signature=218f78faa31dd3fae8884588d9c91963aaf2999c273d9e8b7e36a037896e9590&hash=b0f9f7bb58ccc7078ceb5366956a9ef9c2d7ff111298693182612c88357202db&host=68042c943591013ac2b2430a89b270f6af2c76d8dfd086a07176afe7c76c2c61&pii=001021809290034M&tid=spdf-9052f16b-f62b-4fc0-8491-afc4f3ad3195&sid=2ac321f86850754a0479d544114dbcbcad43gxrqa&type=client&tsoh=d3d3LXNjaWVuY2VkaXJlY3QtY29tLmxpYnByb3h5MS51c2MuZWR1&ua=13165b5e5f5053000151&rr=90847fb36b9ceae4&cc=us) [Link 2](https://scholar.google.com/scholar?hl=en&as_sdt=0%2C5&q=Maas%2C+U.%3B+Pope%2C+S.+B.+Implementation+of+Simpli%EF%AC%81ed+Chemical+Kinetics+Based+on+Intrinsic+Low-Dimensional+Manifolds.+Symposium+%28International%29+on+Combustion%3B+Elsevier%2C+19&btnG=)
- Global quasi-linearization __(GQL)__ [Link 1](https://scholar.google.com/scholar?hl=en&as_sdt=0%2C5&q=Yu%2C+C.%3B+Bykov%2C+V.%3B+Maas%2C+U.+Global+quasi-linearization+%28GQL%29+versus+QSSA+for+a+hydrogen-air+auto-ignition+problem.+Phys.+Chem.+Chem.+Phys.+2018%2C+20%2C+10770%E2%88%9210779.&btnG=)
- Directed Relation Graph __(DRG)__ [Tianfeng Lu](/Tianfeng_Lu/2004_Lu_CNF_DRG.pdf)
