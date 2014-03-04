<!DOCTYPE html>
<html>
<head>
  <meta http-equiv="content-type" content="text/html; charset=UTF-8">
  <title>National GDP data from the United Nations Economic Commission for Latin America and the Caribbean (ECLAC)</title>
  <script type='text/javascript' src='http://d3js.org/d3.v3.min.js'></script>

	<style>
	
 <?php
		include("inc/style_basic.php");
 ?> 

	</style>
</head>
<body>

<script type='text/javascript'>//<![CDATA[

function getParameterByName(name) {
    var match = RegExp('[?&]' + name + '=([^&]*)').exec(window.location.search);
    return match && decodeURIComponent(match[1].replace(/\+/g, ' '));
}

var currentUSD = 1.15848; //factor for converting 2005 dollars to current (2013)
var cYear = 2013;

iso3 = getParameterByName("iso3").toLowerCase();
unit = getParameterByName("unit");
seriesName = getParameterByName("series");
var ufactor = 1000;
if (unit == "billions"){
	ufactor = 1000
} else if (unit == "millions"){
	ufactor = 1;
} else {
	unit = "billions";
	ufactor = 1000;
}
fileName = "csv/cepalstat/2216/2216_" + iso3 + ".csv";

if (!seriesName){
	seriesName = "Gross domestic product (GDP)";
}

 <?php
		include("inc/axis.php");
 ?> 
 
d3.csv(fileName, function(error, data) {
  data.forEach(function(d) {
  	if (d.Item != seriesName){
  		return null;
  	}
  	d.series = d.Item;
    d.date = parseDate(d.Year);
    d.value = (+d["Value"] / ufactor) * currentUSD;
  });

  data = data.filter(function(d){return d.series === seriesName});
  x.domain(d3.extent(data, function(d) { return d.date; }));
  y.domain([0,d3.max(data, function(d) { return d.value; })]);

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

  svg.append("g")
      .attr("class", "y axis")
      .call(yAxis)
    .append("text")
      .attr("transform", "rotate(-90)")
      .attr("dy", "-38px")
      .attr("dx", "-100px")
      .style("text-anchor", "middle")
      .style("font-weight", "bold")
      .style("padding-right","10px")
      .text("Value in current USD (" + unit + ")");

  svg.append("path")
      .datum(data)
      .attr("class", "area")
      .attr("d", area);
});
//]]>

</script>


</body>


</html>
