import pandas as pd
import numpy as np
import json
import geojson
import fileinput
import re
import os


def df_to_geojson(df, properties, lat= 'latitude', lon='longitude'):
    geojson = {'type':'FeatureCollection', 'features':[]}

    for _, row in df.iterrows():
        feature = {'type':'Feature',
                   'properties':{},
                   'geometry':{'type':'Point',
                               'coordinates':[]}}

        feature['geometry']['coordinates'] = [row[lon],row[lat]]

        for prop in properties:
            feature['properties'][prop] = row[prop]


        geojson['features'].append(feature)

    return geojson

def mapit(new_map,geoj,geoj2,x,y,template):
    f_in = fileinput.input(template)

    with open(new_map,'w') as f_out: f_out.write('')

    for line in f_in:
        with open(new_map,'a') as f_out:
            fileline = line
            f_out.write(fileline)
            if re.search("//ADD Permit Points",fileline):
                f_out.write("var gjData = ")
                f_out.write(str(geoj))

            elif re.search("//ADD Structure Points", fileline):
                f_out.write("var gjData2 = ")
                f_out.write(str(geoj2)) 

            elif re.search("//ADD CENTER POINTS", fileline):
                newline = "map.setView([{},{}], 12)".format(y, x)
                f_out.write(str(newline))    

    #map.setView([ 42.06147811051676,  -74.87224712603198], 12);

    f_in.close()
    print('File Created: ', new_map)
    
