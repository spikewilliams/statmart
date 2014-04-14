<?php
	include("../../inc/util.php");
?>
<!DOCTYPE html>
<html>
  <head>
     <title>Water Usage Graph</title>
     <meta http-equiv="X-UA-Compatible" content="IE=9">
<style><?php include('../../inc/style_basic.php'); ?></style>
  </head>
  <body>
    <div id="waterUsageChart"></div>
    <script src="../../js/d3.v3.min.js"></script>
    <script src="../../js/statmartCharts.js"></script>

<script id="waterUsageCountries" type="text/csv">iso3,countryname,series,originalsource,proximatesource
<?php
	$query = <<<SQLQUERY
		SELECT DISTINCT L.iso3, L.countryname, O.series, S.originalsource, S.proximatesource
		FROM observation AS O
		INNER JOIN location AS L ON O.locationid = L.id
		INNER JOIN series AS S ON O.series = S.identifier
		WHERE O.series LIKE  "water-usage_%_sidsrcm";
SQLQUERY;

	csvQuery($query);
?></script>

<script>
	function srs(iso3){ // convenience funciton to provide a quick way of refering to these series
		return "water-usage_" + iso3 + "_sidsrcm";
	}

	var exclude = [srs("cub"),srs("tto"),srs("kna")];

	var data = d3.csv.parse(d3.select("#waterUsageCountries").text());
	var seriesLabels = [];
	data.forEach(function(d) {
		if (exclude.indexOf(d.series) > -1){
			return;
		}
		seriesLabels[d.series] = d.countryname;
	});

	var numLabels = seriesLabels.length;
	var dFilter = function(d) {
		return (d.series in seriesLabels);
	}

	var seriesFilter = function(data, series){
		return data.filter(function(d){ return d.series == series; });
	}

</script>

<script id="waterUsageData" type="text/csv">series,iso3,countryname,year,totalusage,population,value
<?php
	$query = <<<SQLQUERY
		SELECT O.series, L.iso3, L.countryname, D.year, CONVERT(O.value, UNSIGNED) as totalusage, P.population, ROUND(CONVERT(O.value, UNSIGNED)* 1000000/P.population) as gallonspercapita
		FROM observation as O
		INNER JOIN date as D ON O.dateid = D.id
		INNER JOIN location as L ON O.locationid = L.id
		INNER JOIN
		(SELECT CONVERT(O.value, UNSIGNED) as population, D.year as year, O.locationid as locationid, O.series as series
		FROM observation as O,
		date as D WHERE O.series like "pop_%_desa" AND O.dateid = D.id) P
			ON P.locationid = O.locationid and P.year = D.year
		WHERE O.series like "water-usage_%_sidsrcm"
SQLQUERY;

	csvQuery($query);
?></script>

    <script>
	var chart = d3.select("#waterUsageChart")
		.call(smChart("timeSeriesLineGraph")
			.dataFilter(dFilter)
			.dataSelector("#waterUsageData")
			.decimalPlaces(0)
			.divisor(1)
			.labelField("year")
			.legendHeight(120)
            .seriesFilter(seriesFilter)
            .seriesLabels(seriesLabels)
			.subtitle("Imperial gallons per person per year")
			.source("SIDS RCM")
			.title("Per-capita water usage")
			.titleLoc("header")
			.unit("Gallons")
			.yAxisLabel("none")
		<?php
			parse_str($_SERVER['QUERY_STRING'], $params);
			writeParamsJS($params);
		?>
		);
    </script>
  </body>
</html>