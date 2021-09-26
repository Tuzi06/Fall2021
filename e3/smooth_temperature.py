import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from statsmodels.nonparametric.smoothers_lowess import lowess

from pykalman import KalmanFilter

cpu_data = pd.read_csv('sysinfo.csv')

def to_timestamp(d):
    return d.timestamp()

cpu_data['timeData'] = pd.to_datetime(cpu_data['timestamp']).apply(to_timestamp)
print(cpu_data.dtypes)

loess_smoothed = lowess(cpu_data['temperature'],cpu_data['timeData'],frac = 0.01)

# vkalman_data = cpu_data[['temperature', 'cpu_percent', 'sys_load_1', 'fan_rpm']]
# initial_state = kalman_data.iloc[0]
# observation_covariance = np.diag([0, 0, 0, 0]) ** 2 # TODO: shouldn't be zero
# transition_covariance = np.diag([0, 0, 0, 0]) ** 2 # TODO: shouldn't be zero
# transition = [[0,0,0,0], [0,0,0,0], [0,0,0,0], [0,0,0,0]] # TODO: shouldn't (all) be zero 


plt.figure(figsize=(12, 4))
plt.plot(cpu_data['timestamp'], cpu_data['temperature'], 'b.', alpha=0.5)
plt.plot(cpu_data['timestamp'], loess_smoothed[:, 1], 'r-')
plt.show() # maybe easier for testing
# plt.savefig('cpu.svg') # for final submission