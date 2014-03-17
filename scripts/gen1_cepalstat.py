# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>

# <headingcell level=1>

# Generation 1 data fetcher library for CEPALStat

# <markdowncell>

# The functions in this library grab XML data from CEPALStat and transform it into CSV formatted files - one for the data, and another for the metadata. These files are stored in the gen1/cepalstat directory.

# <codecell>

import xml.etree.ElementTree as et
import urllib
import csv
from builtins import *
import os

import pandas as pd

from settings_statmart import *
import utils_statmart as us

gen_0_dir = statmart_facts_gen0 + "cepalstat/"
gen_1_dir = statmart_facts_gen1 + "cepalstat/"

urlroot = "http://interwp.cepal.org/sisgen/ws/cepalstat/"
cepalstat_token = "ripken8"

# <codecell>

def build_url(command,options):
	url = urlroot + command + ".asp?" + options
	url = url + "&language=english&password=" + cepalstat_token
	return url

# <codecell>

def get_countries_by_indicator(id_indicator):	
    url = build_url("getDimensions","idIndicator=" + id_indicator)
    response = urllib.request.urlopen(url)
    xml = response.read()
    tree = et.fromstring(xml)
    dims = tree.findall("dim")
    dim = dims[0] #Countries is the fist dim in the list
    clist = []
    deses = dim.findall("des") 
    for des in deses:
        if (des.attrib["in"] == "1"):
            clist.append(des.attrib["id"])
    return clist

# <codecell>

