<?php
	include("../../inc/settings.php");
	$db_connection = mysqli_connect($db_host,$db_user,$db_pass,$db_schema);

	parse_str($_SERVER['QUERY_STRING'], $params);
	$iso3 = $params['iso3'];
	global $serieses;
	$serieses = ["pop_".$iso3."_desa"];
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
		function getParameterByName(name, default_param) {
			var match = RegExp('[?&]' + name + '=([^&]*)').exec(window.location.search);
			if (match) {
				return match && decodeURIComponent(match[1].replace(/\+/g, ' '));
			}
			return default_param;
		}

		var iso3 = "<?php print($iso3); ?>";

		//~metadata_iso3_map
		var iso3Map = {"ABW":{"countryname":"Aruba","series":"pop_abw_desa","numberyears":61},"AIA":{"countryname":"Anguilla","series":"pop_aia_desa","numberyears":61},"ATG":{"countryname":"Antigua and Barbuda","series":"pop_atg_desa","numberyears":61},"BHS":{"countryname":"Bahamas","series":"pop_bhs_desa","numberyears":61},"BLZ":{"countryname":"Belize","series":"pop_blz_desa","numberyears":61},"BMU":{"countryname":"Bermuda","series":"pop_bmu_desa","numberyears":61},"BRB":{"countryname":"Barbados","series":"pop_brb_desa","numberyears":61},"CUB":{"countryname":"Cuba","series":"pop_cub_desa","numberyears":61},"CYM":{"countryname":"Cayman Islands","series":"pop_cym_desa","numberyears":61},"DMA":{"countryname":"Dominica","series":"pop_dma_desa","numberyears":61},"DOM":{"countryname":"Dominican Republic","series":"pop_dom_desa","numberyears":61},"GLP":{"countryname":"Guadeloupe","series":"pop_glp_desa","numberyears":61},"GRD":{"countryname":"Grenada","series":"pop_grd_desa","numberyears":61},"GUY":{"countryname":"Guyana","series":"pop_guy_desa","numberyears":61},"HTI":{"countryname":"Haiti","series":"pop_hti_desa","numberyears":61},"JAM":{"countryname":"Jamaica","series":"pop_jam_desa","numberyears":61},"KNA":{"countryname":"Saint Kitts and Nevis","series":"pop_kna_desa","numberyears":61},"LCA":{"countryname":"Saint Lucia","series":"pop_lca_desa","numberyears":61},"MSR":{"countryname":"Montserrat","series":"pop_msr_desa","numberyears":61},"PRI":{"countryname":"Puerto Rico","series":"pop_pri_desa","numberyears":61},"SUR":{"countryname":"Suriname","series":"pop_sur_desa","numberyears":61},"TCA":{"countryname":"Turks and Caicos Islands","series":"pop_tca_desa","numberyears":61},"TTO":{"countryname":"Trinidad and Tobago","series":"pop_tto_desa","numberyears":61},"VCT":{"countryname":"Saint Vincent and The Grenadines","series":"pop_vct_desa","numberyears":61},"VGB":{"countryname":"Virgin Islands, British","series":"pop_vgb_desa","numberyears":61},"VIR":{"countryname":"Virgin Islands, U.S.","series":"pop_vir_desa","numberyears":61}};

		//~metadata_series_info_map
		var seriesInfoMap = {"pop_abw_desa":{"originalsource":"UN Department of Economic and Social Affairs: Population Divison","proximatesource":null},"pop_aia_desa":{"originalsource":"UN Department of Economic and Social Affairs: Population Divison","proximatesource":null},"pop_atg_desa":{"originalsource":"UN Department of Economic and Social Affairs: Population Divison","proximatesource":null},"pop_bhs_desa":{"originalsource":"UN Department of Economic and Social Affairs: Population Divison","proximatesource":null},"pop_blz_desa":{"originalsource":"UN Department of Economic and Social Affairs: Population Divison","proximatesource":null},"pop_bmu_desa":{"originalsource":"UN Department of Economic and Social Affairs: Population Divison","proximatesource":null},"pop_brb_desa":{"originalsource":"UN Department of Economic and Social Affairs: Population Divison","proximatesource":null},"pop_cub_desa":{"originalsource":"UN Department of Economic and Social Affairs: Population Divison","proximatesource":null},"pop_cym_desa":{"originalsource":"UN Department of Economic and Social Affairs: Population Divison","proximatesource":null},"pop_dma_desa":{"originalsource":"UN Department of Economic and Social Affairs: Population Divison","proximatesource":null},"pop_dom_desa":{"originalsource":"UN Department of Economic and Social Affairs: Population Divison","proximatesource":null},"pop_glp_desa":{"originalsource":"UN Department of Economic and Social Affairs: Population Divison","proximatesource":null},"pop_grd_desa":{"originalsource":"UN Department of Economic and Social Affairs: Population Divison","proximatesource":null},"pop_guy_desa":{"originalsource":"UN Department of Economic and Social Affairs: Population Divison","proximatesource":null},"pop_hti_desa":{"originalsource":"UN Department of Economic and Social Affairs: Population Divison","proximatesource":null},"pop_jam_desa":{"originalsource":"UN Department of Economic and Social Affairs: Population Divison","proximatesource":null},"pop_kna_desa":{"originalsource":"UN Department of Economic and Social Affairs: Population Divison","proximatesource":null},"pop_lca_desa":{"originalsource":"UN Department of Economic and Social Affairs: Population Divison","proximatesource":null},"pop_msr_desa":{"originalsource":"UN Department of Economic and Social Affairs: Population Divison","proximatesource":null},"pop_pri_desa":{"originalsource":"UN Department of Economic and Social Affairs: Population Divison","proximatesource":null},"pop_sur_desa":{"originalsource":"UN Department of Economic and Social Affairs: Population Divison","proximatesource":null},"pop_tca_desa":{"originalsource":"UN Department of Economic and Social Affairs: Population Divison","proximatesource":null},"pop_tto_desa":{"originalsource":"UN Department of Economic and Social Affairs: Population Divison","proximatesource":null},"pop_vct_desa":{"originalsource":"UN Department of Economic and Social Affairs: Population Divison","proximatesource":null},"pop_vgb_desa":{"originalsource":"UN Department of Economic and Social Affairs: Population Divison","proximatesource":null},"pop_vir_desa":{"originalsource":"UN Department of Economic and Social Affairs: Population Divison","proximatesource":null}};

		countryInfo = iso3Map[iso3.toUpperCase()];
		countryName = countryInfo["countryname"];
		seriesInfo = seriesInfoMap["pop_" + iso3 + "_desa"];
		source = seriesInfo["originalsource"];
		if (source == null){
			source = seriesInfo["proximatesource"];
		}

    </script>
    <script id="csv" type="text/csv">series,iso3,countryname,year,value
<?php
	include("../../inc/series_csv_query.php");
?></script>
    <script>

        d3.select("#chart")
            .call(smChart("lineGraph")
                .decimalPlaces(0)
                .divisor(1000)
                .labelField("year")
                .subtitle(getParameterByName("subtitle", countryName))
                .source(getParameterByName("source", source))
                .title(getParameterByName("title", "Population"))
                .titleLoc(getParameterByName("tloc","header"))
                .yAxisLabel("$Unit")
            );

    </script>
  </body>
</html>