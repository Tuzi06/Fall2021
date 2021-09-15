from PIL import Image
import pandas as pd
import zipfile
import os
from PIL.ExifTags import TAGS
from PIL.ExifTags import GPSTAGS

def get_exif(filename):
    image = Image.open(os.path.abspath("photos" + "/" + filename))
    exif = image._getexif()
    return exif

def get_date_taken(exif):
    return exif[36867]

def get_GPS_info(exif):
    return  exif['GPSInfo']


def get_geotagging(exif):
    geotagging = {}
    if exif is not None:
        for (idx, tag) in TAGS.items():
            if tag == 'GPSInfo':
                if idx in exif:
                    for (key, val) in GPSTAGS.items():
                        if key in exif[idx]:
                            geotagging[val] = exif[idx][key]
    return geotagging

def get_decimal_from_dms(dms, ref):

        degrees = dms[0]
        minutes = dms[1] / 60.0
        seconds = dms[2] / 3600.0
    
        if ref in ['S', 'W']:
            degrees = -degrees
            minutes = -minutes
            seconds = -seconds
    
        return round(degrees + minutes + seconds, 5)
        
def get_lat_coordinates(geotags):
    lat = get_decimal_from_dms(geotags['GPSLatitude'], geotags['GPSLatitudeRef'])
    return lat
            
def get_lon_coordinates(geotags):
    lon = get_decimal_from_dms(geotags['GPSLongitude'], geotags['GPSLongitudeRef'])
    return lon

def get_coordinates(geotags):
    lat = get_decimal_from_dms(geotags['GPSLatitude'], geotags['GPSLatitudeRef'])
    lon = get_decimal_from_dms(geotags['GPSLongitude'], geotags['GPSLongitudeRef'])
    return (lat,lon)

def exif_file_df(file):
    image_list = os.listdir(file)
    df = pd.DataFrame(image_list, columns = ['name'])

    df['exif']=df['name'].apply(get_exif)
    df['time'] = df['exif'].apply(get_date_taken)
    df['geotags'] = df['exif'].apply(get_geotagging)
    df['coords'] = df['geotags'].apply(get_coordinates)
    df['lat'] = df['geotags'].apply(get_lat_coordinates)
    df['lon'] = df['geotags'].apply(get_lon_coordinates)
    
    #from geopy.geocoders import Nominatim
    #geolocator = Nominatim(user_agent="test_app")
    #df['location'] = df['coords'].apply(geolocator.reverse)

    df = df.drop(columns=['exif', 'geotags'])
    df.to_csv('image_locations.csv')