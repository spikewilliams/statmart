# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>

# <codecell>

import pandas as pd

from settings_statmart import *
import utils_statmart as us

# <codecell>

gen_0_dir = statmart_facts_gen0 + "sidsrcm/"
gen_1_dir = statmart_facts_gen0 + "sidsrcm/"
gen_2_dir = statmart_facts_gen0 + "sidsrcm/"

tmpDir = "C:/tmp/"

water = [{
    "description":"Reservoirs",
    "descriptor":"reservoirs",
    "fileName":"Water_1a_Reservoirs.xlsx",
    "generation":"0",
    "path":"water/",
    "timeseries":False
},{
    "description":"Water desalination plants",
    "descriptor":"desalination",
    "fileName":"Water_1c_Desalination.xlsx",
    "generation":"0",
    "path":"water/",
    "timeseries":False
},{
    "description":"Rainfall",
    "descriptor":"rainfall",
    "fileName":"Water_2_Rainfall.xlsx",
    "generation":"0",
    "path":"water/",
    "timeseries":True
},{
    "description":"Evapotranspiration",
    "descriptor":"evapotranspiration",
    "fileName":"Water_3_Evapotrans.xlsx",
    "generation":"0",
    "path":"water/",
    "timeseries":True
},{
    "description":"Surface water",
    "descriptor":"surface",
    "fileName":"Water_4a_Surfacewater.xlsx",
    "generation":"0",
    "path":"water/",
    "timeseries":False
},{
    "description":"Groundwater",
    "descriptor":"ground",
    "fileName":"Water_4b_Groundwater.xlsx",
    "generation":"0",
    "path":"water/",
    "timeseries":True
},{
    "description":"Regional demand",
    "descriptor":"regional-demand",
    "fileName":"Water_5c_RegionalDemand.xlsx",
    "generation":"0",
    "path":"water/",
    "timeseries":True
},{
    "description":"Water employment",
    "descriptor":"water-employment",
    "fileName":"Water_11_WaterEmployment.xlsx",
    "generation":"0",
    "path":"water/",
    "timeseries":True
}] 

'''{
    "description":"Water usage",
    "descriptor":"usage",
    "fileName":"Water_5a_Waterusage.xlsx",
    "generation":"0",
    "path":"rcm/water/",
    "timeseries":True
},,{
    "description":"Households connected",
    "descriptor":"households-connected",
    "fileName":"Water_5d_HouseholdsConnected.xlsx",
    "generation":"0",
    "path":"rcm/water/",
    "timeseries":True
},{
    "description":"Sectoral demand",
    "descriptor":"sectoral-demand",
    "fileName":"Water_5b_SectoralDemand.xlsx",
    "generation":"0",
    "path":"rcm/water/",
    "timeseries":True
},
,{
    "description":"Water production",
    "descriptor":"water-production",
    "fileName":"Water_5e_WaterProduction.xlsx",
    "generation":"0",
    "path":"rcm/water/",
    "timeseries":True
},,{
    "description":"Consumer budget",
    "descriptor":"consumer-budget",
    "fileName":"Water_11b_ConsumerBudget.xlsx",
    "generation":"0",
    "path":"rcm/water/",
    "timeseries":True
},{
    "description":"Potable water",
    "descriptor":"potable",
    "fileName":"Water_11c_PotableWater.xlsx",
    "generation":"0",
    "path":"rcm/water/",
    "timeseries":True
}'''


energy = [{
    "description":"Number of vehicles",
    "descriptor":"number-of-vehicles",
    "fileName":"Energy_6a_NumVehicles.xlsx",
    "generation":"0",
    "path":"energy/",
    "timeseries":True
},{
    "description":"Estimated length of road network",
    "descriptor":"road-network",
    "fileName":"Energy_6i_RoadNetwork.xlsx",
    "generation":"0",
    "path":"energy/",
    "timeseries":True
},{
    "description":"Number of businesses",
    "descriptor":"businesses",
    "fileName":"Energy_6j_Businesses.xlsx",
    "generation":"0",
    "path":"energy/",
    "timeseries":True
},{
    "description":"Employment in energy generation",
    "descriptor":"energy-employment",
    "fileName":"Energy_10a_EnergyEmployment.xlsx",
    "generation":"0",
    "path":"energy/",
    "timeseries":True
},{
    "description":"Percentage of households with access to electricity",
    "descriptor":"electricity-access",
    "fileName":"Energy_10c_Electricity Access.xlsx",
    "generation":"0",
    "path":"energy/",
    "timeseries":True
}] 
"""
{
    "description":"Electric price index",
    "descriptor":"electric-price-index",
    "fileName":"Energy_4b_ElecPriceIndex.xlsx",
    "generation":"0",
    "path":"rcm/energy/",
    "timeseries":True
},

"""

