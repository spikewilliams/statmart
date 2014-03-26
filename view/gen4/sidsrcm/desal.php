<!DOCTYPE html>
<html><head><meta http-equiv='content-type' content='text/html; charset=UTF-8'/>
<title>Water usage</title>
<script type='text/javascript' src='../../js/d3.v3.min.js'></script>
<style><?php include('../../inc/style_basic.php'); ?></style></head>
<body><script type='text/javascript'>//<![CDATA[
//~metadata_iso3_map
var iso3Map = {"ATG":{"countryname":"Antigua and Barbuda","series":"water-usage_atg_sidsrcm","numberyears":6},"CUB":{"countryname":"Cuba","series":"water-usage_cub_sidsrcm","numberyears":21},"JAM":{"countryname":"Jamaica","series":"water-usage_jam_sidsrcm","numberyears":13},"SUR":{"countryname":"Suriname","series":"water-usage_sur_sidsrcm","numberyears":3},"TTO":{"countryname":"Trinidad and Tobago","series":"water-usage_tto_sidsrcm","numberyears":27}};

//~metadata_series_info_map
var seriesInfoMap = {"water-usage_atg_sidsrcm":{"originalsource":null,"proximatesource":"SIDS RCM"},"water-usage_cub_sidsrcm":{"originalsource":null,"proximatesource":"SIDS RCM"},"water-usage_jam_sidsrcm":{"originalsource":"Economic and Social Survey of Jamaica","proximatesource":"SIDS RCM"},"water-usage_sur_sidsrcm":{"originalsource":"Surinaamsche Waterleiding Maatschappij","proximatesource":"SIDS RCM"},"water-usage_tto_sidsrcm":{"originalsource":null,"proximatesource":"SIDS RCM"}};

//~util_function_get_parameters_by_name

function getParameterByName(name, default_param) {
    var match = RegExp('[?&]' + name + '=([^&]*)').exec(window.location.search);
    if (match) {
    	return match && decodeURIComponent(match[1].replace(/\+/g, ' '));
    }
    return default_param;
}

//~js_series_name_from_iso3_parameter
    iso3 = getParameterByName("iso3");
    seriesName = "water-usage_" + iso3 + "_sidsrcm"

//~js_data_url_series_query
    dataURL = "../../series_query.php?s=" + seriesName;

//~graph_set_title (title)
graphTitle = getParameterByName("title", "Water usage");

//~graph_set_subtitle_country
var countryname = iso3Map[iso3.toUpperCase()]["countryname"];
graphSubtitle = getParameterByName("subtitle", countryname);

//~graph_size (width, height, )
var w = getParameterByName("w",456);
var h = getParameterByName("h",362);

//~graph_title_location - this should be included before graph_header is called
var tloc = getParameterByName("tloc","header");
var titleColor = getParameterByName("tcolor","#000");

//~graph_header (header_height, footer_height, header_height_if_no_subtitle
var headerHeight = 50;
var footerHeight = 30;

if (graphSubtitle == "none"){
    headerHeight = 30;
    if (graphTitle == "none"){
        headerHeight = 0;
    }
}
if (typeof tloc != "undefined" && tloc != "header") {
    headerHeight = 0;
}

//~include_js_d3_basic_axis
    <?php
		include("../../inc/axis.php");
     ?>

//~js_d3_start_csv
     d3.csv(dataURL, function(error, data) {

//~js_guess_unit
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

//~js_d3_process_annual_csv_data
        data.forEach(function(d) {
            d.date = parseDate(d.year);
            d.value = (+d["value"] / ufactor);
        });

//~js_d3_build_simple_xy_domains
        x.domain(d3.extent(data, function(d) { return d.date; }));
        y.domain([0,d3.max(data, function(d) { return d.value; })]);

//~js_d3_svg_build_x_axis
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

//~js_d3_svg_build_y_axis_label

        svg.append("g")
          .attr("class", "y axis")
          .call(yAxis)
        .append("text")
          .attr("transform", "rotate(-90)")
          .attr("dy", "-34px")
          .attr("dx", (height * -1) + "px")
          .style("text-anchor", "start")
          .style("padding-right","10px")

          .text("$Unit of imperial mega gallons".replace("$Unit",unit).replace("$unit",unit.toLowerCase()));

//~jd_d3_svg_draw_line
           svg.append("path")
              .datum(data)
              .attr("class", "line")
              .attr("d", line);

//~svg_draw_title
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

//svg_draw_subtitle
        if (graphSubtitle != "none"){
            svg.append("text")
                .attr("class", "subtitle")
                .attr("x", titleLocation["x"] + "px")
                .attr("y", titleLocation["y"] + 27 + "px")
                .style("text-anchor", titleLocation["text-anchor"])
                .style("fill", titleColor)
                .text(graphSubtitle);
        }

//~svg_draw_source

        source = seriesInfoMap[seriesName]["originalsource"];
        if (source == null){
            source = seriesInfoMap[seriesName]["proximatesource"]
        }
        svg.append("g")
		  .attr("transform", "translate(10," + (height - 15) + ")")
        .append("text")
			.attr("class", "source")
			.attr("dy","10px")
			.text("Source: " + source);

//~js_d3_end_csv
    });

//]]></script></body></html>