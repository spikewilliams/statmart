# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>

# <headingcell level=1>

# Generation 4 graph builder library

# <codecell>

import json
import pymysql
import pandas.io.sql as psql
import unittest

from settings_statmart import *
import utils_statmart as us
import gen4_html as html
import gen4_d3js_parts as d3

import imp
imp.reload(d3)

# <codecell>

def build_file_name(config):
    return "%s_%s.php" % (config["prefix"], config["suffix"]);

# <codecell>

def get_all_series_json(config):
    df = ""
    with statmart_utils.get_db_connection() as cursor:
        query = """
                SELECT identifier, description
                FROM series as S 
                WHERE S.identifier like '%s%s%s'
                """ % (config("prefix"), "\_%\_", config("suffix"))
        df = psql.frame_query(query, con=cursor.connection)
    return json.dumps(df.as_matrix().tolist(),indent=4)

# <codecell>

def build_d3_head(title, include_path="../../inc/",style_include="style_basic.php"):
    meta = html.meta([("http-equiv", "content-type"), ("content","text/html; charset=UTF-8")])
    titl = html.title(title)
    scrp = html.script_ext(statmart_d3_path)
    styl = html.style(html.php_include(include_path + style_include))
    head = ("\n").join([meta,titl,scrp,styl])
    return html.head(head)

# <codecell>

def build_d3_line_graph(config):
    script = []
    script.append(d3.metadata_iso3_map % (config["iso3_map"]))   
    script.append(d3.metadata_series_info_map % (config["series_info_map"]))   
    
    if "currency_year" in config:
        script.append(util_currency_converter_2005)
    
    if config["series_source"] == "params":
        script.append(d3.util_function_get_parameters_by_name)
        if config["series_param"] == "iso3":
            script.append(d3.js_series_name_from_iso3_parameter % (config["prefix"],config["suffix"]))
        elif config["series_param"] == "s":
            script.append(d3.js_series_name_from_s_parameter)
    
    if config["data_source"] == "local":
        script.append(d3.js_dataset_list % get_all_series_json(config))
    elif config["data_source"] == "query":
        script.append(d3.js_data_url_series_query)
    
    script.append(d3.graph_set_title % (config["title"])) 
    if config["subtitle"] == "countryname":   
        script.append(d3.graph_set_subtitle_country)
    else:
        script.append(d3.graph_set_subtitle % (config["subtitle"])) 
        
    script.append(d3.graph_default_size)
    script.append(d3.graph_title_location)
    script.append(d3.graph_default_header)
    
    script.append(d3.include_js_d3_basic_axis)
    script.append(d3.js_d3_start_csv)
    
    if config["unit"] == "guess":
        script.append(d3.js_unit_guess)
    else:
        script.append(d3.js_unit_set % (config["unit"], str(config["multiplier"])))
    
    script.append(d3.js_d3_process_annual_csv_data)
    script.append(d3.js_d3_build_simple_xy_domains)
    script.append(d3.js_d3_svg_build_x_axis)
    
    if config["y_axis_label"] == "unit":
        script.append(d3.js_d3_svg_build_y_axis_unit_label)
    else:
        script.append(d3.js_d3_svg_build_y_axis_label % config["y_axis_label"])
        
    script.append(d3.js_d3_svg_draw_line)
    script.append(d3.svg_draw_title)
    script.append(d3.svg_draw_subtitle)
    script.append(d3.svg_draw_source)
    script.append(d3.js_d3_end_csv)
    
    head = build_d3_head(config["indicator"])
    body = html.body(html.script("\n".join(script)))
    page = html.html(head + "\n" + body)
    page_name = build_file_name(config)
    us.mkdirs(config["gen_4_dir"])
    page_file = open(config["gen_4_dir"] + page_name, "w", encoding="utf8")
    page_file.write(page)
    page_file.close()    
    return page

# <codecell>

def get_iso3_map_json(config):
    df = ""
    with us.get_db_connection() as cursor:
        query = """
                SELECT L.iso3, L.countryname, O.series, COUNT(O.dateid) as numberyears
                FROM observation as O
                INNER JOIN location as L ON O.locationid = L.id
                WHERE O.series like '%s\_%s\_%s'
                GROUP BY L.iso3
                """ % (config["prefix"], "%", config["suffix"])
        df = psql.frame_query(query, con=cursor.connection)
        df = df.set_index("iso3")
    return df.to_json(orient="index")

# <codecell>

def get_series_info_map_json(config):
    df = ""
    with us.get_db_connection() as cursor:
        query = """
                SELECT identifier, originalsource, proximatesource
                FROM series
                WHERE series.identifier like '%s\_%s\_%s'
                """ % (config["prefix"], "%", config["suffix"])
        df = psql.frame_query(query, con=cursor.connection)
        df = df.set_index("identifier")
    return df.to_json(orient="index")

# <codecell>

def build_gen4_config(config, 
                      title="indicator", 
                      subtitle="countryname",
                      y_axis_label="unit",
                      data_source="query", 
                      series_source="params", 
                      series_param="iso3",
                      unit="guess"):
    config["iso3_map"] = get_iso3_map_json(config)
    config["series_info_map"] = get_series_info_map_json(config)
    config["title"] = title
    if title == "indicator":
        config["title"] = config["indicator"]
    config["subtitle"] = subtitle
    config["y_axis_label"] = y_axis_label
    config["data_source"] = data_source
    config["series_source"] = series_source
    config["series_param"] = series_param
    config["unit"] = unit
    return config

# <codecell>