# <codecell>

def getXLFile(config):
    filePath = gen_0_dir + "/" + config["path"] + "/" + config["fileName"]
    xlFile = pd.ExcelFile(filePath)
    return xlFile

def excelToMultiIndex(xlfile, sheet=0, header=1):
    df = xlfile.parse(sheet)
    tmpfile = tmpDir + "tmp.csv"
    df.to_csv(tmpfile, encoding="utf-8", index=False) #sending it to CSV and resurecting to DF is a hack, but it works
    df = pd.read_csv(tmpfile, encoding="utf-8", header=header)
    df = df.rename(columns=lambda x: fixCountryName(x))
    return df

def getDataSet(multiIndex, setName, config, index=["Description","Unit","Source","Note"]):
    data = multiIndex[setName]
    data = cleanWhitespace(data)
    meta = data[0:len(index)]
    data = data[len(index):]
    data = data.dropna(how="all")
    data = fixContentTypes(data)
    meta.index = index
    meta = meta.transpose()
    ind = pd.DataFrame([dict(Description=config["description"])], index=["Indicator"])
    con = pd.DataFrame([dict(Description=setName)], index=["Set Name"])
    meta = ind.append(con).append(meta)
    return (data, meta)

def getTimeseriesDataSet(multiIndex, setName, config, index=["Description","Unit","Source","Note"]):
    (data,meta) = getDataSet(multiIndex, setName, config, index=["Description","Unit","Source","Note"])
    data["Year"] = multiIndex["Year"]
    data["Month"] = multiIndex["Month"]
    cols = data.columns.tolist()
    cols = cols[-2:] + cols[:-2]
    data = data[cols]
    data = data.rename(columns=lambda x: replaceUnnamed(setName, x))
    monthly = data.dropna(subset=["Month"]).dropna(how="all", subset=data.columns[2:]).drop("Year",1)
    yearly  = data.dropna(subset=["Year"]).dropna(how="all", subset=data.columns[2:]).drop("Month",1)
    return (monthly, yearly, meta)

def getTopCols(df, filtr=["Year","Month"]):
    li = df.columns.tolist()
    out = set()
    for c in li:
        if c[0] in filtr:
            continue
        out.add(c[0])
    return out

def replaceUnnamed(name, x):
    if x.startswith("Unnamed"):
        return name
    return x

def fixCountryName(country):
    country = country.strip()
    if country == "Antigua & Barbuda":
        country = "Antigua and Barbuda"
    if country == "The Bahamas":
        country = "Bahamas"
    return country

def fixContentTypes(df):
    for colname in list(df.columns):
        try:
            df[colname] = df[colname].astype(int)
        except:
            try:
                df[colname] = df[colname].astype(float)
            except:
                pass
    return df

def cleanWhitespace(df):
    df = df.rename(columns=lambda x: x.strip())
    for col in df.columns:
        try:
            df[col] = df[col].map(str.strip)
        except:
            pass
    return df

#utility functions

chatter = False
def elog(s):
    if chatter:
        print(s)

def formatComputerReadableString(strn):
    return(strn.strip().lower().replace(" ","-"))

def saveAsCSV(df, path, name, prefix, suffix="",index=False, float_format='%.2f'):
    filename = path + prefix + "_" + name
    if suffix:
        filename = filename + "_" + suffix
    filename = filename + ".csv"
    df.to_csv(filename, encoding="utf-8", index=index, float_format=float_format)

# <codecell>

def writeGen1XLS(data, meta, gen1Path, setName, prefix, suffix=""):
    if suffix:
        suffix = "_" + suffix
    xlsPath = gen1Path + prefix + "_" + setName + suffix +".xls"
    writer = pd.ExcelWriter(xlsPath)
    data.to_excel(writer, "data", index=False)
    meta.to_excel(writer, "metadata", index=True)
    writer.save()

