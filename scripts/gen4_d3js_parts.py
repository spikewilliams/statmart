# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>

# <headingcell level=1>

# Generation 4 library of d3js snippets for graph building

# <markdowncell>

# A collection of code fragments using the [d3js](http://d3js.org/) javascript library. These fragments may be selected and assembled to build a complete script for generation of graphs.

# <codecell>

from settings_statmart import *

# <codecell>

js_dataset_list = """//~include_js_d3_basic_axis
    var datasetList = %s;
"""

include_js_d3_basic_axis = """//~include_js_d3_basic_axis 
    <?php
		include("%sinc/axis.php");
     ?> 
 """ % ("../../")

util_function_get_parameters_by_name = """//~util_function_get_parameters_by_name

function getParameterByName(name, default_param) {
    var match = RegExp('[?&]' + name + '=([^&]*)').exec(window.location.search);
    if (match) {
    	return match && decodeURIComponent(match[1].replace(/\+/g, ' '));
    }
    return default_param;
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
    iso3 = getParameterByName("iso3");
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
    dataURL = "%sseries_query.php?s=" + seriesName;
""" % ("../../")

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
            d.value = (+d["value"] / ufactor);
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

core_js_d3_svg_build_y_axis_label = """
        svg.append("g")
          .attr("class", "y axis")
          .call(yAxis)
        .append("text")
          .attr("transform", "rotate(-90)")
          .attr("dy", "-34px")
          .attr("dx", (height * -1) + "px")
          .style("text-anchor", "start")
          .style("padding-right","10px")
"""

js_d3_svg_build_y_axis_unit_label = """//~js_d3_svg_build_y_axis_unit_label
%s
          .text(unit);
""" % (core_js_d3_svg_build_y_axis_label)

js_d3_svg_build_y_axis_label = """//~js_d3_svg_build_y_axis_unit_label
""" + core_js_d3_svg_build_y_axis_label + """
          .text("%s");
"""
          
js_d3_svg_draw_area = """//~js_d3_svg_draw_area
           svg.append("path")
              .datum(data)
              .attr("class", "area")
              .attr("d", area);
"""


js_d3_svg_draw_line = """//~jd_d3_svg_draw_line
           svg.append("path")
              .datum(data)
              .attr("class", "line")
              .attr("d", line);
"""

# <markdowncell>

# These javascript blocks are used for selecting the "unit" to be displayed in the graph (millions, billions, percentage, etc), along with the "ufactor", which is a number by which each data value will be divided, before graphing. Specify the unit using js_unit_set, if possible. Otherwise, js_unit_guess can be used to have the script examine the data and come up with its best guess for the unit. But the logic for this is currently rather crude, and will, at times, guess poorly.

# <codecell>

js_unit_set = """//~js_set_unit (unit type, unit factor)
    unit = "%s";
    ufactor = %s;
"""

js_unit_guess = """//~js_guess_unit
    unit = "";
    ufactor = 1;

    var max = d3.max(data, function(d) { return d["value"]; });
    var min = d3.min(data, function(d) { return d["value"]; });
    
    if (min > 1000 && max > 10000) {
        unit = "Thousands"
        ufactor = 1000;
    }
    if (min > 100000 && max > 1000000) {
        ufactor = 1000000;
        unit = "Millions"   
    }
    if (min > 100000000 && max > 1000000000) {
        ufactor = 1000000000;
        unit = "Billions"   
    }     
    if (min < 1 && max < 1) {
        unit = "Percentage";
        ufactor = 0.01;
    }
"""

# <codecell>

metadata_series_info_map = """//~metadata_series_info_map
var seriesInfoMap = %s;
"""

metadata_iso3_map = """//~metadata_iso3_map
var iso3Map = %s;
"""

# <codecell>

graph_size = """//~graph_size (width, height, )
var w = getParameterByName("w",%i);
var h = getParameterByName("h",%i);
"""

graph_title_location = """//~graph_title_location - this should be included before graph_header is called
var tloc = getParameterByName("tloc","header");
var titleColor = getParameterByName("tcolor","#000");
"""

graph_header = """//~graph_header (header_height, footer_height, header_height_if_no_subtitle
var headerHeight = %i;
var footerHeight = %i;

if (graphSubtitle == "none"){
    headerHeight = %i;
    if (graphTitle == "none"){
        headerHeight = 0;
    }
}
if (typeof tloc != "undefined" && tloc != "header") {
    headerHeight = 0;
}
"""

graph_default_size = graph_size % (456, 362)
graph_default_header = graph_header % (50, 30, 30)


graph_set_title = """//~graph_set_title (title)
graphTitle = getParameterByName("title", "%s");
"""

graph_set_subtitle = """//~graph_set_subtitle (subtitle)
graphSubtitle = getParameterByName("subtitle", "%s");
"""

graph_set_subtitle_country = """//~graph_set_subtitle_country
var countryname = iso3Map[iso3.toUpperCase()]["countryname"];
graphSubtitle = getParameterByName("subtitle", countryname);
"""

graph_set_yaxis_label = """//graph_set_yaxis_label
graphYAxisLabel = getParameterByName("yaxis", "%s");
"""

svg_draw_title = """//~svg_draw_title
        titleLocationMap = {
            "header":{
                "x": 0,
                "y": -1 * headerHeight,
                "text-anchor": "start"
            },
            "topright":{
                "x": (width),
                "y": 0,
                "text-anchor": "end"
            },
            "topleft":{
                "x": 10,
                "y": 0,
                "text-anchor": "start"
            },
            "bottomright":{
                "x": (width),
                "y": (height - 58),
                "text-anchor": "end"
            },
            "bottomleft":{
                "x": 10,
                "y": (height - 58),
                "text-anchor": "start"
            }
        }
        titleLocation = titleLocationMap[tloc];
        if (graphTitle != "none"){
            svg.append("text")
                .attr("class", "title")
                .attr("x", titleLocation["x"] + "px")
                .attr("y", titleLocation["y"] + "px")
                .style("text-anchor", titleLocation["text-anchor"])
                .style("fill", titleColor)
                .text(graphTitle);
        }
"""

svg_draw_subtitle = """//svg_draw_subtitle
        if (graphSubtitle != "none"){
            svg.append("text")
                .attr("class", "subtitle")
                .attr("x", titleLocation["x"] + "px")
                .attr("y", titleLocation["y"] + 27 + "px")
                .style("text-anchor", titleLocation["text-anchor"])
                .style("fill", titleColor)
                .text(graphSubtitle);
        }
"""

svg_draw_source = """//~svg_draw_source
        svg.append("g")
		  .attr("transform", "translate(10," + (height - 15) + ")")
        .append("text")
			.attr("class", "source")
			.attr("dy","10px")
			.text("Source: " + seriesInfoMap[seriesName]["originalsource"]);
"""

