import pandas as pd
import numpy as np
import sys
import matplotlib.pyplot as plt

stations = pd.read_json(sys.argv[1], lines=True)
stations['avg_tmax'] = stations['avg_tmax'] /10

city_data = pd.read_csv(sys.argv[2])
city_data = city_data.dropna().reset_index()
city_data['area']=city_data['area']/1000000
city_data['density']= city_data['population']/city_data['area']
city_data = city_data[city_data['area'] < 10000]

def distance(city, stations):
    sub_lat =stations['latitude']- city['latitude']
    sub_lon =stations['longitude']- city['longitude']

    p = np.pi /180
    a = 0.5 - np.cos((sub_lat)*p)/2 + np.cos(stations['latitude']*p) * np.cos(city['latitude']*p) * (1-np.cos((sub_lon)*p))/2
    d =12742 * np.arcsin (np. sqrt(a))
    return d

def best_tmax(city, stations):
    stations['distance'] = distance(city,stations)
    return stations.loc[stations['distance'].idxmin()]['avg_tmax']
  
  
city_data['best_tmax'] = city_data.apply(best_tmax, axis=1, stations=stations)
plt.plot(city_data['best_tmax'].values, city_data['density'],'b.', alpha=0.5)
plt.title('Temperature vs Population Density')
plt.xlabel('Avg Max Temperature (\u00b0C)')
plt.ylabel('Population Density (people/km\u00b2)')

plt.show()
print(city_data)