def writeGen2CSV(data, meta, gen2Path, setName, prefix, suffix=""):
    data = data.rename(columns=lambda x: formatComputerReadableString(x))
    saveAsCSV(data, gen2Path, setName, prefix, suffix)
    meta["Field"] = meta.index.map(formatComputerReadableString)
    meta["English"] = meta.index
    cols = meta.columns.tolist()
    cols = cols[-2:] + cols[:-2]
    meta = meta[cols]
    meta = meta.rename(columns=lambda x: formatComputerReadableString(x))
    sufx = "meta"
    if suffix:
        sufx = suffix + "_meta"
    saveAsCSV(meta, gen2Path, setName, prefix, sufx)    
        
def processMultiCountryFile(config):
    elog(config)
    xlFile = getXLFile(config)
    multiIndex = excelToMultiIndex(xlFile, header=[1,2])
    cols = getTopCols(multiIndex)
    gen1Path = gen_1_dir + config["path"] + "/"
    gen2Path = gen_2_dir + config["path"] + "/"
    prefix = formatComputerReadableString(config["descriptor"])
    countryMap = {}
    for country in cols:
        lcountry = formatComputerReadableString(country)
        elog(country)
        if config["timeseries"]:
            (monthly, yearly, meta) = getTimeseriesDataSet(multiIndex, country, config)
            countryMap[lcountry] = (monthly, yearly, meta)
            if len(yearly.index):
                writeGen1XLS(yearly, meta, gen1Path, lcountry, prefix, "annual")
                writeGen2CSV(yearly, meta, gen2Path, lcountry, prefix, "annual")
            if len(monthly.index):
                writeGen1XLS(monthly, meta, gen1Path, lcountry, prefix, "monthly")
                writeGen2CSV(monthly, meta, gen2Path, lcountry, prefix, "monthly")                
        else:
            (data, meta) = getDataSet(multiIndex, country, config)
            countryMap[lcountry] = (data, meta)
            writeGen1XLS(data, meta, gen1Path, lcountry, prefix)
            writeGen2CSV(data, meta, gen2Path, lcountry, prefix)
    return countryMap

chatter = False
urlroot = "/sids-rcm-public/html/"
bigMap = {}
print("<ul>")
for config in water:
    countryMap = processMultiCountryFile(config)
    bigMap[config['descriptor']] = countryMap
    numCountries = "1 country"
    if len(countryMap) > 1:
        numCountries = "%i countries" % len(countryMap)
    print("<li><a href='%s%s'>%s</a><br>Data from %s</li>" % (urlroot, config["descriptor"], config["description"], numCountries))
print("</ul>")
#chatter = True
#for config in energy:
#    processMultiCountryFile(config)    

# <codecell>

config = {
    "description":"Number of vehicles",
    "descriptor":"number-of-vehicles",
    "fileName":"Energy_6a_NumVehicles.xlsx",
    "generation":"0",
    "path":"rcm/energy/",
    "timeseries":True
}
xlfile = getXLFile(config)
#multiIndex = excelToMultiIndex(xlfile, header=[1,2])
#multiIndex
df = xlfile.parse(0)
tmpfile = tmpDir + "tmp.csv"
df.to_csv(tmpfile, encoding="utf-8", index=False) #sending it to CSV and resurecting to DF is a hack, but it works
df = pd.read_csv(tmpfile, encoding="utf-8", header=[1,2])
df = df.rename(columns=lambda x: fixCountryName(x))
df

# <codecell>

setName = "Antigua and Barbuda"
multiIndex.columns
(monthly,yearly,meta) = getTimeseriesDataSet(multiIndex, setName, config)

# <codecell>

foo = {"a":"b","c":"d"}
len(foo)

# <codecell>

plot1 = graphData(wdate,'5a. National water demand','Trinidad and Tobago')

# <codecell>

plot2 = graphData(wdate,'4b. Water production','Trinidad & Tobago')

# <codecell>


ind1 = '5a. National water demand'
ind2 = '4b. Water production'

country = 'Trinidad and Tobago'

def getData(dframe, indicator, country):
    worksheet = dframe.parse(indicator, header=2)
    worksheet = worksheet[['Year',country]]
    worksheet = worksheet[pd.notnull(worksheet['Year'])]
    worksheet['Year'] = worksheet['Year'].astype(int)
    return worksheet

def plotIndicators(dframe, ind1, ind2, country):
    w1 = getData(dframe,ind1,country)
    w2 = getData(dframe,ind2,country)
    combined = pd.merge(w1,w2,on="Year")
    combined.columns = ['Year',ind1, ind2]
    combined.plot(x="Year", title=country, kind="line")

