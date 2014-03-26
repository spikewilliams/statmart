/*
    This chart is built using the pattern described at
    http://bost.ocks.org/mike/chart/

*/

function smChart(chartType) {

    var dataSelector = "#csv";

	var width = 456;
	var height = 362;
    var headerHeight = 50;
    var footerHeight = 25;
	var margin = {top: 5, right: 5, bottom: 50, left: 5};

    var valueLabelWidth = 50; // space reserved for value labels (right)
    var barHeight = 26; // height of one bar
    var barPadding = 3;
    var barLabelWidth = 300; // space reserved for bar labels
    var barLabelPadding = 10; // padding between bar and bar labels (left)
    var gridLabelHeight = 18; // space reserved for gridline labels
    var gridChartOffset = 4; // space between start of grid and first bar
    var maxBarWidth = 450; // width of the bar with the max value

    var labelField = "name";
    var valueField = "value";
    var dateFormat = "%Y"

    var title = "none";
    var subtitle = "none";
    var source = "none";
    var yAxisLabel = "none";
    var unit = "guess";
    var titleLoc = "header";
    var divisor = 1;
    var decimalPlaces = 2;


	var parseDate = d3.time.format(dateFormat).parse;


	// accessor functions
	var getLabel = function(d) { return d[labelField]; };
	var getDate  = function(d) { return parseDate(d[labelField]); };
	var getValue = function(d) { return parseFloat(+d[valueField])/divisor; };
	var getWholeValue = function(d) { return parseFloat(+d[valueField]) };

	function barChart(selection) { // barChart is adapted from code provided by d3-generator.com

		selection.each(function() {
			var data = d3.csv.parse(d3.select(dataSelector).text());

			// scales
			var yScale = d3.scale.ordinal().domain(d3.range(0, data.length)).rangeBands([0, data.length * barHeight]);
			var y = function(d, i) { return yScale(i); };
			var yText = function(d, i) { return y(d, i) + yScale.rangeBand() / 2; };
			var x = d3.scale.linear().domain([0, d3.max(data, getValue)]).range([0, maxBarWidth]);

			var width = maxBarWidth + barLabelWidth + valueLabelWidth;
			var height = gridLabelHeight + gridChartOffset * 2 + data.length * barHeight + margin.top + headerHeight + footerHeight + margin.bottom;

			// svg container element
			var svg = d3.select('#chart').append("svg") ////////////////////////////////////////////// #chart -> selection?
			  .attr('width', width)
			  .attr('height', height);

			var cbody = svg.append('g')
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
			  .text(function(d) { return smTranslation(getLabel(d)); });
			// bars
			var barsContainer = cbody.append('g')
			  .attr('transform', 'translate(' + barLabelWidth + ',' + (gridLabelHeight + gridChartOffset) + ')');
			barsContainer.selectAll("rect").data(data).enter().append("rect")
			  .attr('y', y)
			  .attr('height', yScale.rangeBand() - barPadding)
			  .attr('width', function(d) { return x(getValue(d)); })
			  .attr('stroke', 'white')
			  .attr('fill', 'steelblue');
			// bar value labels
			barsContainer.selectAll("text").data(data).enter().append("text")
			  .attr("x", function(d) { return x(getValue(d)); })
			  .attr("y", yText)
			  .attr("dx", 3) // padding-left
			  .attr("dy", ".35em") // vertical-align: middle
			  .attr("text-anchor", "start") // text-align: right
			  .attr("fill", "black")
			  .attr("stroke", "none")
			  .text(function(d) { return d3.round(getValue(d), decimalPlaces); });
			// start line
			barsContainer.append("line")
			  .attr("y1", -gridChartOffset)
			  .attr("y2", yScale.rangeExtent()[1] + gridChartOffset)
			  .style("stroke", "#000");

			titleLocationMap = {
				"header":{
					"x": barLabelWidth,
					"y": 0,
					"text-anchor": "start"
				}
			}
			titleLocation = titleLocationMap[titleLoc];

			header = svg.append("g")
				.attr("transform", "translate(0," + margin.top + ")");
			sourceg = svg.append("g")
				.attr("transform", "translate(" + titleLocation["x"] + "," + (height - footerHeight - margin.bottom + 10) + ")");

			barChart.addTextElements();

		});
	}

	function lineGraph(selection) {
		selection.each(function() {

			var data = d3.csv.parse(d3.select(dataSelector).text());
			if (unit == "guess"){
				var guess = lineGraph.unitGuess(data);
				unit = guess["unit"];
				divisor = guess["divisor"];
			}

			if (subtitle == "none"){ // shrink the header if we don't need the space for title/subtitle
				headerHeight = headerHeight - 15;
				if (title == "none"){
					headerHeight = 0;
				}
			}
			if (typeof titleLoc != "undefined" && titleLoc != "header") {
				headerHeight = 0;
			}

			var plotWidth = width - margin.left - margin.right;
			var plotHeight = height - margin.top - margin.bottom - headerHeight - footerHeight;

		   data.forEach(function(d) {
				d.date = getDate(d);
				d.value = getValue(d);
			});

			var x = d3.time.scale()
				.domain(d3.extent(data, function(d) { return d.date; }))
			    .range([0, plotWidth - 1]);

			var y = d3.scale.linear()
				.domain([0,d3.max(data, function(d) { return d.value; })])
			    .range([plotHeight, 0]);

			var xAxis = d3.svg.axis()
			    .scale(x)
			    .orient("bottom")
			    .ticks(10);

			var yAxis = d3.svg.axis()
			    .scale(y)
			    .orient("left");

			var line = d3.svg.line()
			    .x(function(d) { return x(d.date); })
			    .y(function(d) { return y(d.value); });

			var area = d3.svg.area()
			    .x(function(d) { return x(d.date); })
			    .y0(plotHeight)
			    .y1(function(d) { return y(d.value); });

			var svg = d3.select('#chart').append("svg") /////////////////////////////////////////////////////////////
			    .attr("width", "100%")
			    .attr("height", height)
					.attr("viewBox", "0 0 " + width + " " + height)
			  .append("g")
    			.attr("transform", "translate(" + margin.left + "," + (margin.top + headerHeight) + ")");

			svg.append("g")
			  .attr("class", "x axis")
			  .attr("transform", "translate(0," + plotHeight + ")")
			  .call(xAxis)
				.selectAll("text")
					  .style("text-anchor", "end")
					  .attr("dx", "-.8em")
					  .attr("dy", "-.25em")
					  .attr("transform", function(d) {
						  return "rotate(-90)"
				});

			yaxisg = svg.append("g")
			  .attr("class", "y axis")
			  .call(yAxis)

			yAxisLabelTransform = "rotate(-90) translate(" + plotHeight * -1 + ",-34)";

           	svg.append("path")
              .datum(data)
              .attr("class", "line")
              .attr("d", line);

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
			titleLocation = titleLocationMap[titleLoc];

			header = svg.append("g")
				.attr("class","header")
				.attr("transform", "translate(0," + margin.top + ")");
			sourceg = svg.append("g")
				.attr("class","source")
				.attr("transform", "translate(" + (titleLocation["x"] + 10) + "," + (plotHeight + headerHeight + margin.top - 64) + ")"); //plotHeight - 10

			lineGraph.addTextElements();

		});
	}

	var builder;
	if (chartType == "barChart"){
		builder = barChart;
	} else if (chartType == "lineGraph"){
		builder = lineGraph;
	}
	builder.addTextElements = function() {
		if (title != "none"){
			header.append("text")
				.attr("class", "title")
				.attr("x", titleLocation["x"] + "px")
				.attr("y", titleLocation["y"] + "px")
				.style("text-anchor", titleLocation["text-anchor"])
				.text(title);
		}
		if (subtitle != "none"){
		  	header.append("text")
				.attr("class", "subtitle")
				.attr("x", titleLocation["x"] + "px")
				.attr("y", titleLocation["y"] + 27 + "px")
				.style("text-anchor", titleLocation["text-anchor"])
				.text(subtitle);
		}
		if (source != "none"){
			sourceg.append("text")
				.attr("class", "source")
				.text("Source: " + source);
		}
		if (yAxisLabel != "none"){
			yaxisg.append("text")
			  .attr("transform", yAxisLabelTransform)
			  .style("text-anchor", "start")
			  .style("padding-right","10px")
			  .text(yAxisLabel.replace("$Unit",unit));
		}
	}

	builder.unitGuess = function(data){ // this is a naive algorythm that doesn't do a great job
		unit = "";
		ufactor = 1;

		var max = d3.max(data, getWholeValue);
		var min = d3.min(data, getWholeValue);

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
		return {"unit":unit, "divisor": ufactor}
	}

    builder.dataSelector = function(v) {
        if (!arguments.length) { return dataSelector; }
        dataSelector = v;
        return builder;
    }

    builder.dateFormat = function(v) {
        if (!arguments.length) { return dateFormat; }
        dateFormat = v;
        parseDate = d3.time.format(dateFormat).parse;
        return builder;
    }

    builder.decimalPlaces = function(v) {
        if (!arguments.length) { return decimalPlaces; }
        decimalPlaces = v;
        return builder;
    }

    builder.divisor = function(v) {
        if (!arguments.length) { return divisor; }
        divisor = v;
        return builder;
    }

    builder.height = function(v) {
        if (!arguments.length) { return height; }
        height = v;
        return builder;
    }

    builder.labelField = function(v) {
        if (!arguments.length) { return labelField; }
        labelField = v;
        return builder;
    }

    builder.margin = function(v) {
        if (!arguments.length) { return margin; }
        margin = v;
        return builder;
    }

    builder.source = function(v) {
        if (!arguments.length) { return source; }
        source = v;
        return builder;
    }

    builder.subtitle = function(v) {
        if (!arguments.length) { return subtitle; }
        subtitle = v;
        return builder;
    }

    builder.title = function(v) {
        if (!arguments.length) { return title; }
        title = v;
        return builder;
    }

    builder.titleLoc = function(v) {
        if (!arguments.length) { return titleLoc; }
        titleLoc = v;
        return builder;
    }

    builder.valueField = function(v) {
        if (!arguments.length) { return valueField; }
        valueField = v;
        return builder;
    }

    builder.width = function(v) {
        if (!arguments.length) { return width; }
        width = v;
        return builder;
    }

    builder.yAxisLabel = function(v) {
        if (!arguments.length) { return yAxisLabel; }
        yAxisLabel = v;
        return builder;
    }

    return builder;
}

function smTranslation(text){
	return text; // language translation not yet implemented
}