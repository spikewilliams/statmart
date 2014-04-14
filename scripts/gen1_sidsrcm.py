# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>

# <codecell>

import pandas as pd

from settings_statmart import *
import utils_statmart as us

# <codecell>

us.verbose = True
gen_0_dir = statmart_facts_gen0 + "sidsrcm/"
gen_1_dir = statmart_facts_gen1 + "sidsrcm/"
tmpDir = "C:/tmp/"

# <codecell>

def getXLFile(config):
    filePath = gen_0_dir + "/" + config["path"] + "/" + config["fileName"]
    xlFile = pd.ExcelFile(filePath)
    return xlFile

def excelToMultiIndex(xlfile, sheet=0, header=1):
    df = xlfile.parse(sheet)
    df = cleanWhitespace(df)
    tmpfile = tmpDir + "tmp.csv"
    df.to_csv(tmpfile, encoding="utf-8", index=False) #sending it to CSV and resurecting to DF is a hack, but it works
    df = pd.read_csv(tmpfile, encoding="utf-8", header=header,na_values=" ")
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

def saveAsCSV(df, path, name, prefix, suffix="",index=False, float_format='%.2f'):
    filename = path + prefix + "_" + name
    if suffix:
        filename = filename + "_" + suffix
    filename = filename + ".csv"
    df.to_csv(filename, encoding="utf-8", index=index, float_format=float_format)

def est_month(d):
    if d == 0:
        return ""
    else:
        return "Estimated, based on %i months of data" % (12 - d)
    
def build_annual_from_monthly(mdf, country):
    mdf.index = mdf["Month"]
    mdfmo = mdf.index.to_datetime()
    print (mdfmo)
    mdf.index = mdfmo.to_period(freq='M')
    ts = mdf[country].astype(float)
    every_month = pd.period_range(mdfmo[0], mdfmo[-1], freq='M') 
    df = pd.DataFrame(index=every_month)
    df[country] = ts
    df["Notes"] = pd.isnull(df[country], )
    df[country] = df[country].interpolate()
    df = df.resample('A', how='sum')
    df["Notes"] = df["Notes"].map(est_month)
    df["Year"] = df.index
    
    cols = df.columns.tolist()
    cols = cols[-1:] + cols[:-1]
    df = df[cols]
    return df
    

# <codecell>

def writeGen1XLS(data, meta, gen1Path, setName, prefix, suffix=""):
    if suffix:
        suffix = "_" + suffix
    xlsPath = gen1Path + prefix + "_" + setName + suffix +".xls"
    writer = pd.ExcelWriter(xlsPath)
    data.to_excel(writer, "data", index=False)
    meta.to_excel(writer, "metadata", index=True)
    writer.save()
        
def processMultiCountryFile(config):
    us.log(config)
    xlFile = getXLFile(config)
    multiIndex = excelToMultiIndex(xlFile, header=[1,2])
    cols = getTopCols(multiIndex)
    gen1Path = gen_1_dir + config["path"]
    us.mkdirs(gen1Path)
    prefix = us.format_lower_no_spaces(config["descriptor"])
    countryMap = {}
    for country in cols:
        lcountry = us.format_lower_no_spaces(country)
        us.log(country)
        if config["timeseries"]:
            try:
                (monthly, yearly, meta) = getTimeseriesDataSet(multiIndex, country, config)
                if len(monthly.index) and len(yearly.index) == 0:
                    yearly = build_annual_from_monthly(monthly, country)
                    
                countryMap[lcountry] = (monthly, yearly, meta)
                if len(yearly.index):
                    writeGen1XLS(yearly, meta, gen1Path, lcountry, prefix, "annual")
                if len(monthly.index):
                    writeGen1XLS(monthly, meta, gen1Path, lcountry, prefix, "monthly")
            except ValueError:
                print("********************** Unable to convert data for " + country)
                continue
        else:
            (data, meta) = getDataSet(multiIndex, country, config)
            countryMap[lcountry] = (data, meta)
            writeGen1XLS(data, meta, gen1Path, lcountry, prefix)
    return countryMap



# <codecell>

def process_gen0_xls(config):
    countryMap = processMultiCountryFile(config)
    numCountries = "1 country"
    if len(countryMap) > 1:
        numCountries = "%i countries" % len(countryMap)
    print("Data from %s" % (numCountries))

# <codecell>


