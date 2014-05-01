# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>

# <headingcell level=1>

# Build script for Caribbean SIDS RCM tourism data: Cruise visitor expenditures

# <codecell>

import os, imp
import pandas as pd

from settings_statmart import *
import utils_statmart as us

import gen1_sidsrcm
import gen3_utils
import gen4_utils

us.verbose = True

# <markdowncell>

# Customize the below per this specfic dataset....

# <codecell>

config = {'gen_1_dir': statmart_facts_gen1 + 'sidsrcm/tourism/',
     'gen_2_dir': statmart_facts_gen2 + 'sidsrcm/tourism/',
     'gen_4_dir': statmart_view_gen4 + 'sidsrcm/',
     'description': 'Cruise-ship visitor expenditure per day',
     'indicator': 'Cruise-ship visitor expenditure per day',
     'indicator_category': 'Tourism',
     'indicator_type': 'Cruise visitor expenditure',
     'multiplier': 1,
     'prefix': 'tourism-cruise-expend',
     'suffix': 'sidsrcm',
     'fileprefix': 'cruise-expend',
     'filesuffix': 'annual'}

gen0_config = {
    "description":config["indicator"],
    "descriptor":"cruise-expend",
    "fileName":"Tourism_1c_CruiseVisitorExpen.xlsx",
    "generation":"0",
    "path":"tourism/",
    "timeseries":True
}

# <markdowncell>

# Generation 0 - Prepare the original xls file by converting it into a somewhat more standardized xls formation for use in Gen 1. Each outputted xls has one worksheet of data, and a second with metadata. The names of these sheet are "data" and "metadata".

# <codecell>

import imp
imp.reload(gen1_sidsrcm)
gen1_sidsrcm.process_gen0_xls(gen0_config)

# <markdowncell>

# Generation 1

# <codecell>

country_dict = us.load_carib_country_dict(key_column="name")
dataset = []
for name in sorted(country_dict.keys()):
    path = config['gen_1_dir'] + config['fileprefix'] + "_" + us.machine_name(name) + "_" + config["filesuffix"] + ".xls"
    if os.path.exists(path):
        xlfile = pd.ExcelFile(path)
        df = xlfile.parse("data")
        mf = xlfile.parse("metadata")
        iso3 = country_dict[name]["iso3"]
        #if len(df.columns) == 2:
        dataset.append((iso3, df, mf))
        
dataset[2][1] # This is what the data looks like

# <codecell>

dataset[3][2] # This is what the metadata looks like

# <markdowncell>

# Generation 2 - Refines the rough csv data from Generation 1 into a standardized csv format common to all data sets. Prepares this data for importing to the database.

# <markdowncell>

# This code follows a fairly standard form, in which it loops through each country's information, writes the data to a .csv file, extracts some metadata and writes that to a .csv file, and then writes a list of all the files that it made to a file called \_PREFIX.csv

# <codecell>

keycol = "Total"

filelist = []
us.mkdirs(config["gen_2_dir"])
for (iso3, df, mf) in dataset:
    us.log(iso3)
    try:
        if len(df.columns) == 2:
            df.columns = ["year", "value"]
        else:
            df.columns = ["year", "value", "notes"]
        
    except Exception: # The data for St Kitts only has one column. We are excluding it for now.
        us.log(sys.exc_info())
        continue
    filestem = config["prefix"] + "_" + iso3.lower() + "_" + config["suffix"]
    filename = filestem + ".csv"
    filepath = config["gen_2_dir"] + filename
    df.to_csv(filepath, encoding="utf8", float_format='%.3f', index=False)
    
    country = us.get_country_by_iso3(iso3)
    meta = [("name", "%s - %s [SIDS RCM]" % (country, config["indicator"])),
      #  ("originalsource", mf.ix[keycol]["Source"]),
        ("originalsource", "SIDS RCM"),
        ("proximatesource", "SIDS RCM"),
        ("dataset", config["indicator"]),
        ("description", config["description"]),
      #  ("note", mf.ix[keycol]["Note"]),
      #  ("unit", mf.ix[keycol]["Unit"]),
        ("category", config["indicator_category"]),
        ("type", config["indicator_type"]),
        ("file", filename),
        ("filehash", us.githash(filepath)),
        ("columns", "description,value")
        ]
 
    metafile = config["gen_2_dir"] + filestem + "_meta.csv"
    try:
        pd.DataFrame(meta,columns = ["key","value"]).to_csv(metafile, encoding="utf8", float_format='%.3f',index=False)
    except Exception: 
        pd.DataFrame(meta,columns = ["key","value","notes"]).to_csv(metafile, encoding="utf8", float_format='%.3f',index=False)
       
    filelist.append(filestem)
    
pd.DataFrame(filelist).to_csv(config["gen_2_dir"] + "_" + config["prefix"] + ".csv", encoding="utf8", index=False, header=False)
us.log("%i series saved to %s" % (len(filelist), config["gen_2_dir"]))

# <markdowncell>

# Generation 3 - Load the Generation 2 data into the database.

# <codecell>

data_list = gen3_utils.get_gen2_data(config)
gen3_utils.standard_load_from_data_list(data_list)
data_list[0][1]

# <markdowncell>

# Here are the names of the series:

# <codecell>

filelist

# <codecell>

",".join(filelist)

# <codecell>


