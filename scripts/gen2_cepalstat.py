# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>

# <headingcell level=1>

# Generation 2 CSV file builder library for CEPALStat

# <markdowncell>

# This script creates csv files out of CEPALStat data, in  a format suitable for subsequent loading to the Statmart database. Each country with an available time series will have two csv files representing their data. The first contains the time series data, and the second will contain metadata about the time series. Additionally, the file "\_PREFIX.csv" will be created to list all the created files.

# <markdowncell>

# A full set of stats for an indicator is stored in a file called XXX_all.csv, where XXX is the ID of the indicator, as found in CEPALStat

# <codecell>

import os, imp, sys, traceback
import pandas as pd

from settings_statmart import *
import utils_statmart as us
import gen1_cepalstat

# <codecell>


# <codecell>

def parse_meta_file(metafile):
    metamap = {}
    
    mf = pd.read_csv(metafile, encoding="utf-8")
    source = mf.ix[mf["Key"] == "source"]["Value"]
    if len(source) > 0:
        metamap["source"] = clip_period(source[source.index[0]].strip())
    
    indicator = mf.loc[mf["Key"] == "indicator"]["Value"]
    metamap["indicator"] = clip_period(indicator[indicator.index[0]].strip())
    
    definition = mf.loc[mf["Key"] == "definition"]["Value"]
    if len("definition") > 0:
        metamap["definition"] = clip_period(definition[definition.index[0]].strip())
    
    nf = mf.loc[mf["Key"] == "note"][["ID","Value"]]
    nf = nf.set_index(["ID"])

    for index in us.get_index_set(nf):
        note = nf.ix[index]["Value"].strip()
        note = clip_period(note)
        metamap[str(index)] = note
    return metamap

def get_notes(notes, mmap):
    if notes == "nan":
        return ""
    notes = notes.split(",")
    mynotes = []
    for note in notes:
        if note in mmap:
            mynotes.append(note)
    return "|".join(map(lambda x : mmap[str(x)], mynotes))

def clip_period(str):
    if str[-1] == ".":
        str = str[0:-1]    
    return str

# <codecell>

def build_files(df, config):
    filelist = []
    countrylist = []
    for iso3 in us.get_index_set(df):
        try:
            idf = df.ix[iso3]
            if type(idf) == pd.Series: #idf a Series if there is only one element in it, but we want a DataFrame always
                idf = pd.DataFrame([idf])
            idf = idf[["Year","Value","Source","Notes"]]
            idf.columns = ["year","value","source","notes"]
            mult = config["multiplier"]
            if mult:
                if (mult <= 1 and mult >= -1) or not type(mult) is int:
                    idf["value"] = idf["value"].apply(lambda x : x * mult)
                else:
                    idf["value"] = idf["value"].apply(lambda x : int(x * mult)).astype(object)
            idf["source"] = idf["source"].apply(lambda x : config["source"])
            idf["notes"] = idf["notes"].apply(lambda x : get_notes(str(x), config))
            filestem = config["prefix"] + "_" + iso3.lower() + "_" + config["suffix"]
            filename = filestem + ".csv"
            filepath = config["gen_2_dir"] + filename
            us.log(filepath)
            idf.to_csv(filepath, encoding="utf8", index=False)
                   
            country = us.get_country_by_iso3(iso3)    
            meta = [("name", "%s - %s [CEPALStat]" % (country, config["indicator"])),
                ("originalsource", config["source"]),
                ("proximatesource", "CEPALStat"),
                ("dataset", config["indicator"] + " [" + config["indicator_id"] + "]"),
                ("description", config["definition"]),
                ("category", config["indicator_category"]),
                ("type", config["indicator_type"]),
                ("file", filename),
                ("filehash", us.githash(filepath)),
                ("columns", "year,value,source,notes")
                ]
     
            metafile = config["gen_2_dir"] + filestem + "_meta.csv"    
            pd.DataFrame(meta,columns = ["key","value"]).to_csv(metafile, encoding="utf8", float_format='%.3f',index=False)
            filelist.append([filestem])
            countrylist.append(country)
        except Exception as strerror:
            us.log("ERROR: Failed to build data for %s" % iso3)
            us.log(sys.exc_info())
            traceback.print_tb(sys.exc_info()[2])
            
    fldf = pd.DataFrame(filelist, index=countrylist).sort_index()
    fldf.to_csv(config["gen_2_dir"] + "_" + config["prefix"] + ".csv", encoding="utf8", float_format='%.1f', index=False, header=False)
    return fldf

# <markdowncell>

# This is what gets called by build scripts. The config object should contain all required variables; it can be generated using utils_statmart.build_config().

# <codecell>

def build(config):
    statfile = config["gen_1_dir"] + config["indicator_id"] + "_all.csv"
    df = pd.read_csv(statfile, encoding="utf-8", index_col=["ISO3"], dtype={'Notes':'object'} )
    metafile = config["gen_1_dir"] + config["indicator_id"] + "_meta.csv"
    metamap = parse_meta_file(metafile)
    metamap.update(config) # this enables customizations in config to override entries in the meta file
    report = build_files(df, metamap)
    us.log("%i series saved to %s" % (len(report), config["gen_2_dir"]))
    return report
    

