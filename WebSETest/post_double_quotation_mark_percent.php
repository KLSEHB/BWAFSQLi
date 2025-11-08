<?php
    include 'global_library.php';
    $id = $_POST['id'];
    $difficulty = $_POST['difficulty'];

    $sql = 'SELECT * FROM users WHERE id="%' . $id . '%"';
    #echo "Search: ".$id."<br>";
    #echo $sql ."<br>";

    processQueryResult($sql, $difficulty);

