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
				}
				fclose($out);
			}
		}
	}
?>