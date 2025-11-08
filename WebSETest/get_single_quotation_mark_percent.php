<?php
    include 'global_library.php';
    $id = $_GET['id'];
    $difficulty = $_GET['difficulty'];
	
    $sql = "SELECT * FROM users WHERE id like '%$id%'";
    #echo "Search: ".$id."<br>";
    #echo $sql ."<br>";

    processQueryResult($sql, $difficulty);

