<?php
	include("../../inc/settings.php");
	$db_connection = mysqli_connect($db_host,$db_user,$db_pass,$db_schema);
?>
<!DOCTYPE html>
<html>
  <head>
     <title>Population Line Graph</title>
     <meta http-equiv="X-UA-Compatible" content="IE=9">
<style><?php include('../../inc/style_basic.php'); ?></style>
  </head>
  <body>
    <div id="chart"></div>
    <script src="../../js/d3.v3.min.js"></script>
    <script src="../../js/statmartCharts.js"></script>
    <script>
    </script>
    <script id="csv" type="text/csv">contraceptive,year,value,pvalue,pctchange,iso3
<?php
	include("pop_contraceptives_query.php");
?></script>
    <script>

	d3.select("#chart")
		.call(smChart("scatterPlot")
			.decimalPlaces(2)
			.divisor(0.01)
			.height(400)
			.labelField("iso3")
			.valueField("contraceptive")
			.subtitle("12 Caribbean countries - 1990 to 2009")
			.source("CEPALStat and UN DESA")
			.title("Contraception usage and population growth")
			.titleLoc("header")
			.width(600)
			.xDivisor(0.01)
			.xAxisLabel("Percentage annual population growth")
			.xValueField("pctchange")
			.yAxisLabel("Percentage of women using contraception")
		);

    </script>
  </body>
</html>