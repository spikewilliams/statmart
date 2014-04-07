<?php

$query = <<<SQLQUERY
SELECT C.contraception, C.year, O.value, P.value as pvalue, ((O.value - P.value) / O.value)/2 as pctchange, C.iso3
FROM observation as O
INNER JOIN
(SELECT O.value as contraception, D.id as dateid, D.year as year, D.year - 2 as previous, L.id as locationid, L.iso3
FROM observation as O, location as L, date as D
WHERE O.series LIKE "contraception_%_cepalstat" AND O.locationid = L.id AND O.dateid = D.id) C
	ON C.dateid = O.dateid and C.locationid = O.locationid
INNER JOIN
(SELECT O.value as value, D.year as year, O.locationid as locationid, O.series as series
FROM observation as O,
date as D WHERE O.series like "pop_%_desa" AND O.dateid = D.id) P
	ON P.year = C.previous AND P.locationid = C.locationid and P.series = O.series
WHERE O.series LIKE "pop_%_desa"
ORDER BY C.iso3;
SQLQUERY;

if ($stmt = mysqli_prepare($db_connection, $query)) {
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
