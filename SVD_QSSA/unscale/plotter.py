import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


def plot(arr1, arr2, time):
    plt.figure(figsize=(8,5))
    plt.plot(arr1[:,0], arr1[:,1], color='red', label='A:orig')
    plt.plot(arr1[:,0], arr1[:,3], color='black', label='C:orig')
    plt.plot(arr2[:,0], arr2[:,1], color='blue', linestyle="--", label=f'A:QSSA')
    plt.plot(arr2[:,0], arr2[:,3], color='green', linestyle="--",label=f'C:QSSA')
    plt.axvline(x=time, color='blue', linewidth=0.5, linestyle='--')
    plt.xlabel('t')
    plt.ylabel('Concentration')
    plt.legend()
    plt.title(f'QSSA at t={time:.3f}')
    plt.show()
    


orig_0 = pd.read_csv("unscale_ini.csv")
orig_1 = pd.read_csv('unscale_00001.csv')

ana_2 = pd.read_csv('QSSA_ana_2.csv')
ana_3 = pd.read_csv('QSSA_ana_3.csv')
ana_5 = pd.read_csv('QSSA_ana_5.csv')
ana_6 = pd.read_csv('QSSA_ana_6.csv')
ana_7 = pd.read_csv('QSSA_ana_7.csv')
ana_8 = pd.read_csv('QSSA_ana_8.csv')
ana_9 = pd.read_csv('QSSA_ana_9.csv')

do0 = orig_0.values # original data
do1 = orig_1.values
do = np.vstack((do0, do1))

da2 = ana_2.values  # QSSA data
da3 = ana_3.values
da5 = ana_5.values
da6 = ana_6.values
da7 = ana_7.values
da8 = ana_8.values
da9 = ana_9.values


plot(do, da9, 500)
