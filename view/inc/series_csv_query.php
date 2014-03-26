<?php

$query = <<<SQLQUERY
SELECT O.series, L.iso3, L.countryname, D.year, O.value
FROM observation as O
INNER JOIN date as D ON O.dateid = D.id
INNER JOIN location as L ON O.locationid = L.id
WHERE
SQLQUERY;

$orr = "";
$types = "";
foreach ($serieses as $series) {
    $query .= $orr . " O.series = ? ";
    $orr = " OR ";
    $types .= "s";
}

$query .= " ORDER BY D.year LIMIT 2000;";


function makeValuesReferenced($arr){ // because php is a mess
    $refs = array();
    foreach($arr as $key => $value)
        $refs[$key] = &$arr[$key];
    return $refs;
}

if ($stmt = mysqli_prepare($db_connection, $query)) {
    call_user_func_array('mysqli_stmt_bind_param', array_merge (array($stmt, $types), makeValuesReferenced($serieses)));

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
} else {
 printf("Query failed");
}
