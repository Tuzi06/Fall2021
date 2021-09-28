import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from statsmodels.nonparametric.smoothers_lowess import lowess
from pykalman import KalmanFilter

cpu_data = pd.read_csv('sysinfo.csv')

def to_timestamp(d):
    return d.timestamp()

cpu_data['timeData'] = pd.to_datetime(cpu_data['timestamp']).apply(to_timestamp)

loess_smoothed = lowess(cpu_data['temperature'],cpu_data['timeData'],frac = 0.01)

kalman_data = cpu_data[['temperature', 'cpu_percent', 'sys_load_1', 'fan_rpm']]
initial_state = kalman_data.iloc[0]
observation_covariance = np.diag([0.9, 0.9, 0.9, 0.9]) ** 2 # TODO: shouldn't be zero
transition_covariance = np.diag([0.02, 0.02, 0.2, 0.02]) ** 2 # TODO: shouldn't be zero
transition = [[0.97, 0.5, 0.2, -0.001], [0.1,0.4,2.2,0], [0,0,0.95,0], [0,0,0,1]] # TODO: shouldn't (all) be zero 


kf = KalmanFilter(initial_state_mean=initial_state,
    initial_state_covariance=observation_covariance,
    observation_covariance=observation_covariance,
    transition_covariance=transition_covariance,
    transition_matrices=transition)

kalman_smoothed, _ = kf.smooth(kalman_data)


plt.figure(figsize=(12, 4))

plt.plot(cpu_data['timestamp'], cpu_data['temperature'], 'b.', alpha=0.5)
plt.legend('temperature data')
plt.plot(cpu_data['timestamp'], kalman_smoothed[:, 0], 'y-')
plt.legend('alman_smooth')
plt.plot(cpu_data['timestamp'], loess_smoothed[:, 1], 'r-')
plt.legend('loess_smooth')

plt.show() # maybe easier for testing
plt.savefig('cpu.svg') # for final submission