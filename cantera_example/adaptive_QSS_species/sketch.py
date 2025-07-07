import numpy as np

scs = [0,1,2,3,4,5,6,7,8,9]
delete = [4,9,7]

scs = np.delete(scs, delete)

print(scs)