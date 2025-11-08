<?php
    // 改进后的函数，使用面向对象的方式
    function processQueryResult($sql, $difficulty) {
        $servername = "localhost";
        $username = "root";
        $password = "123456";
        $db = "sqliDB";

        // 创建数据库连接
        $conn = new mysqli($servername, $username, $password, $db);

        // 检查连接
        if ($conn->connect_error) {
            die("Connection failed: " . $conn->connect_error);
        }

        $rs = $conn->query($sql); // 使用面向对象方式查询

        if ($rs) {
            $numRows = $rs->num_rows; // 使用面向对象方式获取行数

            if (strpos($difficulty, 'union') !== false) {
                $count = 0;
                while ($row = $rs->fetch_assoc() and $count < 10) { // 使用面向对象方式获取数据
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
        } else { // 错误处理
            if (strpos($difficulty, 'union') !== false) {
	 echo $conn->error;
                echo 'errors<br>';
            } elseif (strpos($difficulty, 'error') !== false) {
                if ($conn->error) {
                    echo $conn->error; // 使用面向对象方式获取错误信息
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

