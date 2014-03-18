# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>

# <headingcell level=1>

# Generation 3 database population library

# <codecell>

import pandas as pd
import pymysql

import utils_statmart as us

# <markdowncell>

# Returns all data and metadata listed in the gen_2_dir/_prefix.csv file.

# <codecell>

def get_gen2_data(config):
    data_list = []
    filestems = pd.read_csv(config["gen_2_dir"] + "_" + config["prefix"] + ".csv", encoding="utf-8", header=None, squeeze=True,  dtype={'value': object})
    #filestems = open(config["gen_2_dir"] + "_" + config["prefix"] + ".csv", "r").readlines()
    for filestem in filestems:
        iso3 = filestem.split("/")[-1].split("_")[1].upper()
        metafile = config["gen_2_dir"] + filestem + "_meta.csv"
        meta = pd.read_csv(metafile, encoding="utf-8", index_col=["key"], squeeze=True)
        datafile = config["gen_2_dir"] + filestem + ".csv"
        data = pd.read_csv(datafile, encoding="utf-8", index_col=["year"], squeeze=False)
        data_list.append((filestem.split("/")[-1], iso3, meta, data))
    return data_list

# <codecell>

def standard_load_from_data_list(data_list):
    with us.get_db_connection() as cursor:
        for (series_key, iso3, meta, data) in data_list:
            cursor.execute("SELECT ID FROM location WHERE iso3 = %s AND divisionname IS NULL AND city IS NULL", [iso3])
            locationid = list(cursor)[0][0]
            
            cursor.execute("DELETE FROM series WHERE identifier = %s", series_key)
            cursor.execute("DELETE FROM observation WHERE series = %s", series_key)
            
            series_fields = "identifier, dataset, file, filehash, category, type, name, " + \
                            "description, originalsource, proximatesource, originalsourcelink, proximatesourcelink"
            insert_series = "INSERT INTO series (" + series_fields +") VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)" 
            values = [series_key]
            for field in series_fields.split(",")[1:]:
                field = field.strip()
                if field in meta:
                    values.append(meta[field])
                else:
                    values.append(None)
            cursor.execute(insert_series, values)
            
            for date in data.index:
                cursor.execute("SELECT ID FROM date WHERE year = %s AND month IS NULL AND day IS NULL", [str(date)])
                dateid = list(cursor)[0][0]
                observation_fields = "series, locationid, dateid, value, source, note" 
                #full list of fields: `OBSERVATIONID`, `SERIESID`, `LOCATIONID`, `DATEID`, `NOTEID`, `DESCRIPTIONID`, `VALUE`, `UNITID`, `STATUSID`
                insert_observation = "INSERT INTO observation(" + observation_fields + ") VALUES (%s, %s, %s, %s, %s, %s)"
                record = data.ix[date];
                source = ""
                if "source" in list(data.columns):
                    source = str(record["source"])
                note = ""
                if "note" in list(data.columns):
                    note = str(record["notes"])
                values  = [series_key, locationid, dateid, str(record["value"]), source, note]
                cursor.execute(insert_observation, values)
            cursor.execute("COMMIT")

