<!DOCTYPE html>
<html><head><meta http-equiv='content-type' content='text/html; charset=UTF-8'/>
<title>Death rate associated with tuberculosis</title>
<script type='text/javascript' src='http://localhost:81/js/d3.v3.min.js'></script>
<style><?php include('../../inc/style_basic.php'); ?></style></head>
<body><script type='text/javascript'>//<![CDATA[
//~metadata_iso3_map
var iso3Map = {"ABW":{"countryname":"Aruba","series":"tb-death-rate_abw_cepalstat","numberyears":22},"BHS":{"countryname":"Bahamas","series":"tb-death-rate_bhs_cepalstat","numberyears":22},"BLZ":{"countryname":"Belize","series":"tb-death-rate_blz_cepalstat","numberyears":22},"BRB":{"countryname":"Barbados","series":"tb-death-rate_brb_cepalstat","numberyears":22},"CUB":{"countryname":"Cuba","series":"tb-death-rate_cub_cepalstat","numberyears":22},"CYM":{"countryname":"Cayman Islands","series":"tb-death-rate_cym_cepalstat","numberyears":22},"DMA":{"countryname":"Dominica","series":"tb-death-rate_dma_cepalstat","numberyears":22},"DOM":{"countryname":"Dominican Republic","series":"tb-death-rate_dom_cepalstat","numberyears":22},"GRD":{"countryname":"Grenada","series":"tb-death-rate_grd_cepalstat","numberyears":22},"GUY":{"countryname":"Guyana","series":"tb-death-rate_guy_cepalstat","numberyears":22},"HTI":{"countryname":"Haiti","series":"tb-death-rate_hti_cepalstat","numberyears":22},"JAM":{"countryname":"Jamaica","series":"tb-death-rate_jam_cepalstat","numberyears":22},"KNA":{"countryname":"Saint Kitts and Nevis","series":"tb-death-rate_kna_cepalstat","numberyears":22},"LCA":{"countryname":"Saint Lucia","series":"tb-death-rate_lca_cepalstat","numberyears":22},"MSR":{"countryname":"Montserrat","series":"tb-death-rate_msr_cepalstat","numberyears":22},"PRI":{"countryname":"Puerto Rico","series":"tb-death-rate_pri_cepalstat","numberyears":22},"SUR":{"countryname":"Suriname","series":"tb-death-rate_sur_cepalstat","numberyears":22},"TCA":{"countryname":"Turks and Caicos Islands","series":"tb-death-rate_tca_cepalstat","numberyears":22},"TTO":{"countryname":"Trinidad and Tobago","series":"tb-death-rate_tto_cepalstat","numberyears":22},"VCT":{"countryname":"Saint Vincent and The Grenadines","series":"tb-death-rate_vct_cepalstat","numberyears":22},"VGB":{"countryname":"Virgin Islands, British","series":"tb-death-rate_vgb_cepalstat","numberyears":22},"VIR":{"countryname":"Virgin Islands, U.S.","series":"tb-death-rate_vir_cepalstat","numberyears":22}};

