from scipy.integrate import solve_ivp
import numpy as np
import matplotlib.pyplot as plt
import csv
import pandas as pd
import time

csv_name = 'ROBER_QSSA_4250.csv'

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
    if switch_to_QSSA(threshold=threshold).terminal>0 and sol.t[-1]<t_eval[-1]:
        t_span_QSSA = (sol.t[-1],t_span[1])
        y0_QSSA = sol.y[:,-1].tolist()
        t_eval_QSSA = np.arange(sol.t[-1],t_span[1],1e-4)
        sol2 = solve_ivp(prob_QSSA, t_span_QSSA, y0_QSSA, t_eval=t_eval_QSSA, method='BDF')
        print("QSSA is applied after t = " + str(sol.t[-1]) + "s")
    else:
        print("QSSA is not applied. \n aborting.........")
        return None
    
    # Extract the solution
    t = np.hstack((sol.t,sol2.t))
    y1 = np.hstack((sol.y[0],sol2.y[0]))
    y2 = np.hstack((sol.y[1],sol2.y[1]))
    y3 = np.hstack((sol.y[2],sol2.y[2]))
    
    # plot the rsult for 5s then close the plot to keep it running
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(8, 6), sharex=True)
    # Top plot
    ax1.plot(t, y1, label='species A')
    ax1.plot(t, y3, label='species C')
    ax1.set_ylabel('concentration')
    ax1.set_xlabel('t')
    ax1.legend()
    ax1.grid()


    # Bottom plot
    ax2.plot(t, y2, label='species B')
    ax2.set_ylabel('concentration')
    ax2.set_xlabel('t')
    ax2.legend()
    ax2.grid()

    # Adjust layout
    plt.xlim(*t_span)
    plt.tight_layout()
    plt.title('T_{threshold} = ' + str(threshold))
    plt.show()
    time.sleep(5)
    plt.close()
    return t, y1, y2, y3


# initial conditions
y0 = [1.0, 0.0, 0.0]
t_span = (0,1e4)
t_eval = np.arange(t_span[0],t_span[1],1e-4)

# read the original ROBER data
# ROBER_orig_data = "ROBE_BDF.csv"
# ROBER_data = pd.read_csv(ROBER_orig_data, delimiter=',')
# orig_data_end = ROBER_data.iloc[-1].values.tolist() # [t, y1, y2, y3]

threshold = 4250
t, y1, y2, y3 = QSSA_after_threshold(threshold, t_span, t_eval, y0)

# save data to csv file:
data = np.vstack((t,y1,y2,y3))
data = data.T
data = pd.DataFrame(data, columns=['t', 'y1', 'y2', 'y3'])
data.to_csv(csv_name, index=False)