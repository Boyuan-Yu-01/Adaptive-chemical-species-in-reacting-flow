from scipy.integrate import solve_ivp
import numpy as np
import matplotlib.pyplot as plt
import csv
import pandas as pd
import time
from tqdm import tqdm

csv_name = 'ROBER_reltor_test.csv'

# Define ROBER as a system of ODEs
def ROBER(t, sysUnknow, k1=0.04, k2=3e7, k3=1e4):
    y1,y2,y3 = sysUnknow
    y1_dot = -k1*y1 + k3*y2*y3
    y2_dot = k1*y1 - k2*y2**2 - k3*y2*y3
    y3_dot = k2*y2**2
    return [y1_dot, y2_dot, y3_dot]

# Define the QSSA ROBER as a system of ODEs
def QSSA_ROBER(t, sysUnknow, k1=0.04, k2=3e7, k3=1e4):
    y1,y2,y3 = sysUnknow
    y1_dot = -k1*y1 + k3*y2*y3
    y2_dot = 0.0
    y3_dot = k2*y2**2
    return [y1_dot, y2_dot, y3_dot]

# Define when to swithch to QSSA_ROBER
def switch_to_QSSA(threshold):
    def stop_event(t,sysUnknown):
        _,y2,_ = sysUnknown
        _,y2_dot,_ = ROBER(t,sysUnknown)
        inst_life_y2 = abs(y2/y2_dot)
        return inst_life_y2 - threshold
    stop_event.terminal = True
    stop_event.direction = 1    # only trigger when from negative to positive 
    return stop_event
    
# Define function takes in the threshold instantaneous life time
# of species B, run the QSSA_ROBER when the instantaneous life time 
# of species B is greater than the threshold. The function returns the
# difference between QSSA result and the original ROBER result.
def QSSA_after_threshold(threshold, t_span, t_eval, y0, prob_org=ROBER, prob_QSSA=QSSA_ROBER, method="BDF"):
    sol = solve_ivp(prob_org, t_span, y0, t_eval=t_eval, method=method, events=switch_to_QSSA(threshold=threshold))
    if switch_to_QSSA(threshold=threshold).terminal>0 and sol.t[-1]<t_eval[-1]-10:
        QSSA_applied_at = sol.t[-1]
        t_span_QSSA = (sol.t[-1],t_span[1])
        y0_QSSA = sol.y[:,-1].tolist()
        t_eval_QSSA = np.arange(sol.t[-1],t_span_QSSA[1],1e-4)
        t_eval_QSSA = t_eval_QSSA[t_eval_QSSA >= t_span_QSSA[0]]
        t_eval_QSSA = t_eval_QSSA[t_eval_QSSA <= t_span_QSSA[1]]
        sol2 = solve_ivp(prob_QSSA, t_span_QSSA, y0_QSSA, t_eval=t_eval_QSSA, method='BDF')
        # print("QSSA is applied after t = " + str(sol.t[-1]) + "s")
    else:
        print("QSSA is not applied. \n aborting.........")
        return None
    
    # Extract the solution
    t = np.hstack((sol.t,sol2.t))
    y1 = np.hstack((sol.y[0],sol2.y[0]))
    y2 = np.hstack((sol.y[1],sol2.y[1]))
    y3 = np.hstack((sol.y[2],sol2.y[2]))
   
    return t, y1, y2, y3, QSSA_applied_at


# initial conditions
y0 = [1.0, 0.0, 0.0]
t_span = (0,2e4)
t_eval = np.arange(t_span[0],t_span[1],1e-4)

# read the original ROBER data
ROBER_orig_data = "ROBER_BDF.csv"
ROBER_data = pd.read_csv(ROBER_orig_data, delimiter=',')
orig_data_end = ROBER_data.iloc[-1].values.tolist() # [t, y1, y2, y3]

# Try different thresholds, see which is appropriate for the system

thresholds = [4761.900950475238]
QSSA_start_times = []  # time when QSSA is applied
reltors_A = []   # relative tolerance of A
reltors_B = []   # relative tolerance of B
reltors_C = []   # relative tolerance of C

for threshold in tqdm(thresholds):
    print(threshold)
    try: 
        t, y1, y2, y3, QSSA_start_time = QSSA_after_threshold(threshold, t_span, t_eval, y0)
        QSSA_start_times.append(QSSA_start_time)
        reltors_A.append(abs((y1[-1]-orig_data_end[1])/orig_data_end[1]))
        reltors_B.append(abs((y2[-1]-orig_data_end[2])/orig_data_end[2]))
        reltors_C.append(abs((y3[-1]-orig_data_end[3])/orig_data_end[3]))
        # print("QSSA is applied at threshold = " + str(threshold))
    except TypeError:
        print("QSSA is not applied at threshold = " + str(threshold))
        
