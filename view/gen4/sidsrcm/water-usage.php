<?php
	include("../../inc/util.php");

	parse_str($_SERVER['QUERY_STRING'], $params);
	$iso3 = $params["iso3"];
	$serieses = ["water-usage_" . $iso3 . "_sidsrcm"];
	$types = "s";
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
    <script>
		function getParameterByName(name, default_param) {
			var match = RegExp('[?&]' + name + '=([^&]*)').exec(window.location.search);
			if (match) {
				return match && decodeURIComponent(match[1].replace(/\+/g, ' '));
			}
			return default_param;
		}

		var iso3 = "<?php print($iso3); ?>";
    </script>

<script id="waterUsageCountries" type="text/csv">iso3,countryname,series,originalsource,proximatesource
<?php
	$query = <<<SQLQUERY
		SELECT DISTINCT L.iso3, L.countryname, S.originalsource, S.proximatesource
		FROM observation AS O
		INNER JOIN location AS L ON O.locationid = L.id
		INNER JOIN Series AS S ON O.series = S.identifier
		WHERE O.series LIKE  "water-usage_%_sidsrcm";
SQLQUERY;

	csvQuery($query);
?></script>

<script>
	var data = d3.csv.parse(d3.select("#waterUsageCountries").text());
	var wuCountries = [];
	var wuOSource = [];
	var wuPSource = [];
	data.forEach(function(d) {
		wuCountries[d.iso3.toLowerCase()] = d.countryname;
		wuOSource[d.iso3.toLowerCase()] = d.originalsource;
		wuPSource[d.iso3.toLowerCase()] = d.proximatesource;
	});

	var countryName = wuCountries[iso3];
	var source = wuOSource[iso3];
	if (source == null){
		source = wuPSource[iso3];
	}
</script>

<script id="waterUsageData" type="text/csv">series,iso3,countryname,year,value
<?php
include("../../inc/series_csv_query.php");

?></script>

    <script>
	var chart = d3.select("#waterUsageChart")
		.call(smChart("timeSeriesLineGraph")
			.dataSelector("#waterUsageData")
			.decimalPlaces(0)
			.divisor(1000)
			.labelField("year")
			.subtitle(getParameterByName("subtitle", countryName))
			.source(getParameterByName("source", source))
			.title(getParameterByName("title", "Total water usage"))
			.titleLoc(getParameterByName("tloc","header"))
		//	.unit("Imperial mega gallons")
			.yAxisLabel("$Unit")
		);
    </script>
  </body>
</html>