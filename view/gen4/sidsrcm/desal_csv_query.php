<?php

$query = <<<SQLQUERY
SELECT O.series, L.countryname, L.iso3, SUM( O.value ) AS desal
FROM observation AS O
INNER JOIN location AS L ON O.locationid = L.id
WHERE O.series LIKE  "water-desal_%_sidsrcm"
GROUP BY O.series;
SQLQUERY;

function makeValuesReferenced($arr){ // because php is a mess
    $refs = array();
    foreach($arr as $key => $value)
        $refs[$key] = &$arr[$key];
    return $refs;
}

if ($stmt = mysqli_prepare($db_connection, $query)) {
  //  call_user_func_array('mysqli_stmt_bind_param', array_merge (array($stmt, $types), makeValuesReferenced($serieses)));

    mysqli_stmt_execute($stmt);
    $result = $stmt->get_result();
   // mysqli_stmt_store_result($stmt);

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

} else {
 printf("Query failed");
}
