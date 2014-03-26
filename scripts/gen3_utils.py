# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>

# <headingcell level=1>

# Generation 3 database population library

# <codecell>

import pandas as pd
import pymysql

from settings_statmart import *

import utils_statmart as us

verbose = False

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
        data = pd.read_csv(datafile, encoding="utf-8", squeeze=False)
        data_list.append((filestem.split("/")[-1], iso3, meta, data))
    return data_list

# <codecell>

def get_translated_field(data, record, field):
    val = ""
    if field in list(data.columns): #meh
        if (pd.isnull(record[field])):
            val = ""
        else:
            val = get_translation_id(str(record[field]))
    return val
        
def standard_load_from_data_list(data_list, observation_fields="series, locationid, dateid, value, source, note"):
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
                    if pd.isnull(meta[field]):
                        values.append(None)
                    else:
                        values.append(meta[field])
                else:
                    values.append(None)
            cursor.execute(insert_series, values)

            for indx in data.index:
                record = data.ix[indx];
                values = []
                valplaces = []
                for field in observation_fields.split(","):
                    valplaces.append("%s")
                    field = field.strip()
                    if field == "dateid": #TODO: this needs to be revisited; it assumes that "year" is the only date value
                        cursor.execute("SELECT ID FROM date WHERE year = %s AND month IS NULL AND day IS NULL", [str(record["year"])])
                        dateid = list(cursor)[0][0]        
                        values.append(dateid)      
                    
                    if field == "description":
                        values.append(get_translated_field(data, record, "description"))
                
                    if field == "locationid": #TODO: this needs to be revisited
                        values.append(locationid)   
                        
                    if field == "note":        
                        values.append(get_translated_field(data, record, "note"))
                
                    if field == "series":
                        values.append(series_key)
                        
                    if field == "source":               
                        values.append(get_translated_field(data, record, "source"))     
                
                    if field == "value":
                        values.append(str(record["value"]).strip())
                                
                insert_observation = "INSERT INTO observation(" + observation_fields + ") VALUES (" + ", ".join(valplaces) + ")"
                # this logging can be very chatty
                if verbose:
                    us.log(insert_observation)
                    us.log(values)
                cursor.execute(insert_observation, values)
            cursor.execute("COMMIT")

# <codecell>

translation_id_cache = {}

def get_translation_id(strn, lang=statmart_default_language):
    cache_key = lang + " " + strn
    if cache_key in translation_id_cache:
        return translation_id_cache[cache_key]
    if len(lang) > 2: # Since 'lang' is used outside of the prepared statement, we need to protect against SQL injection
        raise Exception("Bad language: '%s' - this value must be a maximum of two characters.")
    with us.get_db_connection() as cursor:
        query = "SELECT id FROM translation WHERE " + lang + " = %s;" 
        count = cursor.execute(query, [strn])
        if count == 1:
            id = list(cursor)[0][0]
            translation_id_cache[cache_key] = id
            return id
        if count > 1:
            raise Exception("There are multiple instances of the phrase '%s' in the database. This case is not currently supported.")
        query = "INSERT INTO translation (" + lang + ") VALUES (%s);"
        cursor.execute(query, [strn.strip()])
        cursor.execute("SELECT LAST_INSERT_ID();")
        id = list(cursor)[0][0]
        translation_id_cache[cache_key] = id
        cursor.execute("COMMIT")
        return id

# <codecell>


# <codecell>


# <codecell>


