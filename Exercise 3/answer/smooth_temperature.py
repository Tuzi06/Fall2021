
import sys
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from statsmodels.nonparametric.smoothers_lowess import lowess
from datetime import datetime
from pykalman import KalmanFilter

#cpu_data = pd.read_csv('sysinfo.csv')
file_load = sys.argv[1]
cpu_data = pd.read_csv(file_load)

def to_timestamp(d):
    return d.timestamp()

cpu_data['timestamp_float'] = pd.to_datetime(cpu_data['timestamp']).apply(to_timestamp)

loess_smoothed = lowess(cpu_data['temperature'], cpu_data['timestamp_float'], frac = 0.02)

kalman_data = cpu_data[['temperature', 'cpu_percent', 'sys_load_1', 'fan_rpm']]

initial_state = kalman_data.iloc[0]
observation_covariance = np.diag([0.9, 0.9, 0.9, 0.9]) ** 2 # TODO: shouldn't be zero
transition_covariance = np.diag([0.5, 0.5, 0.5, 0.5]) ** 2 # TODO: shouldn't be zero
transition = [[0.97,0.5,0.2,-0.001], [0.1,0.4,2.2,0], [0,0,0.95,0], [0,0,0,1]] # TODO: shouldn't (all) be zero

kf = KalmanFilter(initial_state_mean = initial_state, initial_state_covariance = observation_covariance, observation_covariance = observation_covariance, transition_covariance = transition_covariance, transition_matrices = transition)
kalman_smoothed, _ = kf.smooth(kalman_data)


#ploting
plt.figure(figsize=(12, 4))
plt.plot(cpu_data['timestamp_float'], cpu_data['temperature'], 'b.', alpha=0.5)
plt.plot(cpu_data['timestamp_float'], loess_smoothed[:,1], 'r-', alpha=0.9)
plt.plot(cpu_data['timestamp_float'], kalman_smoothed[:, 0], 'g-', alpha=0.7)

plt.legend(['CPU Data', 'LOESS Smoothing', 'Kalman Smoothing'])
#plt.show() # maybe easier for testing
plt.savefig('cpu.svg') # for final submission
