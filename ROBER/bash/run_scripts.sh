# This bash script is used to run all three neural networks in sequence. All neural network will be saved in a json file given by the user.
# After creating the json file, the script will run the first neural network and predict the output.

#fourth neural network
echo "running the fourth NN: 20 x 3..."
python PINN_ROBER_log.py 1 20 20 20 3 20_3_log.json
python postProcessing_log.py 20_3_log.json 20_3_logt_loss.png 20_3_logt_pred.png NN:20x3,lr=1e-5

# First neural network: 128 x 3
echo "running the first NN: 128 x 3..."
python PINN_ROBER_log.py 1 128 128 128 3 128_3_log.json
python postProcessing_log.py 128_3_log.json 128_3_logt_loss.png 128_3_logt_pred.png  NN:128x3,lr=1e-5

# Second neural network: 
echo "running the second NN: 64 x 5..."
python PINN_ROBER_log.py 1 64 64 64 64 64 3 64_5_log.json
python postProcessing_log.py 64_5_log.json 64_5_logt_loss.png 64_5_logt_pred.png NN:64x5,lr=1e-5

# Third neural network:
echo "running the third NN: 128 x 5..."
python PINN_ROBER_log.py 1 128 128 128 128 128 3 128_5_log.json
python postProcessing_log.py 128_5_log.json 128_5_logt_loss.png 128_5_logt_pred.png NN:128x5,lr=1e-5
