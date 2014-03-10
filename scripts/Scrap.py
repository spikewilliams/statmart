# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>

# <codecell>

import xml.etree.ElementTree as et
import pandas as pd

dataRoot = "C:/portal/statmart/data/"
sourceDir = dataRoot + "dimensions/source/"
dimensionsDir = dataRoot + "dimensions/"

df = pd.read_csv(dimensionsDir + "country_base.csv", encoding = "utf-8", dtype={'isonum': object})

iso39912 = sourceDir + "iso_3166_2.xml"
tree = et.parse(iso39912)
root = tree.getroot()
dlist = []
for country in root.findall("iso_3166_country"):
    c = country.attrib["code"]
    cdf = df[["country","iso2","iso3","isonum"]][df["iso2"] == c]
    for subset in country.findall("iso_3166_subset"):
        for division in subset.findall("iso_3166_2_entry"):
            d = division.attrib
            lis = [c,d["code"],d["name"],"",""]
            sdf = pd.DataFrame([lis], columns = ["iso2", "iso31662", "division", "latitude", "longitude"])
            md = pd.merge(cdf,sdf,on=["iso2"])
            dlist.append(md)
ldf = pd.concat(dlist)
ldf.to_csv(dimensionsDir + "division_base.csv", encoding = "utf-8", float_format='%.6f', index=False)

# <codecell>

ddf = pd.read_csv(dimensionsDir + "division_base.csv", encoding = "utf-8", dtype={'isonum': object})

# <codecell>

sdf = pd.DataFrame([["AX","bar"]])
sdf.columns=["iso2","b"]
pd.merge(cdf,sdf,on=["iso2"])

# <codecell>

import geopy
from geopy.geocoders import GoogleV3
from geopy.geocoders import Nominatim
geolocator = Nominatim()

with open(dimensionsDir + "division_log.csv","w") as log:
    for line in ddf.index:
        try:
            o = ddf.ix[line]
            location = o.country + ", " + o.division
            address, (latitude, longitude) = geolocator.geocode(location)
            ddf.ix[line,"latitude"] = latitude
            ddf.ix[line,"longitude"] = longitude
            log.write("%s,%s,%s" % (ddf.ix[line,"iso31662"],latitude,longitude))
        except:
            pass
ddf

# <codecell>

sdf = pd.DataFrame([["AX","bar"]])
edf = pd.DataFrame([["dX","bar"]])
pd.concat([sdf,edf])[1][0]

# <codecell>

import pandas.io.sql as psql
import pymysql

conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='', db='caribstat')

locations = psql.frame_query('select locationid, countryname, isonum from LOCATION WHERE DIVISIONNAME IS NULL AND CITY IS NULL;', con=conn)    
print('loaded dataframe from MySQL. records: %s' % len(df_mysql))
conn.close()
table = pd.merge(locations[["countryname","isonum"]],df,left_on=["isonum"], right_on=["Country code"])

table

# <codecell>

import pandas.io.sql as psql
import pymysql

conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='', db='caribstat')

locations = psql.frame_query('select locationid, countryname, isonum from LOCATION WHERE DIVISIONNAME IS NULL AND CITY IS NULL;', con=conn)    
print('loaded dataframe from MySQL. records: %s' % len(df_mysql))
conn.close()
table = pd.merge(locations[["countryname","isonum"]],df,left_on=["isonum"], right_on=["Country code"])

table

# <codecell>

ipython profile create

# <codecell>

c = get_config()

# <codecell>

from statmart_config import *

# <codecell>

statmart_facts_gen2

# <codecell>


