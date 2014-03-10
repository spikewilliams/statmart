<!DOCTYPE html>
<html>
<head>
  <meta http-equiv="content-type" content="text/html; charset=UTF-8">
  <title>National GDP data from the United Nations Economic Commission for Latin America and the Caribbean (ECLAC)</title>
  <script type='text/javascript' src='js/d3.v3.min.js'></script>

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

seriesName = getParameterByName("s");

dataURL = "series_query.php?s=" + seriesName;

if (!seriesName){
	seriesName = "Gross domestic product (GDP)";
}

 <?php
		include("inc/axis.php");
 ?> 
 
 d3.csv(dataURL, function(error, data) {
 
    
    var max = d3.max(data, function(d) { return d["value"]; });
    var min = d3.min(data, function(d) { return d["value"]; });
    console.log(min);
    console.log(max);
    unit = "";     
    if (min > 1000 && max > 10000) {
        unit = "thousands"   
    }
    if (min > 100000 && max > 1000000) {
        unit = "millions"   
    }
    if (min > 100000000 && max > 1000000000) {
        unit = "billions"   
    }     
    var ufactor = 1;
    if (unit == "billions"){
        ufactor = 1000000000
    } else if (unit == "millions"){
        ufactor = 1000000;
    } else {
        unit = "thousands";
        ufactor = 1000;
    }
     
     data.forEach(function(d) {
        d.date = parseDate(d.year);
        d.value = (+d["value"] / ufactor) * currentUSD;
     });
     

     
    //data = data.filter(function(d){return d.series === seriesName});
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
      .attr("dx", "-120px")
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
Some additional text goes here

</body>


</html>