plotIndicators(wdate, ind1, ind2, country)    

df = getData(wdate, ind1, country) 
df.to_csv("c:/Users/rwilliams/Documents/portal/ttwater.csv", index=False, float_format='%.3f')

# <codecell>


# <codecell>


def getTopCols(df):
    li = df.columns.tolist()
    out = set()
    for c in li:
        out.add(c[0])
    return out

def tweakColumnName(country, x):
    if x.startswith("Unnamed"):
        return country
    return x

def getCountryTimeseriesData(f,country, yearSeries, monthSeries):
    if not country in getTopCols(f):
        return (None, None)
    df = f[country][5:]
    df["Year"] = yearSeries
    df["Month"] = monthSeries
    cols = df.columns.tolist()
    cols = cols[-2:] + cols[:-2]
    df = df[cols]
    df = df.rename(columns=lambda x: x.strip())
    df = df.rename(columns=lambda x: tweakColumnName(country, x))
    monthly = df.dropna(subset=["Month"]).dropna(how="all", subset=df.columns[2:]).drop("Year",1)
    yearly  = df.dropna(subset=["Year"]).dropna(how="all", subset=df.columns[2:]).drop("Month",1)
    return (monthly, yearly)

# <codecell>

sroot = "C:/Users/rwilliams/Documents/portal/data/rcm/water/"
def saveAsCSV(df, country, prefix, suffix=""):
    c = country.strip().lower().replace(" ","-")
    filename = sroot + prefix + "_" + c
    if suffix:
        filename = filename + "_" + suffix
    filename = filename + ".csv"
    df.to_csv(filename, encoding="utf-8", index=False)



# <codecell>

c = open (proot + "Countries.txt","r")
for co in c.readlines():
    country = co.strip()
    (mdf, ydf) = getCountryTimeseriesData(f,country,yearSeries, monthSeries)
    if isinstance(ydf,pd.DataFrame) and len(ydf.index):
        saveAsCSV(ydf, country, "rainfall","annual")
    if isinstance(mdf,pd.DataFrame) and len(mdf.index):
        saveAsCSV(mdf, country, "rainfall","monthly")

# <codecell>

import matplotlib.pyplot as plt

country = "Antigua and Barbuda"
(df,yf) = getCountryTimeseriesData(f,country,yearSeries, monthSeries)
df = df.convert_objects(convert_numeric='force')
df.plot(x="Month")

# <codecell>

def writeGen3HTMLTable(data, meta, gen3Path, setName, prefix, suffix=""):
    header = meta["Description"]["Set Name"] + ": " + meta["Description"]["Indicator"]
    html = "<div style='overflow:auto' class='dataTableSection'><h2>" + header + "</h2>"
    html = html + "<table style='border:1px solid #ccc;'><tr>"
    for col in data.columns:
        html = html + "<th>" + col + "</th>"
    html = html + "</tr>"
    for row in data.index:
        html = html + "<tr>"
        for col in data.columns:
            strn = str(data[col][row])
            if "Year" == col:
                strn = strn[0:4]
            if "Month" == col:
                strn = strn[0:7]
            html = html + "<td style='border:1px solid #ccc; text-align:right; padding-left:10px; padding-right:10px;'>" + strn + "</td>"
        html = html + "</tr>"
    html = html + "</table></div>"
    if suffix:
        suffix = "_" + suffix
    file = open(gen3Path + prefix + "_" + setName + suffix + ".html", 'w')
    file.write(html)
    file.close()
    return html

for config in water:
    desc = config["descriptor"]
    dataSet = bigMap[desc]
    countries = sorted(dataSet.keys())
    gen3Path = gen_3_dir + config["path"] + "/"
    html = ""
    for c in countries:
        data = dataSet[c]
        if len(data) == 2:
            (data,meta) = data
            html = html + writeGen3HTMLTable(data, meta, gen3Path, c, desc, "annual")
        elif len(data) == 3:
            (monthly, yearly, meta) = data
            if len(yearly) > 0:
                html = html + writeGen3HTMLTable(yearly, meta, gen3Path, c, desc, "annual")
            if len(monthly) > 0:
                html = html + writeGen3HTMLTable(monthly, meta, gen3Path, c, desc, "monthly")
        file = open(gen3Path + desc + "_all.html", 'w')
        file.write(html)
        file.close()

# <codecell>

f = sorted(list(bigMap.keys()))
f

# <codecell>


