# This bash script is used to run "unscale_ROBER.py" for different time steps. 
# I do it for convergence analysis: see what time step is enough to get a good solution.
# The script will generate json files for every different time_step size

# timeStep = 10
# echo "timeStep = 10"
# python unscale_ROBER.py 10 unscale_10.csv

# # timeStep = 1
# echo "timeStep = 1"
# python unscale_ROBER.py 1 unscale_1.csv

# # timeStep = 0.1
# echo "timeStep = 0.1"
# python unscale_ROBER.py 0.1 unscale_01.csv

# # timeStep = 0.01
# echo "timeStep = 0.01"
# python unscale_ROBER.py 0.01 unscale_001.csv

# # timeStep = 0.001
# echo "timeStep = 0.0009"
# python unscale_ROBER.py 0.001 unscale_0001.csv

# timeStep = 0.0001
echo "timeStep = 0.0001"
python unscale_ROBER.py 0.0001 unscale_00001.csv True