# Structure within the 'code' directory#
## flame_objects ##
*This directory contains:
						1. a '.json' file*
						2. objects in '.csv' form
## flame.py ##
*'flame.py' is created to output flame objects to '.csv' file s.t. these objects can be reconstructed and commissioned into python quickly.*

*All constructed objects are stored in flame_object folder. the Temperature-Pressure-composition (TPX) condition is from [Link](https://web.stanford.edu/group/haiwanglab/FFCM2/docs/Results/Test/)*
![flame](flame_range.png)
### Caveat ###
- have 'flame_object' folder under the same directory to contain generated '.csv' file(s)
- have 'FFCM2.yaml' under the same directory
- all created object(s) are stored in a '.csv' file. Other save options such as '.yaml' or '.hdf' are available and <span style="color: red;"> EASIER TO RECONSTRUCT </span> but '.csv' is easier to read

### <span style="color: red;">Code elaboration </end>###
#### function###
*__def flame(...)__: function exports flame objects in '.csv' form under directory 'save_path'
		T: temperature in K
		P: pressure in atm
		X: composition
		scheme: 'FFCM2.yaml'
		file_name: output object name
		save_path: object save under this directory. This is a local directory
		restart_csv: the flame calculation can be resumed based on a better initial guess from other calculated conditions*
- restart_csv are initialized by 'None' unless specified
- if the specified restart_csv file does not exist, a random file will be chosen if there is any. If no previous file generated, the restart_csv will be set to 'None'
- <span style="color: red;"> no direct output from this function.</span> To yield direct output, one can manipulate this function and let it 'return f'. return None allows parallel execution of this function.
- if 'restart_csv' is available, the calculation will resume from the flame object stored in 'restart_csv'. This helps speed the calculation
- This function <span style="color: red;"> reject CanteraErrors and Exceptions</span>. Errors from these two sources will be printed and no object will be recorded if such error exists.

*__def flame_accurate(...)__*: function exports the flame object in '.csv'
- The flame_accurate resolve with __transport_model__ as ==multicomponent== and enabled ==soret effect==.
- If no prior '.csv' file recording the flame, this function will call __def flame(...)__ to produce a flame object first and restart from this.

*__def recover_flame_csv(...)__: function recovers flame objects from '.csv' file under directory 'path' to an flame object
		path: local directory to '.csv' files
		fileName: the name of the '.csv' file that will be recovered
		scheme: 'FFCM2.yaml'* 

*__def flame_csv_to_dict(...)__: function convert the flame objects from '.csv' file under directory 'path' to an flame of dictionary type. Molar concentration $[kmol/m^3]$ has been added to the dictionary. 
		path: local directory to '.csv' files
		fileName: the name of the '.csv' file that will be recovered
		scheme: 'FFCM2.yaml'* *

*__def dict_clct_flames_dict(...)__: function convert all '.csv' file under directory 'path' to an flame of dictionary type, then contain all those dictionaries into a __master dictionary__
		path: local directory to '.csv' files
		scheme: 'FFCM2.yaml'
		fileName: the name of the '.csv' file that will be recovered* 
#### main ####
- 'T', 'P' are two lists of size 'n', these are from [Link](https://web.stanford.edu/group/haiwanglab/FFCM2/docs/Results/Test/).
- 'phi' is of size n x m. This parameter contains experimented unburn gas composition. each row (of size m) contains composition from min. to max. documented in [Link](https://web.stanford.edu/group/haiwanglab/FFCM2/docs/Results/Test/).
- the 'TPX_flames' stores 'T', 'P', 'X' under the 'flame_object' as a '.json' file.
- 'task_cpu' determines the number of CPUs for executing the task. This parameter will give a number no more than the number of physical CPUs exist on one's computer.
- function __flame(...)__ will be executed in parallel given all input datasets in the form of a list of tuple
- <span style="color: red;">potential problem: the names of the objects are not clear enough. </span> 
- For ==flame_accurate, a miracle is that running on a single core is faster than running in a parallel fashion.== so there are two sections of running flame object: one using __multiprocessing__ whereas another using __single core__ 
## FFCM2.yaml ##
*[Link](https://web.stanford.edu/group/haiwanglab/FFCM2/docs/Results/Test/)*

