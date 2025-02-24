import yaml
import numpy as np

# with open("FFCM2.yaml", 'r') as file:
#     data = yaml.safe_load(file)
    
# types = []

# for reaction in data['reactions']:
#      if 'type' in reaction:  # Only process dictionaries with 'type'
#         reaction_type = reaction['type']
#         if reaction_type and reaction_type not in types:
#             types.append(reaction_type)
# print(types)

## SVD examples    
A = np.array([[1, 7, 13], [2, 8, 14], [3, 9, 15], [4, 10, 16], [5, 11, 17], [6, 12, 18]])
U, S, VT = np.linalg.svd(A)
V = VT.T
assemble = np.zeros(A.shape)

for i in range(len(S)):
    U_i = U[:, i][:,None]
    VT_i = VT[i,:][None,:]
    assemble += S[i] * np.dot(U_i, VT_i)
    
print(assemble)

    

    
    
    



     