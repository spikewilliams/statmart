# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>

# <codecell>

import json
import pymysql
import pandas.io.sql as psql
import unittest

from s0000_statmart_settings import *
import s0001_statmart_utils as statmart_utils

gen4Dir = statmart_view_gen4 + "cepalstat/"

prefix = "unemployment"
suffix = "cepalstat"

pageName = "%s_%s.php" % (prefix, suffix);

pageTitle = "Unemployment data from the United Nations Economic Commission for Latin America and the Caribbean (ECLAC)"
graphTitle = "Official unemployment rate"
yAxisTitle = "Official unemployment rate"

TEST = unittest.TestCase()

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

head = """
<head>
  <meta http-equiv="content-type" content="text/html; charset=UTF-8">
  <title>%s</title>
  <script type='text/javascript' src='%s'></script>
    <style>
 <?php
		include("%s/inc/style_basic.php");
 ?> 
	</style>
</head>""" % (title, statmart_d3_path, statmart_view_root)

# <codecell>

def tag(tag, html, attributes=[]):
    attribute_str = "";
    space = ""
    for (name, value) in attributes:
        attribute_str = attribute_str + space + name + "='" + value + "'";
        space = " "
    attribute_str = space + attribute_str
    return "<" + tag + attribute_str + ">" + html + "</" + tag + ">"

def html(html, attributes=[]):
    doctype = "<!DOCTYPE html>\n"
    return doctype + tag("html",html, attributes)

def body(html, attributes=[]):
    return tag("body",html, attributes)

def div(html, attributes=[]):
    return tag("div",html, attributes)

def script(js):
    cdata = "//<![CDATA[\n"
    cdataend = "\n//]]>"
    return tag("script", cdata + js + cdataend, [("type","text/javascript")])
    
TEST.assertEqual(body("hello", [("foo","bar"),("woo","war")]),"<body foo='bar' woo='war'>hello</body>")

# <codecell>

include_js_d3_basic_axis = """// include_js_d3_basic_axis 
    <?php
		include("%s/inc/axis.php");
     ?> 
 """ % (statmart_view_root)

# <codecell>

dataset_list = json.dumps(df.as_matrix().tolist(),indent=4)
dataset_list = script("""
    var datasetList = %s;
""" % (dataset_list))

# <codecell>

util_function_get_parameters_by_name = """//~util_function_get_parameters_by_name

function getParameterByName(name) {
    var match = RegExp('[?&]' + name + '=([^&]*)').exec(window.location.search);
    return match && decodeURIComponent(match[1].replace(/\+/g, ' '));
}

"""

util_currency_converter_2005 = """//~util_currency_converter_2005

var currentUSD = 1.15848; //factor for converting 2005 dollars to current (2013)
var cYear = 2013;

function convert2005USDtoCurrent(amount){
    return amount * currentUSD;
}

"""

js_series_name_from_s_parameter = """//~js_series_name_from_s_parameter
    seriesName = getParameterByName("s");
"""

js_series_name_from_iso3_parameter = """//~js_series_name_from_iso3_parameter
    iso3 = getParameterByName("s");
    seriesName = "%s_" + iso3 + "_%s"
"""

js_series_name_from_hardcode = """//~js_series_name_from_hardcode
    seriesName = "%s";
"""

js_series_name_default_value = """//~js_series_name_default_value
if (!seriesName){
	seriesName = "%s";
}
"""

js_data_url_series_query = """//~js_data_url_series_query
    dataURL = "%s/series_query.php?s=" + seriesName;
""" % (statmart_root_url)

js_guess_unit = """//~js_guess_unit
    unit = "";
    ufactor = 1;

    var max = d3.max(data, function(d) { return d["value"]; });
    var min = d3.min(data, function(d) { return d["value"]; });
    
    if (min > 1000 && max > 10000) {
        unit = "thousands"
        ufactor = 1000;
    }
    if (min > 100000 && max > 1000000) {
        ufactor = 1000000;
        unit = "millions"   
    }
    if (min > 100000000 && max > 1000000000) {
        ufactor = 1000000000;
        unit = "billions"   
    }     
    if (min < 1 && max < 1) {
        unit = "percentage";
        ufactor = 0.01;
    }
"""

js_set_unit = """//~js_set_unit (unit type, unit factor)
    unit = "%s";
    ufactor = %s;
"""

js_d3_start_csv = """//~js_d3_start_csv
     d3.csv(dataURL, function(error, data) {
"""

js_d3_filter_data_by_series_name = """//~js_d3_filter_data_by_series_name
        data = data.filter(function(d){return d.series === seriesName});
"""

js_d3_build_simple_xy_domains = """//~js_d3_build_simple_xy_domains
        x.domain(d3.extent(data, function(d) { return d.date; }));
        y.domain([0,d3.max(data, function(d) { return d.value; })]);
"""

js_d3_process_annual_csv_data = """//~js_d3_process_annual_csv_data
        data.forEach(function(d) {
            d.date = parseDate(d.year);
            d.value = (+d["value"] * ufactor);
        });
"""     

js_d3_end_csv = """//~js_d3_end_csv
    });
"""

js_d3_svg_build_x_axis = """//~js_d3_svg_build_x_axis
        svg.append("g")
          .attr("class", "x axis")
          .attr("transform", "translate(0," + height + ")")
          .call(xAxis)
            .selectAll("text")
                  .style("text-anchor", "end")
                  .attr("dx", "-.8em")
                  .attr("dy", "-.25em")
                  .attr("transform", function(d) {
                      return "rotate(-90)"
            });
"""

js_d3_svg_build_y_axis_unit_label = """//~js_d3_svg_build_y_axis_unit_label
        svg.append("g")
          .attr("class", "y axis")
          .call(yAxis)
        .append("text")
          .attr("transform", "rotate(-90)")
          .attr("dy", "-38px")
          .attr("dx", "-120px")
          .style("text-anchor", "middle")
          .style("font-weight", "bold")
          .style("padding-right","10px")
          .text(unit);
"""

js_d3_svg_draw_area = """//~jd_d3_svg_draw_area
           svg.append("path")
              .datum(data)
              .attr("class", "area")
              .attr("d", area);
"""

scrpt = ("\n").join([
    util_function_get_parameters_by_name,
    util_currency_converter_2005,
    js_series_name_from_s_parameter,
    js_data_url_series_query,
    include_js_d3_basic_axis,
    js_set_unit % ("percentage", "1"),
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

pageFile = open(gen4Dir + pageName, "w", encoding="utf8")
pageFile.write(page)
pageFile.close()

# <codecell>


# <codecell>

"%s" % "\_%\_"

# <codecell>


