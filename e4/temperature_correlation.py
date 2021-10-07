import pandas as pd
import sys

stations = pd.read_json(sys.argv[1], lines=True)
stations['avg_tmax'] = stations['avg_tmax'] /10

city_data = pd.read_csv(sys.argv[2])
city_data = city_data.dropna()
city_data['area']=city_data['area']/1000000
city_data = city_data[city_data['area'] < 10000]
# print(stations)
print(city_data)