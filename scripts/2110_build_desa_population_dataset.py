# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>

# <codecell>

import pandas as pd

import statmart_util as smu

from statmart_config import *

gen1Dir = statmart_facts_gen1 + "desa/"
gen2Dir = statmart_facts_gen2 + "desa/"

prefix = "pop"
suffix = "desa"

# <markdowncell>

# The xls source file for the population data is from the [2012 revision of the World Population Prospects](http://esa.un.org/unpd/wpp/index.htm) from the Population Division of the UN Department of Economic and Social Affairs. This covers estimates from 1950-2010. There are many other available views of various aspects of this data available at that site

# <codecell>

fileName = "WPP2012_POP.xls"
popfile = gen1Dir + fileName
xlfile = pd.ExcelFile(popfile)

# <markdowncell>

# The source file has several different estimates available. We are just using the base scenario ('ESTIMATES'), plus the 'NOTES' sheet.

# <codecell>

xlfile.sheet_names

# <markdowncell>

# Create the DataFrame with all population information. The "Country code" column contains the ISO 3166 numeric value, but as an integer, rather than as 3-numeral string padded by zeros. So we fix this to be in line with the ISO spec, and, hence, with our data. We also rename the Country code field to match the name in our schema.

# <codecell>

The source file has several different estimates available. We are just using the base scenario ('ESTIMATES'), plus the 'NOTES' sheet.
df = xlfile.parse("ESTIMATES", skiprows=range(0,15), header=16)
df["Country code"] = df["Country code"].apply(lambda x: "%03i" % int(x))
df = df.rename(columns={"Country code":"isonum"})
We will filter in only Caribbean countries, using the list of isonum values in _country_caribbean.csv...
carib_country_path = statmart_dimensions_gen2 + "cepalstat/_country_caribbean.csv"
carib = pd.read_csv(carib_country_path, encoding="utf-8", usecols=["isonum","iso3","name"], dtype={'isonum': object})
df = pd.merge(carib,df, on="isonum")
df[0:4]

# <markdowncell>

# We will filter in only Caribbean countries, using the list of _isonum_ values in \_country\_caribbean.csv...

# <codecell>

carib_country_path = statmart_dimensions_gen2 + "cepalstat/_country_caribbean.csv"
carib = pd.read_csv(carib_country_path, encoding="utf-8", usecols=["isonum","iso3","name"], dtype={'isonum': object})
df = pd.merge(carib,df, on="isonum")
df[0:4]

# <markdowncell>

# The unit in this data is "thousands." We do the math so that the full number can go in our database. A flag is used to ensure that a DataFrame object get this multiplication only once, just in case this code gets run multiple times. 

# <codecell>

if not hasattr(df,"multipliedFlag"):
    for col in df.columns[7:]:
        df[col] = df[col].apply(lambda x : x * 1000).astype(int)
else:
    print("WARNING: you must reinitialize the DataFrame before running this code a second time.")
df.multipliedFlag = True
df[0:4]

# <markdowncell>

# Next, parse out the notes from the notes sheet. These are a bunch of values in rows, looking like "(22) Refers to Bonaire, Saba and Sint Eustatius."  We need to map the value in parens to something that can be related to the "Notes" field of the main dataframe. Again, use a flag to ensure that notes are run twice against the same DataFrame.

# <codecell>

if not hasattr(df,"notesFlag"):
    noteMap = {}
    notes = xlfile.parse("NOTES").transpose()
    for col in notes.columns:
        (noteid, note) = notes[col][0].split(") ",1)
        noteid = noteid[1:]
        noteMap[noteid] = note
    df["Notes"] = df["Notes"].dropna().apply(lambda x: noteMap[str(x)])
else:
    print("WARNING: you must reinitialize the DataFrame before running this code a second time.")        
df.notesFlag = True
df[10:14]

# <markdowncell>

# Save each list of population estimates into a csv file called pop\__iso3_\_desa.csv, where iso3 is the 3-letter country code, converted to lower case. Save the metadata in a file called pop\__iso3_\_desa\_meta.csv.

# <codecell>

filelist = []
tf = df.transpose()
mf = ""
for col in tf.columns:
    line = tf[col]
    filestem = prefix + "_" + line.ix["iso3"].lower() + "_" + suffix
    filename = filestem + ".csv"
    filepath = gen2Dir + filename
    line[7:].to_csv(filepath, encoding="utf8", index=True, header=["value"], index_label="year")
    
    meta = [("name", "%s - Population estimates (1950-2010) [UN DESA]" % (line.ix["name"])),
                ("dataset", "UN DESA world population estimates"),
                ("description", ("Population estimates for %s from the 2012 Revision of the World Population Prospects, produced by the " + \
                    "Population Division of the United Nations Department of Economic and Social Affairs") % (line.ix["name"])),
                ("file", filename),
                ("filehash", smu.githash(filepath)),
                ("category", "Demographics"),
                ("type", "Population"),
                ("columns", "year,value")]
    
    mf = pd.DataFrame(meta,columns = ["key","value"])
    metafile = gen2Dir + filestem + "_meta.csv"
    mf.to_csv(metafile, encoding="utf8", index=False)
    filelist.append(filestem)
    
pd.DataFrame(filelist).to_csv(gen2Dir + "_" + prefix + ".csv", encoding="utf8", index=False, header=False)
print("%i series saved to %s" % (len(filelist), gen2Dir))

# <markdowncell>

# Sample metadata file:

# <codecell>

mf

# <codecell>