def loadCaribCountryDict(keyColumn="cepalid"):	
    countryDict = {}
    carib_country_path = statmart_dimensions_gen2 + "cepalstat/_country_caribbean.csv"
    with open(carib_country_path, 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            countryDict[row[keyColumn]] = row
    return countryDict

# <codecell>

def get_dimensions(idIndicator, countryDict):	
    url = build_url("getDimensions","idIndicator=" + idIndicator)
    response = urllib.request.urlopen(url)
    xml = response.read()
    tree = et.fromstring(xml)
    dim_dict = {}
    for dim in tree.findall("dim"):
        deses = dim.findall("des") 
        dim_map = {}
        for des in deses:
            if (des.attrib["in"] == "1"):
                if dim.attrib["id"] == "208" and not des.attrib["id"] in countryDict:
                    continue
                dim_map[des.attrib["id"]] = des.attrib["name"]
        dim_dict[dim.attrib["id"]] = {"name":dim.attrib["name"],"labels":dim_map}
    return dim_dict

#dimensions = get_dimensions("127", countryDict) 
#dimensions

# <codecell>

def build_dimension_options(dimensions):
    dims = []
    for key in dimensions.keys():
        if key=="1240": #do not pass in key for "years"; we want all by defalt, and it can make the URL too long for CepalStat to handle
            continue
        labels = dimensions[key]["labels"]
        keys = sorted(list(labels.keys()))
        dims.append("dim_%s=%s" % (key,",".join(keys)))
    return "&".join(sorted(dims))

# <codecell>

def get_data_by_indicator(id_indicator):	
    dimensions = get_dimensions(id_indicator, loadCaribCountryDict())
    url = build_url("getDataMeta","idIndicator=" + id_indicator + "&" + build_dimension_options(dimensions))
    us.log(url)
    us.log(dimensions)
    response = urllib.request.urlopen(url)
    xml = response.read()
    tree = et.fromstring(xml)
    datos = tree.findall("datos")[0].findall("dato")
    data = []
    for dat in datos:
        row = []
        for dim in dimensions.keys():
            key = dat.attrib["dim_" + dim]
            row.append(dimensions[dim]["labels"][key])
            #print(dimensions[key]["name"])
        row.append(dat.attrib["valor"])
        row.append(dat.attrib["id_fuente"])
        row.append(dat.attrib["ids_notas"])
        row.append(dat.attrib["iso3"])
        data.append(row)
    cols = list(map(lambda k : dimensions[k]["name"], list(dimensions.keys())))+ ["Value","Source","Notes","ISO3"]
    cols[cols.index("Countries")] = "Country"
    cols[cols.index("Years")] = "Year"
    df = pd.DataFrame(data, columns=cols)
    newCols = ["Year","Value","Source","Notes","ISO3"]
    for key in cols:
        if not key in newCols: # This is O^2
            newCols.append(key)
    df = df.reindex_axis(newCols, axis=1)
    return (df, get_metadata_from_tree(tree))

#get_data_by_indicator("861")


#http://interwp.cepal.org/sisgen/ws/cepalstat/getDataMeta.asp?dIndicator=2137&language=spanish&dim_10463=10464&dim_28645=28646&dim_28648=28663,28652,28650&password=ripken8

# <codecell>

def get_metadata_by_indicator(id_indicator):	
    dimensions = get_dimensions(id_indicator, loadCaribCountryDict())
    url = build_url("getDataMeta","idIndicator=" + id_indicator + "&" + build_dimension_options(dimensions))
    #print(url)
    response = urllib.request.urlopen(url)
    xml = response.read()
    tree = et.fromstring(xml)
    return get_metadata_from_tree(tree)

def get_metadata_from_tree(tree):
    md = tree.findall("metadatos")[0]
    rows = []
    rows.append([5000000,"indicator-id",         md.attrib["idIndicator"]])
    rows.append([5000001,"indicator",            md.attrib["indicador"]])
    rows.append([5000002,"theme",                md.attrib["tema"]])
    rows.append([5000003,"area",                 md.attrib["area"]])
    rows.append([5000004,"indicator-note",       md.attrib["nota"]])
    rows.append([5000005,"unit",                 md.attrib["unidad"]])
    rows.append([5000006,"definition",           md.attrib["definicion"]])
    rows.append([5000007,"data-charactaristics", md.attrib["caracteristicas_dato"]])
    rows.append([5000008,"methodology",          md.attrib["metodologia_calculo"]])
    rows.append([5000009,"commentary",           md.attrib["comentarios"]]) 
    notas = tree.findall("notas")[0].findall("nota")
    for nota in notas:
        rows.append([int(nota.attrib["id"]), "note", nota.attrib["descripcion"]])
    fuentes = tree.findall("fuentes")[0].findall("fuente")
    for fuente in fuentes:
        rows.append([int(fuente.attrib["id"]), "source", fuente.attrib["nombre_organismo"] + ": " + fuente.attrib["descripcion"]])
    return pd.DataFrame(rows, columns=["ID","Key","Value"]) 
   
#get_metadata_by_indicator('127')

# <codecell>

def save_as_csv(path, df, country, prefix, suffix=""):
    c = country.strip().lower().replace(" ","-")
    filename = path + prefix + "_" + c
    if suffix:
        filename = filename + "_" + suffix
    filename = filename + ".csv"
    df.to_csv(filename, encoding="utf-8", index=False)

#iso3Dict = loadCaribCountryDict("iso3")
def make_country_data_files(indicator, sort=["Year"]):
    countryDict = loadCaribCountryDict()
    countries = get_countries_by_indicator(indicator)
    (df,mdf) = get_data_by_indicator(indicator)
    df = df.sort(sort)
    save_as_csv(gen_1_dir, df, "all", indicator)
    save_as_csv(gen_1_dir, mdf, "meta", indicator)
    
#make_country_data_files("2216", sort=["Year","Item"]) #GDP by sector
#make_country_data_files("861")

# <codecell>

def download(config):
    return make_country_data_files(config["indicator_id"], sort=["Year"]) #Contraception

# <codecell>

#make_country_data_files("307", sort=["Year"]) #Contraception

# <codecell>

#make_country_data_files("468", sort=["Year"]) #Hospital Beds

# <codecell>

#makeCountryDataFiles("465", sort=["Year"]) #Occupied Units

# <codecell>

#makeCountryDataFiles("861", sort=["Year"]) #External Debt

# <codecell>

#makeCountryDataFiles("642", sort=["Year"]) #Agricultural sector product value

# <codecell>

#makeCountryDataFiles("764", sort=["Year"]) #Core inflation

# <codecell>

#makeCountryDataFiles("365", sort=["Year"]) #Consumer price index

# <codecell>

#makeCountryDataFiles("357", sort=["Year"]) #Death rate tuberculosis

# <codecell>

#makeCountryDataFiles("1693", sort=["Year"]) #Incidence rate tuberculosis

# <codecell>

#makeCountryDataFiles("1010", sort=["Year"]) #Prison population rate

# <codecell>

#makeCountryDataFiles("2179", sort=["Year"]) #Nominal exchange rate

# <codecell>

#makeCountryDataFiles("127", sort=["Year"]) #Unemployment rate

# <codecell>

"""    try:
        os.makedirs(path)
    except FileExistsError:
        pass"""

# <codecell>