//~metadata_series_info_map
var seriesInfoMap = {"tb-death-rate_abw_cepalstat":{"originalsource":"United Nations Statistics Division: Millennium Indicators Database","proximatesource":"CEPALStat"},"tb-death-rate_bhs_cepalstat":{"originalsource":"United Nations Statistics Division: Millennium Indicators Database","proximatesource":"CEPALStat"},"tb-death-rate_blz_cepalstat":{"originalsource":"United Nations Statistics Division: Millennium Indicators Database","proximatesource":"CEPALStat"},"tb-death-rate_brb_cepalstat":{"originalsource":"United Nations Statistics Division: Millennium Indicators Database","proximatesource":"CEPALStat"},"tb-death-rate_cub_cepalstat":{"originalsource":"United Nations Statistics Division: Millennium Indicators Database","proximatesource":"CEPALStat"},"tb-death-rate_cym_cepalstat":{"originalsource":"United Nations Statistics Division: Millennium Indicators Database","proximatesource":"CEPALStat"},"tb-death-rate_dma_cepalstat":{"originalsource":"United Nations Statistics Division: Millennium Indicators Database","proximatesource":"CEPALStat"},"tb-death-rate_dom_cepalstat":{"originalsource":"United Nations Statistics Division: Millennium Indicators Database","proximatesource":"CEPALStat"},"tb-death-rate_grd_cepalstat":{"originalsource":"United Nations Statistics Division: Millennium Indicators Database","proximatesource":"CEPALStat"},"tb-death-rate_guy_cepalstat":{"originalsource":"United Nations Statistics Division: Millennium Indicators Database","proximatesource":"CEPALStat"},"tb-death-rate_hti_cepalstat":{"originalsource":"United Nations Statistics Division: Millennium Indicators Database","proximatesource":"CEPALStat"},"tb-death-rate_jam_cepalstat":{"originalsource":"United Nations Statistics Division: Millennium Indicators Database","proximatesource":"CEPALStat"},"tb-death-rate_kna_cepalstat":{"originalsource":"United Nations Statistics Division: Millennium Indicators Database","proximatesource":"CEPALStat"},"tb-death-rate_lca_cepalstat":{"originalsource":"United Nations Statistics Division: Millennium Indicators Database","proximatesource":"CEPALStat"},"tb-death-rate_msr_cepalstat":{"originalsource":"United Nations Statistics Division: Millennium Indicators Database","proximatesource":"CEPALStat"},"tb-death-rate_pri_cepalstat":{"originalsource":"United Nations Statistics Division: Millennium Indicators Database","proximatesource":"CEPALStat"},"tb-death-rate_sur_cepalstat":{"originalsource":"United Nations Statistics Division: Millennium Indicators Database","proximatesource":"CEPALStat"},"tb-death-rate_tca_cepalstat":{"originalsource":"United Nations Statistics Division: Millennium Indicators Database","proximatesource":"CEPALStat"},"tb-death-rate_tto_cepalstat":{"originalsource":"United Nations Statistics Division: Millennium Indicators Database","proximatesource":"CEPALStat"},"tb-death-rate_vct_cepalstat":{"originalsource":"United Nations Statistics Division: Millennium Indicators Database","proximatesource":"CEPALStat"},"tb-death-rate_vgb_cepalstat":{"originalsource":"United Nations Statistics Division: Millennium Indicators Database","proximatesource":"CEPALStat"},"tb-death-rate_vir_cepalstat":{"originalsource":"United Nations Statistics Division: Millennium Indicators Database","proximatesource":"CEPALStat"}};

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
    seriesName = "tb-death-rate_" + iso3 + "_cepalstat"

//~js_data_url_series_query
    dataURL = "http://localhost:81/series_query.php?s=" + seriesName;

//~graph_set_title (title)
graphTitle = getParameterByName("title", "Death rate - Tuberculosis");

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
		include("C:/portal/statmart/view/inc/axis.php");
     ?> 
 
//~js_d3_start_csv
     d3.csv(dataURL, function(error, data) {

//~js_set_unit (unit type, unit factor)
    unit = "Percentage of registered deaths";
    ufactor = 1;

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

//~js_d3_svg_build_y_axis_unit_label

        svg.append("g")
          .attr("class", "y axis")
          .call(yAxis)
        .append("text")
          .attr("transform", "rotate(-90)")
          .attr("dy", "-34px")
          .attr("dx", (height * -1) + "px")
          .style("text-anchor", "start")
          .style("padding-right","10px")

          .text(unit);

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
        svg.append("g")
		  .attr("transform", "translate(10," + (height - 15) + ")")
        .append("text")
			.attr("class", "source")
			.attr("dy","10px")
			.text("Source: " + seriesInfoMap[seriesName]["originalsource"]);

//~js_d3_end_csv
    });

//]]></script></body></html>