<!DOCTYPE html>
<html>
<head>
  <meta http-equiv="content-type" content="text/html; charset=UTF-8">
  <title>National population data from the UN Department of Economic and Social Affairs (DESA)</title>
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
var ufactor = 1000;
if (unit == "millions"){
	ufactor = 1000
} else if (unit == "thousands"){
	ufactor = 1;
} else {
	unit = "thousands";
	ufactor = 1;
}

var countryLower = countryName.toLowerCase().replace(/ /g,"-");
var fileName = "csv/desa/pop_" + countryLower + ".csv";

 <?php
		include("inc/axis.php");
 ?> 
		
d3.csv(fileName, function(error, data) {
  data.forEach(function(d) {
    d.date = parseDate(d.year);
    d.value = +d[countryLower] / ufactor;
  });

  x.domain(d3.extent(data, function(d) { return d.date; }));
  y.domain([0,d3.max(data, function(d) { return d.value; })]);

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
      .attr("dx", "-74px")
      .style("text-anchor", "middle")
      .style("font-weight", "bold")
      .style("padding-right","10px")
      .text("Population (" + unit + ")");

   svg.append("path")
      .datum(data)
      .attr("class", "area")
      .attr("d", area);
});

</script>