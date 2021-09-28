import sys
import pandas as pd
import numpy as np
import xml.etree.ElementTree as ET

# parse_result = ET.parse(sys.argv[1])
# points= parse_result.iter('{http://www.topografix.com/GPX/1/0}trkpt')
    
# gps = pd.DataFrame({
#     'lat':[],
#     'lon':[],
# })
    
# for elements in points:
#     point = pd.DataFrame([[elements.attrib['lat'],elements.attrib['lon']]],columns =['lat','lon'])
#     gps = gps.append(point,ignore_index=True)

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

points = pd.DataFrame({
    'lat': [49.28, 49.26, 49.26],
    'lon': [123.00, 123.10, 123.05]})
print(distance(points).round(6))