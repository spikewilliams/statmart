var w = 456;
var h = 282;

var margin = {top: 0, right: 12, bottom: 50, left: 50},
    width = w - margin.left - margin.right,
    height = h - margin.top - margin.bottom;

var parseDate = d3.time.format("%Y").parse;

var x = d3.time.scale()
    .range([0, width - 1]);

var y = d3.scale.linear()
    .range([height, 0]);

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
    .y0(height)
    .y1(function(d) { return y(d.value); });

var svg = d3.select("body").append("svg")
    .attr("width", "100%")
    .attr("height", h)
		.attr("viewBox", "0 0 " + w + " " + h)
  .append("g")
    .attr("transform", "translate(" + margin.left + "," + margin.top + ")");