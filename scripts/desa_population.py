# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>

# <headingcell level=1>

# Build script for UN DESA population estimates (Caribbean)

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

config = {'gen_1_dir': statmart_facts_gen1 + 'desa/',
     'gen_2_dir': statmart_facts_gen2 + 'desa/pop/',
     'gen_4_dir': statmart_view_gen4 + 'desa/',
     'indicator': 'Population',
     'indicator_category': 'Demographic',
     'indicator_type': 'Population',
     'multiplier': 1000,
     'prefix': 'pop',
     'suffix': 'desa'}

# <markdowncell>

# Generation 1 - The xls source file for the population data is from the [2012 revision of the World Population Prospects](http://esa.un.org/unpd/wpp/index.htm) from the Population Division of the UN Department of Economic and Social Affairs. This covers estimates from 1950-2010. There are many other available views of various aspects of this data available at that site.

# <codecell>

file_name = "WPP2012_POP.xls"
popfile = config["gen_1_dir"] + file_name
xlfile = pd.ExcelFile(popfile)
xlfile.sheet_names # The source file has several different estimates available. We are just using the base scenario ('ESTIMATES'), plus the 'NOTES' sheet.

# <markdowncell>

# Generation 2 - Refines the rough csv data from Generation 1 into a standardized csv format common to all data sets. Prepares this data for importing to the database.

# <markdowncell>

# First, create the DataFrame with all population information. The "Country code" column contains the ISO 3166 numeric value, but as an integer, rather than as 3-numeral string padded by zeros. So we fix this to be in line with the ISO spec, and, hence, with our data. We also rename the Country code field to match the name in our schema.

# <codecell>

df = xlfile.parse("ESTIMATES", skiprows=range(0,15), header=16)
df["Country code"] = df["Country code"].apply(lambda x: "%03i" % int(x))
df = df.rename(columns={"Country code":"isonum"})

country_dict = us.load_carib_country_dict(key_column="isonum") # Here we filter in only Caribbean countries
carib = pd.DataFrame(country_dict).T
cf = pd.merge(carib,df, on="isonum")
cf = cf.set_index("iso3")
cf = us.multiply_data(cf, cf.columns[8:], config)  # The data is in thousands. Multiply it out to get the full number.
cf[0:5] # look at a sample

# <markdowncell>

# Next, parse out the notes from the notes sheet. These are a bunch of values in rows, looking like "(22) Refers to Bonaire, Saba and Sint Eustatius."  We need to map the value in parens to something that can be related to the "Notes" field of the main dataframe. This uses a flag to ensure that notes are run twice against the same DataFrame.

# <codecell>

if not hasattr(cf,"notesFlag"):
    noteMap = {}
    notes = xlfile.parse("NOTES").transpose()
    for col in notes.columns:
        (noteid, note) = notes[col][0].split(") ",1)
        noteid = noteid[1:]
        noteMap[noteid] = note
    cf["Notes"] = cf["Notes"].dropna().apply(lambda x: noteMap[str(x)])
else:
    print("WARNING: you must reinitialize the DataFrame before running this code a second time.")        
cf.notesFlag = True
cf[10:14]

# <markdowncell>

# Save each list of population estimates into a csv file called pop\__iso3_\_desa.csv, where iso3 is the 3-letter country code, converted to lower case. Save the metadata in a file called pop\__iso3_\_desa\_meta.csv.

# <codecell>

filelist = []
tf = cf.T
mf = ""
for col in tf.columns:
    line = tf[col]
    filestem = config["prefix"] + "_" + col.lower() + "_" + config["suffix"]
    filename = filestem + ".csv"
    filepath = config["gen_2_dir"] + filename
    line[8:].to_csv(filepath, encoding="utf8", index=True, header=["value"], index_label="year")
    
    meta = [("name", "%s - Population estimates (1950-2010) [UN DESA]" % (line.ix["name"])),
                ("dataset", "UN DESA world population estimates"),
                ("description", ("Population estimates for %s from the 2012 Revision of the World Population Prospects, produced by the " + \
                    "Population Division of the United Nations Department of Economic and Social Affairs") % (line.ix["name"])),
                ("file", filename),
                ("filehash", us.githash(filepath)),
                ("category", config["indicator_category"]),
                ("type", config["indicator_type"]),
                ("originalsource", "UN Department of Economic and Social Affairs: Population Divison"),
                ("columns", "year,value")]
    mf = pd.DataFrame(meta,columns = ["key","value"])
    metafile = config["gen_2_dir"] + filestem + "_meta.csv"
    mf.to_csv(metafile, encoding="utf8", index=False)
    filelist.append(filestem)
    
pd.DataFrame(filelist).to_csv(config["gen_2_dir"] + "_" + config["prefix"] + ".csv", encoding="utf8", index=False, header=False)
print("%i series saved to %s" % (len(filelist), config["gen_2_dir"]))

# <markdowncell>

# Generation 3 - Load the Generation 2 data into the database.

# <codecell>

imp.reload(gen3_utils)
data_list = gen3_utils.get_gen2_data(config)
gen3_utils.standard_load_from_data_list(data_list)
#data_list[0:3]

# <markdowncell>

# Generation 4 - Build a php file that uses javascript to generate SVGs using the data in the database

# <codecell>

import imp
imp.reload(gen4_utils)
config = gen4_utils.build_gen4_config(config)
page = gen4_utils.build_d3_line_graph(config)

# <codecell>

filelist

# <codecell>


