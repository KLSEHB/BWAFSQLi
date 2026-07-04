<?php
    function processQueryResult($sql, $difficulty) {
        $servername = "localhost";
        $username = "root";
        $password = "123456";
        $db = "sqliDB";

        $conn = new mysqli($servername, $username, $password, $db);

        if ($conn->connect_error) {
            die("Connection failed: " . $conn->connect_error);
        }

        $rs = $conn->query($sql);

        if ($rs) {
            $numRows = $rs->num_rows;

            if (strpos($difficulty, 'union') !== false) {
                $count = 0;
                while ($row = $rs->fetch_assoc() and $count < 10) {
                    echo "ID: " . $row["id"] . " - Name: " . $row["name"] . " - Pass: " . $row["pass"] . "<br>";
                    $count += 1;
                }
                if ($numRows == 0) {
                    echo "<br>";
                }
            } elseif (strpos($difficulty, 'error') !== false) {
                echo 'No errors<br>';
            } elseif (strpos($difficulty, 'bool') !== false) {
                if ($numRows != 0) {
                    echo "success<br>";
                } else {
                    echo "fail<br>";
                }
            } else {
                echo "Equivalence experiments<br>";
            }
        } else {
            if (strpos($difficulty, 'union') !== false) {
	 echo $conn->error;
                echo 'errors<br>';
            } elseif (strpos($difficulty, 'error') !== false) {
                if ($conn->error) {
                    echo $conn->error;
                } else {
                    echo 'No errors<br>';
                }
            } elseif (strpos($difficulty, 'bool') !== false) {
                echo 'errors<br>';
            } elseif (strpos($difficulty, 'time') !== false) {
                echo 'errors<br>';
            } else {
                echo "Equivalence experiments<br>";
            }
        }
        $conn->close();
    }

