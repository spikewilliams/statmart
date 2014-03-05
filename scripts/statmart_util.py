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
    
def get_gen2_data(gen2Dir, prefix):
    """Returns all data and metadata listed in the gen2Dir/_prefix.csv file."""
    data_list = []
    filestems = pd.read_csv(gen2Dir + "_" + prefix + ".csv", encoding="utf-8", header=False, squeeze=True,  dtype={'value': object})
    for filestem in filestems:
        iso3 = filestem.split("/")[-1].split("_")[1].upper()
        metafile = gen2Dir + filestem + "_meta.csv"
        meta = pd.read_csv(metafile, encoding="utf-8", index_col=["key"], squeeze=True)
        datafile = gen2Dir + filestem + ".csv"
        data = pd.read_csv(datafile, encoding="utf-8", index_col=["year"], squeeze=True)
        data_list.append((filestem.split("/")[-1],iso3,meta,data))
    return data_list