# save the results to a csv file
data = np.vstack((thresholds, QSSA_start_times, reltors_A, reltors_B, reltors_C))
data = data.T
data = pd.DataFrame(data, columns=['threshold', 'QSSA_start_time', 'reltors_A', 'reltors_B', 'reltors_C'])
data.to_csv('thresholds_reltors.csv', index=False)

# Find what threshold is appropriate for the system
# threshold_range = [2e3,4.7e3]
# key=0   # key = 0 indicates try the left of the threshold_range, key = 1 indicates try the right of the threshold_range
# keep_looping = 1    # =1: keep while loop, =0: stop while loop
# thresholds = []
# reltors_A = []   # relative tolerance of A
# reltors_C = []   # relative tolerance of C

# while keep_looping and abs(threshold_range[0]-threshold_range[1]) > 1e-2:
#     try: 
#         t, y1, y2, y3 = QSSA_after_threshold(threshold_range[key], t_span, t_eval, y0)
#         thresholds.append(threshold_range[key])
#         reltors_A.append(abs((y1[-1]-orig_data_end[1])/orig_data_end[1]))
#         reltors_C.append(abs((y3[-1]-orig_data_end[3])/orig_data_end[3]))
#         new_threshold = (threshold_range[0]+threshold_range[1])/2
#         threshold_range[key] = new_threshold
#         key = 1 - key   # switch to the other side of the threshold
        
#         if reltors_A[-1] < 1e-2 and reltors_C[-1] < 1e-2 and reltors_A[-2] < 1e-2 and reltors_C[-2] < 1e-2:
#             keep_looping = 0
#             print("QSSA is applied between threshold = " + str(threshold_range[0]) + "and threshold = " + str(threshold_range[1]))
            
#     except TypeError:
#         print("QSSA is not applied at threshold = " + str(threshold_range[key]))
#         print(threshold_range)
#         new_threshold = (-1)**key*(threshold_range[key]-threshold_range[1-key])/3 + threshold_range[key]
#         threshold_range[key] = new_threshold
#         # do not switch to the other side of the threshold
    
# # reorder thresholds, reltors_A, reltors_C according to the ascending order of thresholds
# idx = np.argsort(thresholds)
# thresholds = np.array(thresholds)[idx]
# reltors_A = np.array(reltors_A)[idx]
# reltors_C = np.array(reltors_C)[idx]
# print("thresholds are:", thresholds)
# print("relative tolerance of A are:", reltors_A)
# print("relative tolerance of C are:", reltors_C)
# data = np.vstack((thresholds,reltors_A,reltors_C))
# data = pd.DataFrame(data.T, columns=['threshold', 'reltors_A', 'reltors_C'])
# data.to_csv('thresholds_reltors.csv', index=False)


# threshold = 50
# t, y1, y2, y3 = QSSA_after_threshold(threshold, t_span, t_eval, y0)

# # Solve using BDF method
# sol = solve_ivp(ROBER, t_span, y0, t_eval=t_eval, method='BDF', events=switch_to_QSSA(threshold=threshold))
# if switch_to_QSSA(threshold=threshold).terminal>0 and sol.t[-1]<t_eval[-1]:
#     print("QSSA is applied after t = " + str(sol.t[-1]) + "s")
#     t_span_QSSA = (sol.t[-1],t_span[1])
#     y0_QSSA = sol.y[:,-1].tolist()
#     t_eval_QSSA = np.arange(sol.t[-1],t_span[1],1e-4)
#     sol2 = solve_ivp(QSSA_ROBER, t_span_QSSA, y0_QSSA, t_eval=t_eval_QSSA, method='BDF')
    
# # Extract the solution
# t = sol.t
# y1 = sol.y[0]
# y2 = sol.y[1]
# y3 = sol.y[2]
# try:
#     sol2    
# except NameError:
#     print("QSSA is not executed.")
# else:
#     t = np.hstack((sol.t,sol2.t))
#     y1 = np.hstack((sol.y[0],sol2.y[0]))
#     y2 = np.hstack((sol.y[1],sol2.y[1]))
#     y3 = np.hstack((sol.y[2],sol2.y[2]))


# # Save the solution to a CSV file
# data = np.vstack((sol.t,sol.y))
# data = data.T
# data = pd.DataFrame(data, columns=['t', 'y1', 'y2', 'y3'])
# data.to_csv(csv_name, index=False)

# # Create vertical subplots (2 rows, 1 column)
# fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(8, 6), sharex=True)

# # Top plot
# ax1.plot(t, y1, label='species A')
# ax1.plot(t, y3, label='species C')
# ax1.set_ylabel('concentration')
# ax1.set_xlabel('t')
# ax1.legend()
# ax1.grid()


# # Bottom plot
# ax2.plot(t, y2, label='species B')
# ax2.set_ylabel('concentration')
# ax2.set_xlabel('t')
# ax2.legend()
# ax2.grid()

# # Adjust layout
# plt.xlim(*t_span)
# plt.tight_layout()
# plt.title('T_threshold = ' + str(threshold))
# plt.show()