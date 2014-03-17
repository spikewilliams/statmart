# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>

# <headingcell level=1>

# Build script for CEPALStat indicator #347: Tuburculosis death rate

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

prefix = "tb-death-rate"
suffix = "cepalstat"
indicator_id = "357"
indicator_name = "Death rate associated with tuberculosis"
indicator_category = "Social"
indicator_type = "Health"

config = us.build_config(suffix,prefix,indicator_id,indicator_name,indicator_category,indicator_type)
#config["source"] = "Economic Commission for Latin America and the Caribbean"
#config["multiplier"] = 1000000
config["multiplier"] = 0.01

config

# <markdowncell>

# Generation 1 - Downloads XML through the CEPALStat web service and dumps the enclosed data to a csv file.

# <codecell>

gen1_cepalstat.download(config)

# <markdowncell>

# Generation 2 - Refines the rough csv data from Generation 1 into a standardized csv format common to all data sets. Prepares this data for importing to the database.

# <codecell>

gen2_cepalstat.build(config)
data_list = gen3_utils.get_gen2_data(config)
us.log(data_list[0:3]) # have a look at a sample of the data

# <markdowncell>

# Generation 3 - Load the Generation 2 data into the database.

# <codecell>

gen3_utils.standard_load_from_data_list(data_list)

# <markdowncell>

# Generation 4 - Build a php file that uses javascript to generate SVGs using the data in the database

# <codecell>

import imp
imp.reload(gen4_utils)
config = gen4_utils.build_gen4_config(config)
page = gen4_utils.build_d3_line_graph(config)

# <codecell>


