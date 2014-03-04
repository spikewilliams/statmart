<!DOCTYPE html>
<html>
<head>
  <meta http-equiv="content-type" content="text/html; charset=UTF-8">
  <title>d3.js scatterplot and heat (density) chart - jsFiddle demo</title>

  	<script type='text/javascript' src='http://d3js.org/d3.v3.min.js'></script>

	<style>

	svg {
	  font: bold 14px sans-serif;
	}

	.axis path,
	.axis line {
	  fill:none;
	  stroke: #000;
	  shape-rendering: crispEdges;
	}

	.line {
	  fill: none;
	  stroke: steelblue;
	  stroke-width: 1.5px;
	}

	.area {
	  fill: steelblue;
	}

	.area1 {
	  fill: #ccc;
	}
	</style>

</head>
<body>

<script type='text/javascript'>//<![CDATA[

function getParameterByName(name) {
    var match = RegExp('[?&]' + name + '=([^&]*)').exec(window.location.search);
    return match && decodeURIComponent(match[1].replace(/\+/g, ' '));
}

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

var margin = {top: 20, right: 22, bottom: 50, left: 50},
    width = 500 - margin.left - margin.right,
    height = 309 - margin.top - margin.bottom;

var parseDate = d3.time.format("%Y").parse;

var x = d3.time.scale()
    .range([0, width]);

var y = d3.scale.linear()
    .range([height, 0]);


var xAxis = d3.svg.axis()
    .scale(x)
    .orient("bottom");

var yAxis = d3.svg.axis()
    .scale(y)
    .orient("left");

var line = d3.svg.line()
    .x(function(d) { return x(d.date); })
    .y(function(d) { return y(d.norm); });

var area = d3.svg.area()
    .x(function(d) { return x(d.date); })
    .y0(height)
    .y1(function(d) { return y(d.close); });

var color = d3.scale.category10();

var svg = d3.select("body").append("svg")
    .attr("width", width + margin.left + margin.right)
    .attr("height", height + margin.top + margin.bottom)
  .append("g")
    .attr("transform", "translate(" + margin.left + "," + margin.top + ")");


d3.csv(fileName, function(error, data) {

	var dbase = {}

  data.forEach(function(d) {
  	d.series = d.Item;
    d.date = parseDate(d.Year);
    d.close = +d["Value"] / ufactor;
    if (""+d.Year == "1990"){
    	dbase[d.series] = d.close;
    }
  });

  data.forEach(function(d) {
  	d.norm = (d.close/dbase[d.series]) * 100;
  });

  s = ["Construction",
  			"Electricity, gas and water supply",
  			"Financial intermediation, real estate, renting and business activities",
  			"Mining and quarrying",
  			"Agriculture, hunting, forestry and fishing"];
  data = data.filter(function(d){return s.indexOf(d.series) > -1});
  series = [];
  for (i = 0; i < s.length; i++){
  	series[i] = data.filter(function(d){return d.series === s[i]});
  }

  x.domain(d3.extent(data, function(d) { return d.date; }));
  y.domain([d3.min(data, function(d) { return d.norm * 0.93; }),
  			d3.max(data, function(d) { return d.norm * 1.05; })]);

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
      .attr("dx", "-124px")
      .style("text-anchor", "middle")
      .style("font-size", "16px")
      .style("padding-right","50px")
      .text("Value in USD (" + unit + " - 2005)");

	for (i = 0; i < series.length; i++) {
	  svg.append("path")
		  .datum(series[i])
		  .attr("class", "line")
		  .attr("d", line)
		  .style("stroke", function(d) { return color(i); });
	}

/* //TODO: this does not center at 100 on the graph like I want it to
	svg.append("g")
		.attr("class", "line")
		.append("line").attr("x1",0)
		.attr("y1",height - 100)
		.attr("x2",width)
		.attr("y2",height - 100);
*/
/*
   svg.append("path")
      .datum(series1)
      .attr("class", "area1")
      .attr("d",function(d) { return area(d.series); }); */
});
//]]>

</script>


</body>


</html>
