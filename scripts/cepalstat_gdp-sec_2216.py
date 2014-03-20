# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>

# <headingcell level=1>

# Build script for CEPALStat indicator #2216: Sectoral GDP

# <codecell>

import os, imp
import pandas as pd

from settings_statmart import *
import utils_statmart as us

import gen1_cepalstat
import gen2_cepalstat
import gen3_utils
import gen4_utils

us.verbose = True

# <markdowncell>

# Customize the below per this specfic dataset....

# <codecell>

prefix = "gdp-sec"
suffix = "cepalstat"
indicator_id = "2216"
indicator_name = "Gross Domestic Product"
indicator_category = "Economic"
indicator_type = "GDP"

config = us.build_config(suffix,prefix,indicator_id,indicator_name,indicator_category,indicator_type)
config["source"] = "Economic Commission for Latin America and the Caribbean"
config["multiplier"] = 1000000
#config["multiplier"] = 0.01

config

# <markdowncell>

# Generation 1 - Downloads XML through the CEPALStat web service and dumps the enclosed data to a csv file.

# <codecell>

gen1_cepalstat.download(config)

# <markdowncell>

# Generation 2 - Refines the rough csv data from Generation 1 into a standardized csv format common to all data sets. Prepares this data for importing to the database.

# <codecell>

statfile = config["gen_1_dir"] + indicator_id + "_all.csv"
df = pd.read_csv(statfile, encoding="utf-8", index_col=["Item"])
df = df.transpose()
sample = df["Construction"].transpose()
sample[11:20]

# <markdowncell>

# We need a list of sectors so we can build a map out of them. __Should any sectors be added to the data in the future, the additional fields will need to be added in the sectorMap, below.__ If the additional sector fields are not added, an error will occur during the file generation step, when the sector name is not found in sector_map.

# <codecell>

sectors = us.get_index_set(df.transpose())
sectors

# <markdowncell>

# Here is the sector_map, which maps every long name of a sector (see set listing above) to a short one for use in the file system. We also ensure that a directory exists to corresponding to each sector in the map.

# <codecell>

sector_map = {'Agriculture, hunting and forestry':'aghufo',
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
                                                                                
for val in sector_map.values(): # ensure there is a directory for each of the above sets
    directory = config['gen_2_dir'] + val + "/"
    if not os.path.exists(directory):
        os.makedirs(directory)

# <codecell>

metafile = config["gen_1_dir"] + config["indicator_id"] + "_meta.csv"
metamap = gen2_cepalstat.parse_meta_file(metafile)
metamap

# <codecell>

metamap.update(config)
metamap["note"] = metamap["6495"]
metamap["unit"] = "USD2005"
del metamap["6432"]
del metamap["6495"]
metamap

# <codecell>

import imp
imp.reload(gen2_cepalstat)
configs = []
for sector in sectors:
    qf = df[sector].transpose().set_index(["ISO3"])
    sconfig = dict(metamap)
    sec = sector_map[sector]
    sconfig["prefix"] = prefix + "--" + sec
    sconfig["indicator"] = sector
    if name != sector:
        sconfig["definition"] = "Sectoral GDP: " + sector
    sconfig["gen_2_dir"] = config["gen_2_dir"] + sec + "/"
    print(sconfig["gen_2_dir"])
    gen2_cepalstat.build_files(qf, sconfig)
    configs.append(sconfig)

# <markdowncell>

# Generation 3 - Load the Generation 2 data into the database.

# <codecell>

for config in configs:
    data_list = gen3_utils.get_gen2_data(config)
    gen3_utils.standard_load_from_data_list(data_list)

# <markdowncell>

# Generation 4 - Build a php file that uses javascript to generate SVGs using the data in the database

# <codecell>

import imp
imp.reload(gen4_utils)
for config in configs:
    config = gen4_utils.build_gen4_config(config, unit="Value in millions of USD (2013 equivalent)")
    page = gen4_utils.build_d3_line_graph(config)

# <codecell>


# <codecell>


