# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>

# <headingcell level=1>

# Build script for CEPALStat indicator #127: Unemployment

# <markdowncell>

# This script creates csv files out of CEPALStat data, in  a format suitable for subsequent loading to the Statmart database. Each country with an available time series will have two csv files representing their data. The first contains the time series data, and the second will contain metadata about the time series. Additionally, the file "\_unemployment.csv" will be created to list all the created files.

# <codecell>

import os, imp
import pandas as pd

from s0000_statmart_settings import *
import s0001_statmart_utils as statmart_utils
import s2201_cepalstat_utils as cepalstat_utils

# <markdowncell>

# Customize the below per this specfic dataset....

# <codecell>

gen_1_dir = statmart_facts_gen1 + "cepalstat/"
gen_2_dir = statmart_facts_gen2 + "cepalstat/unemployment/"

prefix = "unemployment"
suffix = "cepalstat"
indicator_id = "127"
indicator_name = "Official unemployment rate"
indicator_category = "Economic"
indicator_type = "Unemployment"

# <markdowncell>

# We have two csv files pulled down from CEPALStat by a previous script. Lets take a look at what is in these files. First, the data file:

# <codecell>

statfile = gen_1_dir + indicator_id + "_all.csv"
df = pd.read_csv(statfile, encoding="utf-8", index_col=["ISO3"])
df[:10] # have a look at a sample of the data

# <markdowncell>

# And the metadata:

# <codecell>

metafile = gen_1_dir + indicator_id + "_meta.csv"
metamap = cepalstat_utils.parse_meta_file(metafile)
metamap

# <markdowncell>

# This part builds the csv files for each time series. The only thing we have to do is provide a function that customizes the metadata, and then have cepalstat_utils.build_files take care of the rest. Any tweaks to the default metadata values should be set in the get_metadata function.

# <codecell>

def get_metadata(iso3, meta_map):
    country = statmart_utils.get_country_by_iso3(iso3)    
    return [("name", "%s - %s [CEPALStat]" % (country, indicator_name)),
                ("originalsource", meta_map["source"]),
                ("proximatesource", "CEPALStat"),
                ("dataset", meta_map["indicator"] + " [" + indicator_id + "]"),
                ("description", meta_map["definition"]),
                ("category", indicator_category),
                ("type", indicator_type)
                ]

report = cepalstat_utils.build_files(df, get_metadata, metamap, gen_2_dir, prefix, suffix)
print("%i series saved to %s" % (len(report), gen_2_dir))
report

# <codecell>


