# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>

# <markdowncell>

# The following script creates "dimensions/gen2/base/countries\_base.csv", which is a file containing identification and location information for approximatly 249 countries, as defined by ISO 3166. This csv file has header names corresponding to field names in the Statmart database's _Location_ table. The content for this file was provided by the [OpenGeo.org](http://opengeocode.org) "Countries of the World" database.

# <codecell>

import pandas as pd

from settings_statmart import *

gen_1_dir = statmart_dimensions_gen1 + "opengeocode/"
gen_2_dir = statmart_dimensions_gen2 + "base/"

pd.set_option('chained_assignment',None) # supress raising of SettingWithCopyWarning

# <codecell>

df = pd.read_csv(gen_1_dir + "cow.txt", encoding = "utf-8", dtype={"ISO3166N3":object}, sep=";", skiprows=28)
pf = df[['ISO3166A2', 'ISO3166A3', 'ISO3166N3', 'ISOen_ro_name', 'ISOen_ro_proper', 
   'latitude', 'longitude', 'maxlatitude', 'minlatitude', 'maxlongitude', 'minlongitude']] 

pf.columns = ["iso2","iso3","isonum","countryname","name",
               'latitude', 'longitude', 'maxlatitude', 'minlatitude', 'maxlongitude', 'minlongitude']
pf['iso3'] = pf['iso3'].apply(str.strip) 
pf['countryname'] = pf['countryname'].apply(str.strip) 
pf['name'] = pf['name'].apply(str.strip) 
pf["isonum"] = pf["isonum"].apply(lambda x: "%03i" % int(x))
pf.to_csv(gen_2_dir + "country_base.csv", encoding = "utf-8", float_format='%.6f', index=False)

# <markdowncell>

# A look at some of the data...

# <codecell>

pf[0:10]

# <markdowncell>

# Here are the column names for the country\_base.csv file, in lower and upper case.

# <codecell>

"iso2,iso3,isonum,countryname,name,latitude,longitude,maxlatitude,minlatitude,maxlongitude,minlongitude".upper()

# <codecell>


