# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>

# <headingcell level=1>

# Load script for CEPALStat indicator \#127: Unemployment.

# <markdowncell>

# This script imports csv formatted data (generation 2) into the database (generation 3.)
# 
# This script will import data from all files listed in "data/facts/gen2/cepalstat/contraception/_unemployment.csv".

# <codecell>

import os.path
import pandas as pd
import pymysql
import pandas.io.sql as psql

from s0000_statmart_settings import *
import s0001_statmart_utils as statmart_utils
import s3001_load_utils as load_utils

# <markdowncell>

# Settings:

# <codecell>

gen_2_dir = statmart_facts_gen2 + "cepalstat/unemployment/"

prefix = "unemployment"
suffix = "cepalstat"
indicator_id = "127"

# <markdowncell>

# Bring in all the data and metadata using the load\_utils.get\_gen2\_data function. The data is returned as an array of tupples. Each tupple contains the "series key", the ISO3 value of the country, the meta DataFrame, and the dataset DataFrame. 

# <codecell>

data_list = load_utils.get_gen2_data(gen_2_dir, prefix)
data_list[0:3] # have a look at a sample of the data

# <markdowncell>

# Insert the data from data_list into the MySQL database

# <codecell>

load_utils.standard_load_from_data_list(data_list)

# <markdowncell>

# Here is an example of how to make an SQL query to retrieve data in the series:

# <codecell>

df = ""
with statmart_utils.get_db_connection() as cursor:
    query = """
            SELECT L.iso3, L.countryname, D.year, O.value 
            FROM observation as O 
            INNER JOIN date as D    ON O.dateid = D.id
            INNER JOIN location as L    ON O.locationid = L.id
            WHERE O.series like 'unemployment\_%\_cepalstat'
            ORDER BY D.year
            """
    df = psql.frame_query(query, con=cursor.connection)
    
df

# <codecell>


# <codecell>

import imp
imp.reload(load_utils)

# <codecell>


