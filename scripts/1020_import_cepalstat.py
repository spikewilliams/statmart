# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>

# <codecell>

from bs4 import BeautifulSoup  #pip install beautifulsoup4
import urllib
import lxml   #
import csv
from builtins import *
import os

from s0000_statmart_settings import *
import s0001_statmart_utils as statmart_utils

gen_0_dir = statmart_facts_gen0 + "cepalstat/"
gen_0_dir = statmart_facts_gen1 + "cepalstat/"

prefix = "unemployment"
suffix = "cepalstat"
indicator = "127"

cepalstat_token = "ripken8"

# <codecell>

urlroot = "http://interwp.cepal.org/sisgen/ws/cepalstat/"

def build_url(command,options):
	url = urlroot + command + ".asp?" + options
	url = url + "&language=english&password=" + cepalstat_token
	return url

# <codecell>

def get_countries_by_indicator(id_indicator):	
	url = build_url("getDimensions","idIndicator=" + id_indicator)
	#print(url)
	response = urllib.request.urlopen(url)
	xml = response.read()

	soup = BeautifulSoup(xml,"xml")
	dims = soup.find_all("dim")
	dim = next(iter(dims)) #Countries is the fist dim in the list
	clist = []
	deses = dim.find_all("des") 
	for des in deses:
		if (des["in"] == "1"):
			clist.append(des["id"])
	return clist
print (get_countries_by_indicator(indicator))

# <codecell>

