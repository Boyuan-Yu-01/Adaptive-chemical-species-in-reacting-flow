## References
__Thermodynamic properties and their abbreviations:__ [Link](https://cantera.org/2.5/sphinx/html/cython/thermo.html)
__Chemical Kinetics and their abbreviations:__  [Link](https://cantera.org/3.1/python/kinetics.html)

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
