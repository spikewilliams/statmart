# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>

# <headingcell level=1>

# Build script for Caribbean SIDS RCM water data: Reservoir

# <markdowncell>

# This script moves descriptive data from Generation 1 through Generation 3.

# <codecell>

import os, imp
import pandas as pd

from settings_statmart import *
import utils_statmart as us

import gen3_utils
import gen4_utils

us.verbose = True

# <markdowncell>

# Customize the below per this specfic dataset....

# <codecell>

config = {'gen_1_dir': statmart_facts_gen1 + 'sidsrcm/water/',
     'gen_2_dir': statmart_facts_gen2 + 'sidsrcm/water/',
     'gen_4_dir': statmart_view_gen4 + 'sidsrcm/',
     'description': 'Capacity of water reservoirs and storage tanks',
     'indicator': 'Reservoir capacity',
     'indicator_category': 'Water',
     'indicator_type': 'Reservoirs',
     'multiplier': 1,
     'prefix': 'water-reservoir',
     'suffix': 'sidsrcm',
     'fileprefix': 'reservoirs'}

# <markdowncell>

# Generation 1 - The xls source files this this data have been prepared by an external script. The file name is in the format desalination_country-name.xls. Each file has one worksheet of data, and a second with metadata. The names of these sheet are "data" and "metadata".

# <codecell>

country_dict = us.load_carib_country_dict(key_column="name")
dataset = []
for name in sorted(country_dict.keys()):
    path = config['gen_1_dir'] + config['fileprefix'] + "_" + us.machine_name(name) + ".xls"
    if os.path.exists(path):
        xlfile = pd.ExcelFile(path)
        df = xlfile.parse("data")
        mf = xlfile.parse("metadata")
        dataset.append((country_dict[name]["iso3"], df, mf))
        
dataset[0][1] # This is what the data looks like

# <codecell>

dataset[0][2] # This is what the metadata looks like

# <markdowncell>

# Generation 2 - Refines the rough csv data from Generation 1 into a standardized csv format common to all data sets. Prepares this data for importing to the database.

# <markdowncell>

# This code follows a fairly standard form, in which it loops through each country's information, writes the data to a .csv file, extracts some metadata and writes that to a .csv file, and then writes a list of all the files that it made to a file called \_PREFIX.csv

# <codecell>

filelist = []
us.mkdirs(config["gen_2_dir"])
for (iso3, df, mf) in dataset:
    us.log(iso3)
    try:
        df.columns = ["description", "value"]
    except Exception: # The data for St Kitts only has one column. We are excluding it for now.
        us.log(sys.exc_info())
        continue
    filestem = config["prefix"] + "_" + iso3.lower() + "_" + config["suffix"]
    filename = filestem + ".csv"
    filepath = config["gen_2_dir"] + filename
    df.to_csv(filepath, encoding="utf8", float_format='%.3f', index=False)
    
    country = us.get_country_by_iso3(iso3)    
    meta = [("name", "%s - %s [SIDS RCM]" % (country, config["indicator"])),
        ("originalsource", mf.ix["Capacity"]["Source"]),
        ("proximatesource", "SIDS RCM"),
        ("dataset", config["indicator"]),
        ("description", config["description"]),
        ("note", mf.ix["Capacity"]["Note"]),
        ("unit", mf.ix["Capacity"]["Unit"]),
        ("category", config["indicator_category"]),
        ("type", config["indicator_type"]),
        ("file", filename),
        ("filehash", us.githash(filepath)),
        ("columns", "description,value")
        ]
 
    metafile = config["gen_2_dir"] + filestem + "_meta.csv"    
    pd.DataFrame(meta,columns = ["key","value"]).to_csv(metafile, encoding="utf8", float_format='%.3f',index=False)
    filelist.append(filestem)
    
pd.DataFrame(filelist).to_csv(config["gen_2_dir"] + "_" + config["prefix"] + ".csv", encoding="utf8", index=False, header=False)
us.log("%i series saved to %s" % (len(filelist), config["gen_2_dir"]))

# <markdowncell>

# Generation 3 - Load the Generation 2 data into the database.

# <codecell>

data_list = gen3_utils.get_gen2_data(config)
observation_fields = "series, description, value, locationid"
gen3_utils.standard_load_from_data_list(data_list, observation_fields)
data_list

# <markdowncell>

# Here are the names of the series:

# <codecell>

filelist

# <codecell>


