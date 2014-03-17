# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>

# <codecell>

import json
import pymysql
import pandas.io.sql as psql
import unittest

from s0000_statmart_settings import *
import s0001_statmart_utils as statmart_utils
from s4002_html_tools import *
from s4004_js_parts import *

# <codecell>

gen_4_dir = statmart_view_gen4 + "cepalstat/"

prefix = "unemployment"
suffix = "cepalstat"

page_name = "%s_%s.php" % (prefix, suffix);

page_title = "Unemployment data from the United Nations Economic Commission for Latin America and the Caribbean (ECLAC)"
graph_title = "Official unemployment rate"
y_axis_title = "Official unemployment rate"

# <codecell>

df = ""
with statmart_utils.get_db_connection() as cursor:
    query = """
            SELECT identifier, description
            FROM series as S 
            WHERE S.identifier like '%s%s%s'
            """ % (prefix, "\_%\_", suffix)
    df = psql.frame_query(query, con=cursor.connection)
df

# <codecell>


# <codecell>

dataset_list = json.dumps(df.as_matrix().tolist(),indent=4)

# <codecell>

scrpt = ("\n").join([
    js_dataset_list % json.dumps(df.as_matrix().tolist(),indent=4),                 
    util_function_get_parameters_by_name,
    util_currency_converter_2005,
    js_series_name_from_s_parameter,
    js_data_url_series_query,
    include_js_d3_basic_axis,
    js_unit_set % ("percentage", "1"),
    js_d3_start_csv,
        js_d3_process_annual_csv_data,
        js_d3_build_simple_xy_domains,  
        js_d3_svg_build_x_axis,
        js_d3_svg_build_y_axis_unit_label,
        js_d3_svg_draw_area,
    js_d3_end_csv
    ])
    
bdy = script(scrpt)
page = html(head + body(bdy))

# <codecell>

page_file = open(gen_4_dir + pageName, "w", encoding="utf8")
page_file.write(page)
page_file.close()

# <codecell>

import imp
imp.reload(s4004_js_parts)

# <codecell>


