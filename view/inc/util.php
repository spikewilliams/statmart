<?php
	include_once("settings.php");
	$db_connection = mysqli_connect($db_host,$db_user,$db_pass,$db_schema);


	function makeValuesReferenced($arr){ // because php is a mess
		$refs = array();
		foreach($arr as $key => $value){
			$refs[$key] = &$arr[$key];
		}
		return $refs;
	}

	function csvQuery($query, $params=False, $types=False){
		global $db_connection;
		$rowcount = 0;
		if ($stmt = mysqli_prepare($db_connection, $query)) {
			if ($params){
				call_user_func_array('mysqli_stmt_bind_param', array_merge (array($stmt, $types), makeValuesReferenced($params)));
			}

			mysqli_stmt_execute($stmt);
			$result = $stmt->get_result();

			$fields = mysqli_fetch_fields(mysqli_stmt_result_metadata($stmt));
			$headers = array();
			foreach ($fields as $field){
				$headers[] = $field->name;
			}
			mysqli_stmt_close($stmt);

			if ( $result) {
				$out = fopen('php://output', 'w');
				while ($row = $result->fetch_array(MYSQLI_NUM)) {
					fputcsv($out, array_values($row));
					$rowcount++;
				}
				fclose($out);
			}
		}
		return $rowcount;
	}

	function writeParamsJS($params){
		if (array_key_exists('dp',$params)){
			print (".decimalPlaces(${params['dp']})");
		}
		if (array_key_exists('div',$params)){
			print (".divisor(${params['div']})");
		}
		if (array_key_exists('h',$params)){
			print (".height(${params['h']})");
		}
		if (array_key_exists('source',$params)){
			print (".source('${params['source']}')");
		}
		if (array_key_exists('subtitle',$params)){
			print (".subtitle('${params['subtitle']}')");
		}
		if (array_key_exists('title',$params)){
			print (".title('${params['title']}')");
		}
		if (array_key_exists('tloc',$params)){
			print (".titleLoc(${params['loc']})");
		}
		if (array_key_exists('unit',$params)){
			print (".unit('${params['unit']}')");
		}
		if (array_key_exists('w',$params)){
			print (".width(${params['w']})");
		}
		if (array_key_exists('xal',$params)){
			print (".xAxisLabel('${params['xal']}')");
		}
		if (array_key_exists('xdiv',$params)){
			print (".xdiv(${params['xdiv']})");
		}
		if (array_key_exists('yal',$params)){
			print (".yAxisLabel('${params['yal']}')");
		}
		if (array_key_exists('yaloffset',$params)){
			print (".yLabelOffset(${params['yaloffset']})");
		}
	}

?>