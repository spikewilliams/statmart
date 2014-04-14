<?php

include("../inc/util.php");

parse_str($_SERVER['QUERY_STRING'], $params);

$s = $params['s'];
if (strlen($s) == 0){
    die;
}
$serieses = explode(",",$s);
$md5 = substr(md5($_SERVER['QUERY_STRING']),0,6);
$chartName = "chart_" . $md5;
$countriesName = "countries_" . $md5;
$dataName = "data_" . $md5;

?><!DOCTYPE html>
<html>
  <head>
     <title>Series graph</title>
     <meta http-equiv="X-UA-Compatible" content="IE=9">
	<style><?php include('../inc/style_basic.php'); ?></style>
    <script src="../js/d3.v3.min.js"></script>
    <script src="../js/statmartCharts.js"></script>
  </head>
  <body>
    <div id="<?php print $chartName; ?>"></div>

<script id="<?php print $countriesName; ?>" type="text/csv">iso3,countryname,series,originalsource,proximatesource
<?php
	$query = <<<SQLQUERY
	SELECT DISTINCT L.iso3, L.countryname, S.originalsource, S.proximatesource
	FROM observation AS O
	INNER JOIN location AS L ON O.locationid = L.id
	INNER JOIN series AS S ON O.series = S.identifier
	WHERE
SQLQUERY;

	$orr = "";
	$types = "";

	foreach ($serieses as $series) {
		$query .= $orr . " O.series = ? ";
		$orr = " OR ";
		$types .= "s";
	}

	$query .= ";";

	csvQuery($query);
?></script>


<script id="<?php print $dataName; ?>" type="text/csv">series,iso3,countryname,year,value
<?php
include("../inc/series_csv_query.php");
?></script>

    <script>
	var data = d3.csv.parse(d3.select("#<?php print $dataName; ?>").text());

	var seriesLabels = [];
	data.forEach(function(d) {
		seriesLabels[d.series] = d.countryname;
	});

	var numLabels = seriesLabels.length;
	var dFilter = function(d) {
		return (d.series in seriesLabels);
	}

	var seriesFilter = function(data, series){
		return data.filter(function(d){ return d.series == series; });
	}
    <?php
    if ($rowcount == 0){
    	print "//XXX_NO_DATA_XXX";
    } else { ?>

	var chart = d3.select("#<?php print $chartName; ?>")
		.call(smChart("timeSeriesLineGraph")
			.dataSelector("#<?php print $dataName; ?>")
			.labelField("year")
			.legendHeight(60)
			.legendXSpace(180)
			.seriesLabels(seriesLabels)
			.seriesFilter(seriesFilter)
		<?php
			writeParamsJS($params);
		?>
		);

	<?php } ?>
    </script>
  </body>
</html>