<!DOCTYPE html>
<html>
<head>
  <meta http-equiv="content-type" content="text/html; charset=UTF-8">
  <title><function title at 0x0000000005B78598></title>
  <script type='text/javascript' src='http://localhost:81/js/d3.v3.min.js'></script>
    <style>
 <?php
		include("C:/portal/statmart/view//inc/style_basic.php");
 ?> 
	</style>
</head><body><script type='text/javascript'>//<![CDATA[
//~util_function_get_parameters_by_name

function getParameterByName(name) {
    var match = RegExp('[?&]' + name + '=([^&]*)').exec(window.location.search);
    return match && decodeURIComponent(match[1].replace(/\+/g, ' '));
}


//~util_currency_converter_2005

var currentUSD = 1.15848; //factor for converting 2005 dollars to current (2013)
var cYear = 2013;

function convert2005USDtoCurrent(amount){
    return amount * currentUSD;
}


//~js_series_name_from_s_parameter
    seriesName = getParameterByName("s");

//~js_data_url_series_query
    dataURL = "http://localhost:81//series_query.php?s=" + seriesName;

// include_js_d3_basic_axis 
    <?php
		include("C:/portal/statmart/view//inc/axis.php");
     ?> 
 
//~js_set_unit (unit type, unit factor)
    unit = "percentage";
    ufactor = 1;

//~js_d3_start_csv
     d3.csv(dataURL, function(error, data) {

//~js_d3_process_annual_csv_data
        data.forEach(function(d) {
            d.date = parseDate(d.year);
            d.value = (+d["value"] * ufactor);
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
          .attr("dy", "-38px")
          .attr("dx", "-120px")
          .style("text-anchor", "middle")
          .style("font-weight", "bold")
          .style("padding-right","10px")
          .text(unit);

//~jd_d3_svg_draw_area
           svg.append("path")
              .datum(data)
              .attr("class", "area")
              .attr("d", area);

//~js_d3_end_csv
    });

//]]></script></body></html>