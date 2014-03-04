import pandas as pd
import pymysql
import pandas.io.sql as psql

from hashlib import sha1

from statmart_config import *

def githash(filepath):
    datafile = open(filepath,"rb")
    data = datafile.read()
    datafile.close()
    s = sha1()
    s.update(("blob %u\0" % len(data)).encode("utf-8"))
    s.update(data)
    return s.hexdigest()

def get_db_connection():
    return pymysql.connect(host=statmart_db_host, 
            port=statmart_db_port, 
            user=statmart_db_user, 
            passwd=statmart_db_passwd,
            db=statmart_db_schema)

iso3df = 0

def get_iso3_country_df():           
    return pd.read_csv(statmart_dimensions_gen2 + "base/country_base.csv", encoding="utf-8", usecols=["iso3","name"], index_col=["iso3"])

def get_country_by_iso3(iso3):
    global iso3df
    if isinstance(iso3df, int):
        iso3df = get_iso3_country_df()    
    return iso3df.ix[iso3]['name']

def get_index_set(df): 
    """Returns a set containing uniqe index values in a DataFrame."""
    myset = set()  
    for indx in df.index: 
        myset.add(indx)
    return myset