<?php
include_once("util.php");

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

csvQuery($query, $serieses, $types);