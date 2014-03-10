# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>

# <codecell>

import pandas as pd
import pymysql
import pandas.io.sql as psql

from hashlib import sha1


from s0000_statmart_settings import *

# <markdowncell>

# Creates a MySQL database connection using the pymsql connector.

# <codecell>

def get_db_connection():
    return pymysql.connect(host=statmart_db_host, 
            port=statmart_db_port, 
            user=statmart_db_user, 
            passwd=statmart_db_passwd,
            db=statmart_db_schema)

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

# <markdowncell>

# This retrieves a set containing all unique index values in a DataFrame.

# <codecell>

def get_index_set(df): 
    myset = set()  
    for indx in df.index: 
        myset.add(indx)
    return myset

# <codecell>


