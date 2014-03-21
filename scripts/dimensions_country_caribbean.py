# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>

# <markdowncell>

# The following creates a csv file containing a list of identification parameters for Caribbean countries, and can be used as an example of how to create a file containing information on a subset of countries. The csv file created here is not uploaded to the database, but is instead used as a utility file by other data building scripts. The newly generated csv file is called "\_country_caribbean.csv" - prepended with an underscore to indicate that it is not to be uploaded to the database.

# <codecell>

import pandas as pd

from settings_statmart import *

gen_1_dir = statmart_dimensions_gen1 + "cepalstat/"
gen_2_dir = statmart_dimensions_gen2 + "cepalstat/"
gen_2_dir_base = statmart_dimensions_gen2 + "base/"

# <markdowncell>

# The new csv file is created using the countries\_base.csv file, combined with a csv file containing ISO 3166 values for each of the countries to be included. This file also contains a "cepalid" for each country, which is used for reference in the CepalStat web service. There are other fields in this file, but "iso2" and "cepalid" are the only ones we will be using.

# <codecell>

country_base = gen_2_dir_base + "country_base.csv"
eclac_countries = gen_1_dir + "eclac_carib_countries.csv"
cb = pd.read_csv(country_base, encoding="utf-8", dtype={'isonum': object})[["iso2","iso3","isonum","name"]]
ec = pd.read_csv(eclac_countries, encoding="utf-8")[["iso2","cepalid"]]
carib = pd.merge(cb,ec,on="iso2")
carib.to_csv(gen_2_dir + "_country_caribbean.csv", encoding = "utf-8", float_format='%.6f', index=False)

# <markdowncell>

# And here is what the data in the resulting csv file looks like:

# <codecell>

carib

# <codecell>


