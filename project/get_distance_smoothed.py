import pandas as pd
import numpy as np
from pykalman import KalmanFilter

def distance(data):
    from math import radians, cos, sin, asin, sqrt, pi
    R = 6371 # Radius of the earth in km
    lat1=data['lat'].values.astype(float)
    lon1=data['lon'].values.astype(float)
    lat2 = data['lat'].shift(-1,fill_value=0)
    lon2 = data['lon'].shift(-1,fill_value=0)
    dLat = np.deg2rad(lat2 - lat1)
    dLon = np.deg2rad(lon2 - lon1)
    #a = np.sin(dLat/2) * np.sin(dLat/2)+np.cos(np.deg2rad(lat1)) * np.cos(np.deg2rad(lat2)) * np.sin(dLon/2) * np.sin(dLon/2)
    x =0.5 -np.cos(dLat)/2+np.cos(np.deg2rad(lat1))* np.cos(np.deg2rad(lat2)) * (1-np.cos(dLon))/2
    y = 2*R * np.arcsin(np.sqrt(x))
    
    arr_result = y[:-1]
    result = np.sum(arr_result)*1000
    
    return(result)


def smooth(points):
    initial_state = points.iloc[0]
    observation_covariance = np.diag([2/100000,2/100000]) ** 2
    transition_covariance = np.diag([1/100000,1/100000]) ** 2
    transition_matrix = [[1,0],[0,1]]
    kf = KalmanFilter(initial_state_mean=initial_state, 
                      initial_state_covariance=observation_covariance, 
                      observation_covariance=observation_covariance, 
                      transition_covariance=transition_covariance, 
                      transition_matrices=transition_matrix)
    
    
    x,y = kf.smooth(points)
    arr = np.array(x)
    data_frame = pd.DataFrame(arr, columns=['lat','lon'])
    
    return data_frame