## References
__Thermodynamic properties and their abbreviations:__ [Link](https://cantera.org/2.5/sphinx/html/cython/thermo.html)
__Chemical Kinetics and their abbreviations:__  [Link](https://cantera.org/3.1/python/kinetics.html)

# version 0
## Constant Pressure Reactor
There are two functions: __IdealGasConstPressureReactor__ and __IdealGasConstPressurMoleReactor__

For a constant pressure homogeneous reactor simulation, there is no difference (this has been justified.) 

In __IdealGasConstPressureReactor__, the [description](https://cantera.org/3.1/cxx/dc/d5d/classCantera_1_1IdealGasConstPressureReactor.html) mentioned that "...reactor may have an arbitrary number of inlets and outlets, each of which may be connected to a "flow device" such as a mass flow controller, a pressure regulator, etc. Additional reactors may be connected to the other end of the flow device, allowing construction of arbitrary reactor networks." This has not been mentioned in the other one.

In my function, I utilized __IdealGasConstPressurMoleReactor__ with ==no special reason.==

## Constant Volume Reactor Reactor
For a constant volume homogeneous reactor simulation, I utilized __IdealGasMoleReactor__

## Constant Temperature & Pressure Reactor
The constant TP reactor is modified from the __Constant Pressure Reactor__ with ==energy solver turned off.== 

## Class Reactor
This class summarises all above three reactors. Two methods can be applied for simulations. 

Both methods are demonstrated in the [script](reactors.py)

# Update (version 1):

## reduce_reaction.py
*This is a new python class file that is designed to simulate homogeneous reaction by applying QSSA assumption at __SOME__ time steps*

### Class "Homo_Reactor"
Class "Homo_Reactor" is adopted from file "reactors.py", one more instance variable is defined: ==self.reaction_info==. This is a __dictionary variable__ that contains:

| key                 | value size |
| ------------------- | ---------- |
| t                   | m by 1     |
| P                   | m by 1     |
| rho                 | m by 1     |
| species             | 1 by n     |
| net_production_rate | m by n     |
| concentrations      | m by n     |

# Update (version 2)

## reduce_reaction.py
*This is a python class file that contain two classes: 'Homo_Reaction_ODE' and 'Homo_Reactor'*

### Class "Homo_Reactor_ODE"
Class "Homo_Reactor_ODE" are ODE functions and solver for constant volume and constant pressure homogeneous reactions.

### Class "Homo_Reactor"
Class "Homo_Reactor" call ODE solvers from "Homo_Reactor_ODE" instead of cantera
	Method "csv_output" controls the number of species output

