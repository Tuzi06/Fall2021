import pandas as pd
import sys
import gzip
import numpy as np
import matplotlib.pyplot as plt

stations_file = sys.argv[1]
city_file= sys.argv[2]
output_file = sys.argv[3]

stations = pd.read_json(stations_file, lines=True)
stations['avg_tmax']=stations['avg_tmax']/10
city_data =pd.read_csv(city_file)

city_data.dropna(subset=["population"],inplace=True)
city_data.dropna(subset=["area"],inplace=True)
city_data['area']=city_data['area']/1000000
city_data = city_data[city_data.area <= 10000]
city_data=city_data.reset_index(drop=True)
city_data['density']=city_data['population']/city_data['area']

def distance(city, stations):
    from math import radians, cos, sin, asin, sqrt, pi
    R = 6371 # Radius of the earth in km
  
    dLat = np.deg2rad(stations['latitude'] - city['latitude'])
    dLon = np.deg2rad(stations['longitude'] - city['longitude'])
    #a = np.sin(dLat/2) * np.sin(dLat/2)+np.cos(np.deg2rad(lat1)) * np.cos(np.deg2rad(lat2)) * np.sin(dLon/2) * np.sin(dLon/2)
    x =0.5 -np.cos(dLat)/2+np.cos(np.deg2rad(city['latitude']))* np.cos(np.deg2rad(stations['latitude'])) * (1-np.cos(dLon))/2
    y = 2*R * np.arcsin(np.sqrt(x))
    
    return(y)

def best_tmax(city, stations):
    stations['distance'] = distance(city, stations)
    station = stations[stations['distance'] == stations['distance'].min()]
    station = station.reset_index(drop= True)

    result = station.loc[0, 'avg_tmax']

    return result

city_data['avg_tmax'] = city_data.apply(best_tmax, axis=1, stations=stations)

plt.scatter(city_data['avg_tmax'], city_data['population'])
plt.title('Temperature vs Population Density')
plt.xlabel('Avg Max Temperature (\u00b0C)')
plt.ylabel('Population Density (people/km\u00b2)')
plt.savefig(output_file)