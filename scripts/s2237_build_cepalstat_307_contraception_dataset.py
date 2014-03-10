# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>

# <headingcell level=1>

# Build script for CEPALStat indicator #307: Contraception usage

# <markdowncell>

# This script creates csv files out of CEPALStat data, in  a format suitable for subsequent loading to the Statmart database. Each country with an available time series will have two csv files representing their data. The first contains the time series data, and the second will contain metadata about the time series. Additionally, the file "\_contraception.csv" will be created to list all the created files.

# <codecell>

import os, imp
import pandas as pd

from s0000_statmart_settings import *
import s0001_statmart_utils as statmart_utils
import s2201_cepalstat_utils as cepalstat_utils

# <markdowncell>

# Settings:

# <codecell>

gen_1_dir = statmart_facts_gen1 + "cepalstat/"
gen_2_dir = statmart_facts_gen2 + "cepalstat/contraception/"

prefix = "contraception"
suffix = "cepalstat"
indicator_id = "307"

# <markdowncell>

# We have two csv files pulled down from CEPALStat by an outside script. Lets take a look at what is in these files. First, the data file:

# <codecell>

statfile = gen_1_dir + indicator_id + "_all.csv"
df = pd.read_csv(statfile, encoding="utf-8", index_col=["ISO3"])
df[:10] # have a look at a sample of the data

# <markdowncell>

# Here is the metadata:

# <codecell>

metafile = gen_1_dir + indicator_id + "_meta.csv"
metamap = cepalstat_utils.parse_meta_file(metafile)
metamap

# <markdowncell>

# And here we build a csv file containing a yearly series of values for each country/sector combination. We create a metadata file for each one as well.

# <codecell>

imp.reload(cepalstat_utils) # just to ensure we have any recent updates to the module loaded into memory

def get_metadata(iso3, meta_map):
    country = statmart_utils.get_country_by_iso3(iso3)    
    return [("name", "%s - Contraceptive use [CEPALStat]" % (country)),
                ("originalsource", meta_map["source"]),
                ("proximatesource", "CEPALStat"),
                ("dataset", meta_map["indicator"] + " [" + indicator_id + "]"),
                ("description", meta_map["definition"]),
                ("category", "Social"),
                ("type", "Health")
                ]

report = cepalstat_utils.build_files(df, get_metadata, metamap, gen_2_dir, prefix, suffix)

print("%i series saved to %s" % (len(report), gen_2_dir))
report

# <codecell>

import imp
imp.reload(cepalstat_utils)

# <codecell>


