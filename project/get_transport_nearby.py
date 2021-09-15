##
import pandas as pd
import numpy as np
from PIL import Image
from GPSPhoto import gpsphoto
from math import sin, cos, sqrt, atan2, radians
import os
import time
from get_distance_smoothed import distance,smooth

def string_to_timestamp(string):
    return time.strptime(string, '%Y:%M:%d %H:%m:%S')

def calcutate_speed_from_photo(df):
    df['time'] =  pd.to_datetime(df['time'], format='%Y:%m:%d %H:%M:%S')
    smoothed_points = smooth(df[['lat','lon']])
    time_seconds = (df['time'][df.shape[0]-1]-df['time'][0]).total_seconds()
    return distance(smoothed_points )/time_seconds

#determine ways of travel: walking, biking, driving
def transportation(df):
    speed = calcutate_speed_from_photo(df)
    if (speed<=1.5):
        return "walking"
    elif(speed<=7):
        return "biking"
    else:
        return "driving"



def nearby_locations(osm,location_df):
    R = 6371 # Radius of the earth in km
    lat1=osm['lat']
    lon1=osm['lon']
    data_frame=pd.DataFrame()
    for (lt,ln) in zip(location_df['lat'],location_df['lon']):
        lat2 = lt
        lon2 = ln
        dLat = np.deg2rad(lat2 - lat1)
        dLon = np.deg2rad(lon2 - lon1)
        #a = np.sin(dLat/2) * np.sin(dLat/2)+np.cos(np.deg2rad(lat1)) * np.cos(np.deg2rad(lat2)) * np.sin(dLon/2) * np.sin(dLon/2)
        x =0.5 -np.cos(dLat)/2+np.cos(np.deg2rad(lat1))* np.cos(np.deg2rad(lat2)) * (1-np.cos(dLon))/2
        y = 2*R * np.arcsin(np.sqrt(x))
        osm['distance']=y*1000
        if(transportation(location_df)=="walking"):
            data = osm[osm['distance'] < 500].reset_index()
            
        elif(transportation(location_df)=="biking"):
            data = osm[osm['distance'] < 1000].reset_index()
            
        else:
            data = osm[osm['distance'] < 1500].reset_index()
        
        data_frame=pd.concat([data_frame,data])
    data_frame = data_frame.drop_duplicates(subset=['lat','lon'])
    return data_frame