def loadCaribCountryDict(keyColumn="cepalid"):	
	countryDict = {}
    
    carib_country_path = statmart_dimensions_gen2 + "cepalstat/_country_caribbean.csv"
	with open(carib_country_path", 'r') as csvfile:
		reader = csv.DictReader(csvfile)
		for row in reader:
			countryDict[row[keyColumn]] = row
	return countryDict

# <codecell>

countryDict = loadCaribCountryDict("cepalid")
countryDict

# <codecell>

def getDimensions(idIndicator, countryDict):	
    url = buildURL("getDimensions","idIndicator=" + idIndicator)
    response = urllib.request.urlopen(url)
    xml = response.read()
    soup = BeautifulSoup(xml,"xml")
    dimDict = {}
    for dim in soup.find_all("dim"):
        #print(dim["name"] + " " + dim["id"])
        deses = dim.find_all("des") 
        dimMap = {}
        for des in deses:
            if (des["in"] == "1"):
                if dim["id"] == "208" and not des["id"] in countryDict:
                    continue
                dimMap[des["id"]] = des["name"]
        dimDict[dim["id"]] = {"name":dim["name"],"labels":dimMap}
    return dimDict

dimensions = getDimensions("307", countryDict) 
dimensions

# <codecell>

def buildDimensionOptions(dimensions):
    dims = []
    for key in dimensions.keys():
        if key=="1240": #do not pass in years; we want all by defalt, and it can make the URL too long for CepalStat to handle
            continue
        labels = dimensions[key]["labels"]
        keys = sort(list(labels.keys()))
        dims.append("dim_%s=%s" % (key,",".join(keys)))
    return "&".join(sort(dims))
buildDimensionOptions(dimensions)

# <codecell>

def getDataByIndicator(idIndicator):	
    dimensions = getDimensions(idIndicator, loadCaribCountryDict())
    url = buildURL("getDataWithoutMeta","idIndicator=" + idIndicator + "&" + buildDimensionOptions(dimensions))
    print(url)
    response = urllib.request.urlopen(url)
    xml = response.read()
    soup = BeautifulSoup(xml,"xml")
    datos = soup.find_all("dato")
    for dat in datos:
        print(dat)
        for dim in dimensions.keys():
            key = dat["dim_" + dim]
            #print(dimensions[key][name])
        #print(dat["valor"])
getDataByIndicator('307')

#http://interwp.cepal.org/sisgen/ws/cepalstat/getDataMeta.asp?dIndicator=2137&language=spanish&dim_10463=10464&dim_28645=28646&dim_28648=28663,28652,28650&password=ripken8

# <codecell>

",".join(["bar","baz"])

# <codecell>

sort(["bar","faz"])

# <codecell>

df[["Country","ISO3"]].drop_duplicates()

# <codecell>

def getDataByIndicator(idIndicator):	
    dimensions = getDimensions(idIndicator, loadCaribCountryDict())
    url = buildURL("getDataMeta","idIndicator=" + idIndicator + "&" + buildDimensionOptions(dimensions))
    print(url)
    #print dimensions
    response = urllib.request.urlopen(url)
    xml = response.read()
    soup = BeautifulSoup(xml,"xml")
    datos = soup.find_all("dato")
    data = []
    for dat in datos:
        row = []
        for dim in dimensions.keys():
            key = dat["dim_" + dim]
            row.append(dimensions[dim]["labels"][key])
            #print(dimensions[key]["name"])
        row.append(dat["valor"])
        row.append(dat["id_fuente"])
        row.append(dat["ids_notas"])
        row.append(dat["iso3"])
        data.append(row)
    cols = list(map(lambda k : dimensions[k]["name"], list(dimensions.keys()))) + ["Value","Source","Notes","ISO3"]
    cols[cols.index("Countries")] = "Country"
    cols[cols.index("Years")] = "Year"
    return (pd.DataFrame(data, columns=cols), getMetaDataFromSoup(soup))


#http://interwp.cepal.org/sisgen/ws/cepalstat/getDataMeta.asp?dIndicator=2137&language=spanish&dim_10463=10464&dim_28645=28646&dim_28648=28663,28652,28650&password=ripken8

# <codecell>

(df,mdf) = getDataByIndicator('2216')

# <codecell>

list(map(lambda k : dimensions[k]["name"], list(dimensions.keys())))

# <codecell>

df = getDataByIndicator('307')
mydf = df[["Countries","Years","Value","Source","Notes"]]
mydf.columns=["Country","Year","Value","Source","Notes"]

# <codecell>

df.sort(["Countries","Years"])

# <codecell>

myd.columns=["ISO3","Country","Year","Value","Source","Notes"]

# <codecell>


# <codecell>

def getMetaDataByIndicator(idIndicator):	
    dimensions = getDimensions(idIndicator, loadCaribCountryDict())
    url = buildURL("getDataMeta","idIndicator=" + idIndicator + "&" + buildDimensionOptions(dimensions))
    print(url)
    #print dimensions
    response = urllib.request.urlopen(url)
    xml = response.read()
    soup = BeautifulSoup(xml,"xml")
    return getMetaDataFromSoup(soup)

def getMetaDataFromSoup(soup):
    md = soup.find("metadatos")
    rows = []
    rows.append([5000000,"indicator-id",md["idIndicator"]])
    rows.append([5000001,"indicator",md["indicador"]])
    rows.append([5000002,"theme",md["tema"]])
    rows.append([5000003,"area",md["area"]])
    rows.append([5000004,"indicator-note",md["nota"]])
    rows.append([5000005,"unit",md["unidad"]])
    rows.append([5000006,"definition",md["definicion"]])
    rows.append([5000007,"data-charactaristics",md["caracteristicas_dato"]])
    rows.append([5000008,"methodology",md["metodologia_calculo"]])
    rows.append([5000009,"commentary",md["comentarios"]]) 
    notas = soup.find_all("nota")
    for nota in notas:
        rows.append([int(nota["id"]), "note", nota["descripcion"]])
    fuentes = soup.find_all("fuente")
    for fuente in fuentes:
        rows.append([int(fuente["id"]), "source", fuente["nombre_organismo"] + ": " + fuente["descripcion"]])
    return pd.DataFrame(rows, columns=["ID","Key","Value"]) 
   
getMetaDataByIndicator('872')

# <codecell>

getMetaDataByIndicator('2216')

# <codecell>

mdf.ix[1]["Value"]

# <codecell>

df[df["Country"] == "Antigua and Barbuda"]
             

# <codecell>

def saveAsCSV(path, df, country, prefix, suffix=""):
    c = country.strip().lower().replace(" ","-")
    filename = path + prefix + "_" + c
    if suffix:
        filename = filename + "_" + suffix
    filename = filename + ".csv"
    df.to_csv(filename, encoding="utf-8", index=False)

#iso3Dict = loadCaribCountryDict("iso3")
def makeCountryDataFiles(indicator, sort=["Year"]):
    path = dataroot + indicator + "/"
    try:
        os.makedirs(path)
    except FileExistsError:
        pass
    countryDict = loadCaribCountryDict()
    countries = getCountriesByIndicator(indicator)
    (df,mdf) = getDataByIndicator(indicator)
    df = df.sort(sort)
    for c in countries:
        if c in countryDict:
            cdf = df[df["ISO3"] == countryDict[c]["iso3"]]
            saveAsCSV(path, cdf, countryDict[c]["iso3"], indicator)
    saveAsCSV(path, df, "all", indicator)
    saveAsCSV(path, mdf, "meta", indicator)
    
makeCountryDataFiles("2216", sort=["Year","Item"]) #GDP by sector
               
def getCountryData(country, sort=["Year"]):
    df[df["Country"] == "Bahamas"].sort(["Year","Item"])

# <codecell>

makeCountryDataFiles("307", sort=["Year"]) #Contraception

# <codecell>

makeCountryDataFiles("468", sort=["Year"]) #Hospital Beds

# <codecell>

makeCountryDataFiles("465", sort=["Year"]) #Occupied Units

# <codecell>

makeCountryDataFiles("861", sort=["Year"]) #External Debt

# <codecell>

makeCountryDataFiles("642", sort=["Year"]) #Agricultural sector product value

# <codecell>

makeCountryDataFiles("764", sort=["Year"]) #Core inflation

# <codecell>

makeCountryDataFiles("365", sort=["Year"]) #Consumer price index

# <codecell>

makeCountryDataFiles("357", sort=["Year"]) #Death rate tuberculosis

# <codecell>

makeCountryDataFiles("1693", sort=["Year"]) #Incidence rate tuberculosis

# <codecell>

makeCountryDataFiles("1010", sort=["Year"]) #Prison population rate

# <codecell>

makeCountryDataFiles("2179", sort=["Year"]) #Nominal exchange rate

# <codecell>

makeCountryDataFiles("127", sort=["Year"]) #Unemployment rate

# <codecell>


def getCountryData(indicator,iso3, sort=["Year"]):
    (df,mdf) = getDataByIndicator(indicator)
    df = df.sort(sort)
    cdf = df[df["ISO3"] == iso3]
    return (cdf, mdf) 

(df,mdf) = getCountryData("2216", "TTO", sort=["Year","Item"]) #GDP by sector
df

# <codecell>


# <codecell>

def makeGDPPlot(iso3, countryName):
    (df,mdf) = getCountryData("2216", iso3, sort=["Year","Item"]) #GDP by sector
    gdp = df[df["Item"] == "Gross domestic product (GDP)"]
    gdp = gdp[['Year','Value']]
    gdp['Year'] = gdp['Year'].astype(int)
    gdp['Value'] = gdp['Value'].astype(float)
    return gdp.plot(x="Year",y="Value",title="", kind="line",figsize=(5,3))

# <codecell>

plot = makeGDPPlot("BHS","The Bahamas")
fig = plt.gcf()
fig.savefig(dataroot + "bhs.png")

# <codecell>

fig = plt.gcf()
fig.savefig(dataroot + "bhs.png")

# <codecell>

plot = makeGDPPlot("ATG","Antigua and Barbuda")
fig = plt.gcf()
fig.savefig(dataroot + "atg.png")

# <codecell>

import bs4
bs4.builder.builder_registry.builders

# <codecell>

import lxml.etree

# <codecell>


