# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>

# <headingcell level=1>

# Build script for ITU Internet Access Data

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

config = {'gen_1_dir': statmart_facts_gen1 + 'itu/',
     'gen_2_dir': statmart_facts_gen2 + 'itu/',
     'indicator': 'Percentage of population with access to the Internet',
     'indicator_category': 'ICT',
     'indicator_type': 'Internet access',
     'multiplier': .01,
     'prefix': 'internet-access',
     'suffix': 'itu'}

# <markdowncell>

# Generation 1 - The csv source file was exported from UN Data.

# <codecell>

file_name = config["prefix"] + "_" + config["suffix"] + ".csv"
my_file = config["gen_1_dir"] + file_name
df = pd.read_csv(my_file)
df[30:50]

# <markdowncell>

# Generation 2 - Refines the rough csv data from Generation 1 into a standardized csv format common to all data sets. Prepares this data for importing to the database.

# <markdowncell>

# The data is separated into a sereies of lists, each containing a timeseries for one country. These lists are into a csv file called prefix\__iso3_\_suffix.csv, where prefix is the file prefix (generally related to the indicator topic), iso3 is the 3-letter country code (converted to lower case), and suffix is the suffix (usually related to the source of the data). The metadata for each series is stored in a file called prefix\__iso3_\_suffix\_meta.csv.

# <codecell>

country_fix_map = {"Dominican Rep.":"Dominican Republic",
                   "St. Vincent and the Grenadines":"Saint Vincent and the Grenadines",
                   "Virgin Islands (U.S.)":"Virgin Islands, U.S."}
def fix_country(c):
    if c in country_fix_map:
        return country_fix_map[c]
    return c

filelist = []
us.mkdirs(config["gen_2_dir"])
for country in df["Country or Area"].unique():
    cf = df[df["Country or Area"] == country][["Year","Value"]]
    cf.columns = ["year","value"]
    cf["value"] = cf["value"].apply(lambda x: config["multiplier"] * x)
    
    #print (cf)
    cc = fix_country(country)
    iso3 = us.get_iso3_by_country(cc)
    filestem = config["prefix"] + "_" + iso3.lower() + "_" + config["suffix"]
    filename = filestem + ".csv"
    filepath = config["gen_2_dir"] + filename
    cf.to_csv(filepath, encoding="utf8", float_format='%.3f', index=False)
    meta = [("name", "%s - Percentage of population with Internet access [ITU]" % (cc)),
                ("dataset", "International Telecommunications Union database"),
                ("description", ("Pecentage of population of %s from the International Telecommunications Union") % (cc)),
                ("file", filename),
                ("filehash", us.githash(filepath)),
                ("category", config["indicator_category"]),
                ("type", config["indicator_type"]),
                ("originalsource", "International Telecommunications Union"),
                ("proximatesource", "UN Data"),
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
data_list[0:3]

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

str = "timeseries.php?s="
str = str + ",".join(filelist)
str

# <codecell>


