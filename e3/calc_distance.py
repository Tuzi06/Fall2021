import xml.etree.ElementTree as ET
import pandas as pd
import numpy as np
import sys
from pykalman import KalmanFilter


def get_data(file):
    parse_result = ET.parse(sys.argv[1])
    points= parse_result.iter('{http://www.topografix.com/GPX/1/0}trkpt')
    
    gps = pd.DataFrame({
        'lat':[],
        'lon':[],
    })
    
    for elements in points:
        point = pd.DataFrame([[elements.attrib['lat'],elements.attrib['lon']]],columns =['lat','lon'])
        gps = gps.append(point,ignore_index=True)
        
    return gps
    
def distance(gps):
    # adapted from https://stackoverflow.com/questions/27928/calculate-distance-between-two-latitude-longitude-points-haversine-formula/21623206
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
    

def output_gpx(points, output_filename):
    """
    Output a GPX file with latitude and longitude from the points DataFrame.
    """
    from xml.dom.minidom import getDOMImplementation
    def append_trkpt(pt, trkseg, doc):
        trkpt = doc.createElement('trkpt')
        trkpt.setAttribute('lat', '%.8f' % (pt['lat']))
        trkpt.setAttribute('lon', '%.8f' % (pt['lon']))
        trkseg.appendChild(trkpt)
    
    doc = getDOMImplementation().createDocument(None, 'gpx', None)
    trk = doc.createElement('trk')
    doc.documentElement.appendChild(trk)
    trkseg = doc.createElement('trkseg')
    trk.appendChild(trkseg)
    
    points.apply(append_trkpt, axis=1, trkseg=trkseg, doc=doc)
    
    with open(output_filename, 'w') as fh:
        doc.writexml(fh, indent=' ')


def main():
    points = get_data(sys.argv[1])
    print('Unfiltered distance: %0.2f' % (distance(points),))
    
    smoothed_points = smooth(points)
    print('Filtered distance: %0.2f' % (distance(smoothed_points),))
    output_gpx(smoothed_points, 'out.gpx')


if __name__ == '__main__':
    main()