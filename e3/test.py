import sys
import pandas as pd
import numpy as np
import xml.etree.ElementTree as ET
from pykalman import KalmanFilter

parse_result = ET.parse(sys.argv[1])
points= parse_result.iter('{http://www.topografix.com/GPX/1/0}trkpt')
    
gps = pd.DataFrame({
    'lat':[],
    'lon':[],
})
    
for elements in points:
    point = pd.DataFrame([[elements.attrib['lat'],elements.attrib['lon']]],columns =['lat','lon'])
    gps = gps.append(point,ignore_index=True)

# lat = gps['lat'].values.astype(float)
# lon = gps['lon'].values.astype(float)

# shifted = gps.shift(periods = 1)
# print(shifted)
# shifted_lat = shifted['lat'].values.astype(float)
# shifted_lon = shifted['lon'].values.astype(float)

# sub_lat = lat - shifted_lat
# sub_lon = lon - shifted_lon

# p = np.pi /180
# a = 0.5 - np.cos((sub_lat)*p)/2 + np.cos(lat*p) * np.cos(shifted_lat*p) * (1-np.cos((sub_lon)*p))/2
# d =12742 * np.arcsin (np. sqrt(a))

def distance(gps):
    lat = gps['lat'].values.astype(float)
    lon = gps['lon'].values.astype(float)

    shifted = gps.shift(periods = 1)
    shifted_lat = shifted['lat'].values.astype(float)
    shifted_lon = shifted['lon'].values.astype(float)

    sub_lat = lat - shifted_lat
    sub_lon = lon - shifted_lon

    p = np.pi /180
    a = 0.5 - np.cos((sub_lat)*p)/2 + np.cos(lat*p) * np.cos(shifted_lat*p) * (1-np.cos((sub_lon)*p))/2
    d =12742 * np.arcsin (np. sqrt(a))
    return (sum(d[1:]))*1000

def smooth(gps):
    print(gps,'\n\n')
    kalman_data = pd.DataFrame( gps['lat'].values.astype(float),columns=['lat'])
    kalman_data['lon'] = gps['lon'].values.astype(float)
    
    initial_state = kalman_data.iloc[0]
    observation_covariance = np.diag([2/10000, 2/10000]) ** 2 
    transition_covariance = np.diag([1/100000, 1/100000]) ** 2 
    transition = [[1,0],[0,1]] 


    kf = KalmanFilter(initial_state_mean=initial_state,
        initial_state_covariance=observation_covariance,
        observation_covariance=observation_covariance,
        transition_covariance=transition_covariance,
        transition_matrices=transition)

    kalman_smoothed, _ = kf.smooth(kalman_data)
    print(kalman_smoothed.dtype)
    smoothed = pd.DataFrame(kalman_smoothed, columns = ['lat','lon'])
    return smoothed


print(distance(gps).round(6))
# print(distance(smooth(gps)))

print(smooth(gps))