<!DOCTYPE html>
<html>
<head>
  <meta http-equiv="content-type" content="text/html; charset=UTF-8">
  <title>Regional demand for water</title>
  <script type='text/javascript' src='http://d3js.org/d3.v3.min.js'></script>
	<style>
	
 <?php
		include("inc/style_basic.php");
 ?> 

	</style>
</head>
<body>
<script>

function getParameterByName(name) {
    var match = RegExp('[?&]' + name + '=([^&]*)').exec(window.location.search);
    return match && decodeURIComponent(match[1].replace(/\+/g, ' '));
}

var countryName = getParameterByName("country");
var unit = getParameterByName("unit");
var interval = getParameterByName("interval");
var seriesName = getParameterByName("series");

var ufactor = 1000;
if (unit == "millions"){
	ufactor = 1000000
} else if (unit == "thousands"){
	ufactor = 1000;
} else {
	unit = "thousands";
	ufactor = 1000;
}

var countryLower = countryName.toLowerCase().replace(/ /g,"-");
var fileName = "gen2/rcm/water/regional-demand_jamaica_annual.csv";

var snames = "blue-mountain-south,kingston,rio-cobre,rio-minho,black-river,carbarita-river,great-river,martha-brae-river,dry-harbour-mountain,blue-mountain-north".split(",")

 <?php
		include("inc/axis.php");
 ?> 
var color = d3.scale.category10();

function clone(obj) {
    if (null == obj || "object" != typeof obj) return obj;
    var copy = obj.constructor();
    for (var attr in obj) {
        if (obj.hasOwnProperty(attr)) copy[attr] = obj[attr];
    }
    return copy;
}


var series = Array();
for (i = 0; i < snames.length; i++){
		series[i] =  Array();
}
			
d3.csv(fileName, function(error, data) {
	
  data.forEach(function(d) {
		for (i = 0; i < snames.length; i++){
			c = clone(d);
    	c.date = parseDate(d.year.substring(0,4));
    	c.value = +d[snames[i]] / ufactor;
			c.close = c.value;
			d.date = c.date;
			if (c.value > d.value){
				d.value = c.value;
			}
			series[i].push(c);
  	}
  });


  x.domain(d3.extent(data, function(d) { return d.date; }));
  y.domain([0,d3.max(data, function(d) { return 100 ; })]);

  svg.append("g")
      .attr("class", "x axis")
      .attr("transform", "translate(0," + (height) + ")")
      .call(xAxis)
      .selectAll("text")
            .style("text-anchor", "end")
            .attr("dx", "-.8em")
            .attr("dy", "-.25em")
            .attr("transform", function(d) {
                return "rotate(-90)"
            });

  svg.append("g")
      .attr("class", "y axis")
      .call(yAxis)
    .append("text")
      .attr("transform", "rotate(-90)")
      .attr("dy", "-38px")
      .attr("dx", "-104px")
      .style("text-anchor", "middle")
      .style("font-weight", "bold")
      .style("padding-right","10px")
      .text("Water demand by region");

	for (i = 0; i < series.length; i++) {
	  svg.append("path")
		  .datum(series[i])
		  .attr("class", "line")
		  .attr("d", line)
		  .style("stroke", function(d) { return color(i); });
	}
});

</script>