# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>

# <codecell>

import os
import pandas as pd
import pymysql
import pandas.io.sql as psql
import csv
import string
from hashlib import sha1

from settings_statmart import *

# <markdowncell>

# Creates a MySQL database connection using the pymsql connector.

# <codecell>

def get_db_connection():
    return pymysql.connect(host=statmart_db_host, 
            port=statmart_db_port, 
            user=statmart_db_user, 
            passwd=statmart_db_passwd,
            db=statmart_db_schema,
            charset='utf8')

# <markdowncell>

# Gets an SHA1 encryption of a file using the same encryption method as git. Note that this has not yet been validated for its intended git compatability.

# <codecell>

def githash(filepath):
    datafile = open(filepath,"rb")
    data = datafile.read()
    datafile.close()
    s = sha1()
    s.update(("blob %u\0" % len(data)).encode("utf-8"))
    s.update(data)
    return s.hexdigest()

# <codecell>

def format_lower_no_spaces(strn):
    return(strn.strip().lower().replace(" ","-"))

def machine_name(s):
    exclude = set(string.punctuation)
    s = ''.join(ch for ch in s if ch not in exclude)
    name = format_lower_no_spaces(s)[0:32]
    return name

# <markdowncell>

# These functions retrieve data from country_base.csv, for use in processing datasets.

# <codecell>

iso3df = 0

def get_iso3_country_df():
    return pd.read_csv(statmart_dimensions_gen2 + "base/country_base.csv", encoding="utf-8", usecols=["iso3","name"], index_col=["iso3"])

def get_country_by_iso3(iso3):
    global iso3df
    if isinstance(iso3df, int):
        iso3df = get_iso3_country_df()
    return iso3df.ix[iso3]['name']

# <codecell>

countrydf = 0

def get_country_iso3_df():
    return pd.read_csv(statmart_dimensions_gen2 + "base/country_base.csv", encoding="utf-8", usecols=["iso3","countryname"])

def get_iso3_by_country(country):
    global countrydf
    if isinstance(countrydf, int):
        countrydf = get_country_iso3_df()
        countrydf["lname"] = [format_lower_no_spaces(x) for x in countrydf["countryname"]]
        countrydf = countrydf.set_index(["lname"])
    return countrydf.ix[format_lower_no_spaces(country)]['iso3']

#get_iso3_by_country("Barbados")


# <markdowncell>

# This retrieves a set containing all unique index values in a DataFrame.

# <codecell>

def get_index_set(df): 
    myset = set()  
    for indx in df.index: 
        myset.add(indx)
    return myset

# <codecell>

def build_config(group, prefix, indicator_id, indicator, category, itype):
    config = {"gen_1_dir": statmart_facts_gen1 + group + "/",
              "gen_2_dir": statmart_facts_gen2 + group + "/" + prefix + "/",
              "gen_4_dir": statmart_view_gen4 + group + "/",
              "prefix":prefix,
              "suffix":"cepalstat",
              "indicator_id":indicator_id,
              "indicator":indicator,
              "indicator_type":itype,
              "indicator_category":category,
              "multiplier":1}
    return config

# <codecell>

def get_gen2_data(gen_2_dir, prefix):
    data_list = []
    filestems = pd.read_csv(gen_2_dir + "_" + prefix + ".csv", encoding="utf-8", header=False, squeeze=True,  dtype={'value': object})
    for filestem in filestems:
        iso3 = filestem.split("/")[-1].split("_")[1].upper()
        metafile = gen_2_dir + filestem + "_meta.csv"
        meta = pd.read_csv(metafile, encoding="utf-8", index_col=["key"], squeeze=True)
        datafile = gen_2_dir + filestem + ".csv"
        data = pd.read_csv(datafile, encoding="utf-8", index_col=["year"], squeeze=True)
        data_list.append((filestem.split("/")[-1],iso3,meta,data))
    return data_list

# <codecell>

verbose = False
def log(str):
    if verbose:
        print(str)

# <codecell>

def multiply_data(df, columns, config):
    if not hasattr(df,"multiplied_flag"):
        for col in columns:
            df[col] = df[col].apply(lambda x : x * config["multiplier"]).astype(int)
    else:
        log("WARNING: you must reinitialize the DataFrame before running this code a second time.")
    df.multiplied_flag = True
    return df

# <codecell>

# Deprecated
def load_carib_country_dict(key_column="iso3"):	
    country_dict = {}
    carib_country_path = statmart_dimensions_gen2 + "cepalstat/_country_caribbean.csv"
    with open(carib_country_path, 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            country_dict[row[key_column]] = row
    return country_dict

# <codecell>

def mkdirs(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)

