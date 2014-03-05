<?php

parse_str($_SERVER['QUERY_STRING'], $params);
/*$sid = $params['sid'];
$src = $params['src'];
$iso = $params['iso'];

$series = $sid."_".$iso."_".$src; */

$s = $params['s'];
if (strlen($s) == 0){
    die;
}

//gdp-sec-cstrn\_%\_cepalstat
//sid=gdp-sec-cstrn&iso=tto&src=cepalstat

$db_connection = mysqli_connect("127.0.0.1","root","","statmart");

$query = <<<SQLQUERY
SELECT O.series, L.iso3, L.countryname, D.year, O.value
FROM observation as O
INNER JOIN date as D ON O.dateid = D.id
INNER JOIN location as L ON O.locationid = L.id
WHERE
SQLQUERY;

$orr = "";
$types = "";
$serieses = explode(",",$s);
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
   // mysqli_stmt_store_result($stmt);
    
    $fields = mysqli_fetch_fields(mysqli_stmt_result_metadata($stmt));
    $headers = array();
    foreach ($fields as $field){
        $headers[] = $field->name;  
    }
    mysqli_stmt_close($stmt);
    
    header('Content-Type: text/plain');
    header('Pragma: no-cache');
    header('Expires: 0');
    
    $fp = fopen('php://output', 'w');
    if ($fp && $result) {
        fputcsv($fp, $headers);
        while ($row = $result->fetch_array(MYSQLI_NUM)) {
            fputcsv($fp, array_values($row));
        }
    }
    die;  
    
} else {
 printf("Query failed");   
}
