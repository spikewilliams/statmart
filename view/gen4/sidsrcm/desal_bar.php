<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<!-- Generated with d3-generator.com -->
<html>
  <head>
     <title>Bar Chart</title>
     <meta http-equiv="X-UA-Compatible" content="IE=9">
<style><?php include('../../inc/style_basic.php'); ?></style>
  </head>
  <body>
    <div id="chart"></div>
    <script src="../../js/d3.v3.min.js"></script>
    <script>
function renderChart() {

var data = d3.csv.parse(d3.select('#csv').text());
var valueLabelWidth = 50; // space reserved for value labels (right)
var barHeight = 26; // height of one bar
var barPadding = 3;
var barLabelWidth = 300; // space reserved for bar labels
var barLabelPadding = 10; // padding between bar and bar labels (left)
var gridLabelHeight = 18; // space reserved for gridline labels
var gridChartOffset = 10; // space between start of grid and first bar
var maxBarWidth = 450; // width of the bar with the max value
var headerHeight = 50;
var footerHeight = 25;


// accessor functions
var barLabel = function(d) { return d['countryname']; };
var barValue = function(d) { return parseInt(d['total']/1000); };


var graphTitle = "Desalination capacity in the Caribbean";
var graphSubtitle = "Thousands of imperial gallons per day";
var titleColor = "#000;"

// scales
var yScale = d3.scale.ordinal().domain(d3.range(0, data.length)).rangeBands([0, data.length * barHeight]);
var y = function(d, i) { return yScale(i); };
var yText = function(d, i) { return y(d, i) + yScale.rangeBand() / 2; };
var x = d3.scale.linear().domain([0, d3.max(data, barValue)]).range([0, maxBarWidth]);

var width = maxBarWidth + barLabelWidth + valueLabelWidth;
var height = gridLabelHeight + gridChartOffset + data.length * barHeight + headerHeight + footerHeight;

// svg container element
var chart = d3.select('#chart').append("svg")
  .attr('width', width)
  .attr('height', height);

var cbody = chart.append('g')
	.attr('transform', 'translate(0,' +  headerHeight + ')');

// grid line labels
var gridContainer = cbody.append('g')
  .attr('transform', 'translate(' + barLabelWidth + ',' + gridLabelHeight + ')');
gridContainer.selectAll("text").data(x.ticks(10)).enter().append("text")
  .attr("x", x)
  .attr("dy", -3)
  .attr("text-anchor", "middle")
  .text(String);
// vertical grid lines
gridContainer.selectAll("line").data(x.ticks(10)).enter().append("line")
  .attr("x1", x)
  .attr("x2", x)
  .attr("y1", 0)
  .attr("y2", yScale.rangeExtent()[1] + gridChartOffset)
  .style("stroke", "#ccc");
// bar labels
var labelsContainer = cbody.append('g')
  .attr('transform', 'translate(' + (barLabelWidth - barLabelPadding) + ',' + (gridLabelHeight + gridChartOffset) + ')');
labelsContainer.selectAll('text').data(data).enter().append('text')
  .attr('y', yText)
  .attr('stroke', 'none')
  .attr('fill', 'black')
  .attr("dy", ".35em") // vertical-align: middle
  .attr('text-anchor', 'end')
  .text(barLabel);
// bars
var barsContainer = cbody.append('g')
  .attr('transform', 'translate(' + barLabelWidth + ',' + (gridLabelHeight + gridChartOffset) + ')');
barsContainer.selectAll("rect").data(data).enter().append("rect")
  .attr('y', y)
  .attr('height', yScale.rangeBand() - barPadding)
  .attr('width', function(d) { return x(barValue(d)); })
  .attr('stroke', 'white')
  .attr('fill', 'steelblue');
// bar value labels
barsContainer.selectAll("text").data(data).enter().append("text")
  .attr("x", function(d) { return x(barValue(d)); })
  .attr("y", yText)
  .attr("dx", 3) // padding-left
  .attr("dy", ".35em") // vertical-align: middle
  .attr("text-anchor", "start") // text-align: right
  .attr("fill", "black")
  .attr("stroke", "none")
  .text(function(d) { return d3.round(barValue(d), 2); });
// start line
barsContainer.append("line")
  .attr("y1", -gridChartOffset)
  .attr("y2", yScale.rangeExtent()[1] + gridChartOffset)
  .style("stroke", "#000");


//~svg_draw_title
	  titleLocationMap = {
		  "header":{
			  "x": barLabelWidth,
			  "y": -1 * headerHeight,
			  "text-anchor": "start"
		  }
	  }
	  titleLocation = titleLocationMap["header"];

	  if (graphTitle != "none"){
		  cbody.append("text")
			  .attr("class", "title")
			  .attr("x", titleLocation["x"] + "px")
			  .attr("y", titleLocation["y"] + "px")
			  .style("text-anchor", titleLocation["text-anchor"])
			  .style("fill", titleColor)
			  .text(graphTitle);
	  }

//svg_draw_subtitle
	  if (graphSubtitle != "none"){
		  cbody.append("text")
			  .attr("class", "subtitle")
			  .attr("x", titleLocation["x"] + "px")
			  .attr("y", titleLocation["y"] + 27 + "px")
			  .style("text-anchor", titleLocation["text-anchor"])
			  .style("fill", titleColor)
			  .text(graphSubtitle);
	  }

		var source = "Economic Commission for Latin America and the Caribbean";

		chart.append("g")
		  .attr("transform", "translate(" + titleLocation["x"] + "," + (height - footerHeight + 10) + ")")
		.append("text")
			.attr("class", "source")
			.attr("dy","10px")
			.text("Source: " + source);
}



    </script>
    <script id="csv" type="text/csv">series,countryname,iso3,total
		<?php
			include("../../inc/settings.php");
			$db_connection = mysqli_connect($db_host,$db_user,$db_pass,$db_schema);
			include("desal_csv_query.php");
		?></script>
    <script>renderChart();</script>
  </body>
</html>