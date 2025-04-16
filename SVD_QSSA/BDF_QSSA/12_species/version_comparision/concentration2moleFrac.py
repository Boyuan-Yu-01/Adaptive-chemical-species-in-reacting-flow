import csv
import numpy as np
import pandas as pd
file_name = "ver_2.csv"

with open(file_name, 'r') as f:
    reader = csv.reader(f)
    header = next(reader)
    remaining_rows = [row for row in reader]
data = np.array(remaining_rows, dtype=np.float64)

for i in range(data.shape[0]):
    sum = 0 # total concentration
    for j in range(1, data.shape[1]):
        sum += data[i][j]
        data[i][j] /= sum

df = pd.DataFrame
output_file = file_name.strip(".csv") + "_X.csv"
df.to_csv(output_file, index=False)