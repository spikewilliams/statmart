<?php

	include("../../inc/util.php");

	parse_str($_SERVER['QUERY_STRING'], $params);
	$iso3 = $params["iso3"];
	$serieses = ["gdp-sec%_". $iso3 ."_cepalstat"];
	$types = "s";
?>
<!DOCTYPE html>
<html>
  <head>
     <title>GDP by Sector</title>
     <meta http-equiv="X-UA-Compatible" content="IE=9">
<style><?php include('../../inc/style_basic.php'); ?></style>
  </head>
  <body>
    <div id="gdpSecChart"></div>
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

<script id="topSectors" type="text/csv">series,description,value
<?php
	$query = <<<SQLQUERY
		SELECT O.series, S.description, O.value
		FROM observation AS O
		INNER JOIN date AS D ON O.dateid = D.id
		INNER JOIN series AS S ON O.series = S.identifier
		WHERE O.series LIKE ?
		AND D.year="2012"
		ORDER BY CONVERT(O.value,SIGNED) DESC
SQLQUERY;

	csvQuery($query, $serieses, $types);
?></script>

<script>
	function srs(s){ // convenience funciton to provide a quick way of refering to these series
		return "gdp-sec--" + s + "_" + iso3 + "_cepalstat";
	}

	var exclude = [srs("gdp"),srs("tva"),srs("taxes"),srs("discrep")];

	var exclusionaryPairs = [];
	exclusionaryPairs[srs("hr")] =		srs("wrtrghr");
	exclusionaryPairs[srs("wrtrg")] =	srs("wrtrghr");
	exclusionaryPairs[srs("aghufo")] =	srs("aghufofi");
	exclusionaryPairs[srs("fish")] =	srs("aghufofi");
	exclusionaryPairs[srs("tsaa")] =	srs("tsc");
	exclusionaryPairs[srs("pt")] =	srs("tsc");

	var data = d3.csv.parse(d3.select("#topSectors").text());

	var allSeriesLabels = [];
	var seriesOrder = [];
	var maxSeries = 16;
	var blockList = [];
	data.forEach(function(d) {
		if (exclude.indexOf(d.series) > -1){
			return;
		}
		sLabel = d.description.substring("Sectoral GDP: ".length);
		allSeriesLabels[d.series] = sLabel;
		if (seriesOrder.length < maxSeries && blockList.indexOf(d.series) == -1){
			seriesOrder.push(d.series);
			// weed out aggregates when components are available
			if (d.series in exclusionaryPairs){seriesOrder.splice(seriesOrder.indexOf(exclusionaryPairs[d.series]),1);
				seriesOrder.push(d.series);
				blockList.push(exclusionaryPairs[d.series]); // for the unfortunate cases when agregates come in lower than their components
			}
		}
	});

	allSeriesLabels[srs("public")] = "Public spending and health, education, social and personal services";
	allSeriesLabels[srs("mq")] = "Mining, quarrying, and oil and gas extraction";

	var seriesLabels = [];
	for(var i = 0; i < seriesOrder.length; i++){
		var s = seriesOrder[i];
		seriesLabels[s] = allSeriesLabels[s];
	}

	var dFilter = function(d) {
		return (d.series in seriesLabels);
	}

	var seriesFilter = function(data, series){
		return data.filter(function(d){ return d.series == series; });
	}
</script>

<script id="secGDPCountries" type="text/csv">iso3,countryname
<?php
	$query = <<<SQLQUERY
		SELECT DISTINCT L.iso3, L.countryname
		FROM observation AS O
		INNER JOIN location AS L ON O.locationid = L.id
		WHERE O.series LIKE  "gdp-sec_%_cepalstat";
SQLQUERY;

	csvQuery($query);
?></script>
<script>
	var data = d3.csv.parse(d3.select("#secGDPCountries").text());
	var gdpCountries = [];
	data.forEach(function(d) {
		gdpCountries[d.iso3.toLowerCase()] = d.countryname;
	});

	var countryName = gdpCountries[iso3];
</script>

<script id="gdpData" type="text/csv">series,description,iso3,countryname,year,value
<?php
	$query = <<<SQLQUERY
		SELECT O.series, S.description, L.iso3, L.countryname, D.year, O.value
		FROM observation AS O
		INNER JOIN date AS D ON O.dateid = D.id
		INNER JOIN location AS L ON O.locationid = L.id
		INNER JOIN series AS S ON O.series = S.identifier
		WHERE O.series LIKE  ?
SQLQUERY;

	csvQuery($query, $serieses, $types);
?></script>

    <script>
    	var color = d3.scale.category20();
    	var seriesAbrevs = ['firerba','skip_1','wrtrg','wrtrghr','aghufo','aghufofi','cstrn','egws','fisim','fish','hr','mfg','mq','pt','skip_2','public','tsaa','tsc','wrtrghr'];


    	for (var i = 0; i < seriesAbrevs.length; i++){
    		color(srs(seriesAbrevs[i]));
    	}

        var chart = d3.select("#gdpSecChart")
            .call(smChart("timeSeriesLineGraph")
            	.color(color)
            	.dataFilter(dFilter)
            	.dataSelector("#gdpData")
                .decimalPlaces(0)
                .divisor(1000)
                .labelField("year")
                .legendHeight(seriesOrder.length * 20)
                .height(550 + seriesOrder.length * 20)
                .seriesFilter(seriesFilter)
                .seriesOrder(seriesOrder)
                .seriesLabels(seriesLabels)
                .subtitle(getParameterByName("subtitle", countryName))
                .source("Economic Commission for Latin America and the Caribbean (CEPALStat)")
                .title(getParameterByName("title", "Contribution to GDP by sector"))
                .titleLoc(getParameterByName("tloc","header"))
                .yAxisLabel("$Unit of USD (2005 equivalent)")
            );
    </script>
  </body>
</html>