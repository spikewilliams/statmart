# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>

# <codecell>

import os
import pandas as pd

import statmart_util as smu

from statmart_config import *

gen1Dir = statmart_facts_gen1 + "cepalstat/"
gen2Dir = statmart_facts_gen2 + "cepalstat/gdp-sec/"

prefix = "gdp-sec"
suffix = "cepalstat"
indicator = "2216"

# <markdowncell>

# We have two csv files pulled down from CEPALStat by an outside script. Lets take a look at what is in these files. First, the data file:

# <codecell>

statfile = gen1Dir + indicator + "_all.csv"
df = pd.read_csv(statfile, encoding="utf-8", index_col=["Item"])
df = df.transpose()
sample = df["Construction"].transpose()
sample[11:20]

# <markdowncell>

# And here is the metadata:

# <codecell>

metafile = gen1Dir + indicator + "_meta.csv"
mf = pd.read_csv(metafile, encoding="utf-8")
mf

# <markdowncell>

# We need a list of sectors so we can build a map out of them. __Should any sectors be added to the data in the future, the additional fields will need to be added in the sectorMap, below.__ If the additional sector fields are not added, an error will occur during the file generation step, when the sector name is not found in sectorMap.

# <codecell>

sectors = smu.get_index_set(df.transpose())
sectors

# <markdowncell>

# Here is the sectorMap, which maps every long name of a sector (see set listing above) to a short one for use in the file system. We also ensure that a directory exists to corresponding to each sector in the map.

# <codecell>

sectorMap = {'Agriculture, hunting and forestry':'aghufo',
 'Agriculture, hunting, forestry and fishing':'aghufofi',
 'Construction':'cstrn',
 'Electricity, gas and water supply':'egws',
 'Financial intermediation services indirectly measured (FISIM)':'fisim',
 'Financial intermediation, real estate, renting and business activities':'firerba',
 'Fishing':'fish',
 'Gross domestic product (GDP)':'gdp',
 'Hotels and restaurants':'hr',
 'Manufacturing':'mfg',
 'Mining and quarrying':'mq',
 'Post and telecommunications':'pt',
 'Public administration, defence, compulsory social security, education, ' +
     'health and social work, and other community, social and personal service activities': 'public',
 'Statistical discrepancy of GDP by economic activity': 'discrep',
 'Taxes on products less subsidies on products': 'taxes',
 'Total value added': 'tva',
 'Transport and supporting and auxiliary activities': 'tsaa',
 'Transport, storage and communications': 'tsc',
 'Wholesale and retail trade, and repair of goods': 'wrtrg',
 'Wholesale and retail trade, repair of goods, and hotels and restaurants': 'wrtrghr'}

for val in sectorMap.values(): # ensure there is a directory for each of the above sets
    directory = gen2Dir + val + "/"
    if not os.path.exists(directory):
        os.makedirs(directory)

# <markdowncell>

# And here we build a csv file containing a yearly series of values for each country/sector combination. We create a metadata file for each one as well.

# <codecell>

filelist = []
for sector in sectors:
    qf = df[sector].transpose().set_index(["ISO3"])
  
    for iso3 in smu.get_index_set(qf):
        directory = gen2Dir + sectorMap[sector] + "/"
        idf = qf.ix[iso3]
        idf = idf[["Year","Value","Source","Notes"]]
        idf.columns = ["year","value","source","notes"]
        idf["value"] = idf["value"].apply(lambda x : int(1000000 * x)).astype(object) # convert to dollars from millions of dollars
        idf["source"] = idf["source"].apply(lambda x : "CEPALStat: " + str(x))
        idf["notes"] = idf["notes"].apply(lambda x : "CEPALStat: " + str(x))
        filestem = prefix + "-" + sectorMap[sector] + "_" + iso3.lower() + "_" + suffix
        filename = filestem + ".csv"
        filepath = directory + filename
        idf.to_csv(filepath, encoding="utf8", index=False)
        
        country = smu.get_country_by_iso3(iso3)
        meta = [("name", "%s - Annual Gross Domestic Product (GDP) by activity: %s [CEPALStat]" % (country, sector)),
                ("dataset", "CEPALStat national accounts [2216]"),
                ("description", ("Annual national account statistics for %s: %s") % (country, sector)),
                ("file", filename),
                ("filehash", smu.githash(filepath)),
                ("category", "Economy"),
                ("type", "GDP"),
                ("columns", "year,value,source,notes")]
        
        metafile = directory + filestem + "_meta.csv"    
        pd.DataFrame(meta,columns = ["key","value"]).to_csv(metafile, encoding="utf8", index=False)
        filelist.append([sectorMap[sector] + "/" + filestem])
        
pd.DataFrame(filelist).to_csv(gen2Dir + "_" + prefix + ".csv", encoding="utf8", index=False, header=False)
print("%i series saved to %s" % (len(filelist), gen2Dir))

# <codecell>


# <codecell>


