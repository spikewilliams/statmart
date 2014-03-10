# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>

# <codecell>

import pandas as pd
import pymysql
import pandas.io.sql as psql

from hashlib import sha1

from s0000_statmart_settings import *
import s0001_statmart_utils as statmart_utils

pd.options.mode.chained_assignment = None  # turn off a noisy pandas warning that doesn't apply to our case

# <codecell>

def parse_meta_file(metafile):
    metamap = {}
    
    mf = pd.read_csv(metafile, encoding="utf-8")
    source = mf.ix[mf["Key"] == "source"]["Value"]
    metamap["source"] = clip_period(source[source.index[0]])
    
    indicator = mf.loc[mf["Key"] == "indicator"]["Value"]
    metamap["indicator"] = clip_period(indicator[indicator.index[0]])
    
    definition = mf.loc[mf["Key"] == "definition"]["Value"]
    metamap["definition"] = clip_period(definition[definition.index[0]])
    
    nf = mf.loc[mf["Key"] == "note"][["ID","Value"]]
    nf = nf.set_index(["ID"])

    for index in statmart_utils.get_index_set(nf):
        note = nf.ix[index]["Value"].strip()
        note = clip_period(note)
        metamap[index] = note
    return metamap

def get_notes(notes, mmap):
    notes = notes.split(",")
    return "|".join(map(lambda x : mmap[int(x)], notes))
    
    
 #   get_notes("4422,5170")

# <rawcell>

# build_files(df, meta_function, gen_2_dir, prefix, suffix)
# 
# This will write all the data files and metadata files to the gen_2_dir directory.
# 
# Parameters:
#     - df - A DataFrame with national ISO3 values as the index
#     - meta_function - a function that will return an array of tupples. Each tuple will correspond to a line in the metadata file, and may be uploaded to the Series table of the database during the "load" process
#     - meta_map containing metadata values, including such values as "source", "indicator", "definition", and various notes, identified by their number
#     - gen_2_dir - the directory these files will be going into
#     - prefix - a prefix for the .csv files, generally corresponding to the name of the indicator
#     - suffix - a suffix for the .csv files, generally corresponding to the name of the source
# 
# Each csv file will be named prefix\_iso\_suffix.csv and each metadata file will be named prefix\_iso\_suffix\_meta.csv. Additionally, prefix\_iso\_suffix will be used as the Series indicators for this data in the database.

# <codecell>

def build_files(df, meta_function, meta_map, gen_2_dir, prefix, suffix):
    filelist = []
    countrylist = []
    for iso3 in statmart_utils.get_index_set(df):
        try:
            idf = df.ix[iso3]
            if type(idf) == pd.Series: #idf a Series if there is only one element in it, but we want a DataFrame always
                idf = pd.DataFrame([idf])
            idf = idf[["Year","Value","Source","Notes"]]
            idf.columns = ["year","value","source","notes"]
            idf["source"] = idf["source"].apply(lambda x : meta_map["source"])
            idf["notes"] = idf["notes"].apply(lambda x : get_notes(str(x), meta_map))
            filestem = prefix + "_" + iso3.lower() + "_" + suffix
            filename = filestem + ".csv"
            filepath = gen_2_dir + filename
            idf.to_csv(filepath, encoding="utf8", index=False)
        
            meta = meta_function(iso3, meta_map)
            meta.append(("file", filename))
            meta.append(("filehash", statmart_utils.githash(filepath)))
            meta.append(("columns", "year,value,source,notes"))        
            metafile = gen_2_dir + filestem + "_meta.csv"    
            pd.DataFrame(meta,columns = ["key","value"]).to_csv(metafile, encoding="utf8", index=False)
            filelist.append([filestem])
            countrylist.append(statmart_utils.get_country_by_iso3(iso3))
        except Exception as strerror:
            print ("ERROR: Failed to build data for %s" % iso3)
            print (strerror)
            
    fldf = pd.DataFrame(filelist, index=countrylist).sort_index()
    fldf.to_csv(gen_2_dir + "_" + prefix + ".csv", encoding="utf8", float_format='%.1f', index=False, header=False)
    return fldf

# <markdowncell>

# The data is inconsistant with use of the period at the end of a note. So we strip them all

# <codecell>

def clip_period(str):
    if str[-1] == ".":
        str = str[0:-1]    
    return str

# <codecell>


