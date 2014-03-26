<!DOCTYPE html>
<html>
  <head>
     <title>Bar Chart</title>
     <meta http-equiv="X-UA-Compatible" content="IE=9">
<style><?php include('../../inc/style_basic.php'); ?></style>
  </head>
  <body>
    <div id="chart"></div>
    <script src="../../js/d3.v3.min.js"></script>
    <script src="../../js/statmartCharts.js"></script>
    <script>


    </script>
    <script id="csv" type="text/csv">series,name,iso3,value
        <?php
            include("../../inc/settings.php");
            $db_connection = mysqli_connect($db_host,$db_user,$db_pass,$db_schema);
            include("reservoir_csv_query.php");
        ?></script>
    <script>

        d3.select("#chart")
            .call(smChart("barChart")
    			.width(getParameterByName("w",456))
				.height(getParameterByName("w",362))
                .divisor(1000)
                .decimalPlaces(3)
                .title("Reservoirs of the Caribbian")
                .subtitle("Thousands of imperial mega gallons")
                .source("Economic Commission for Latin America and the Caribbean")
            );

    </script>
  </body>
</html>