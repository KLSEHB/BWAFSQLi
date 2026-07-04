<!DOCTYPE html>
<html lang="en">

    <head>
        <meta charset="utf-8">
        <title>SQLI web server</title>
    </head>

    <body>
        <pre>
  ____    ___   _      _  __        __     _       _              _
 / ___|  / _ \ | |    (_) \ \      / /___ | |__   | |_  ___  ___ | |_   ___   ___  _ __ __   __ ___  _ __
 \___ \ | | | || |    | |  \ \ /\ / // _ \| '_ \  | __|/ _ \/ __|| __| / __| / _ \| '__|\ \ / // _ \| '__|
  ___) || |_| || |___ | |   \ V  V /|  __/| |_) | | |_|  __/\__ \| |_  \__ \|  __/| |    \ V /|  __/| |
 |____/  \__\_\|_____||_|    \_/\_/  \___||_.__/   \__|\___||___/ \__| |___/ \___||_|     \_/  \___||_|
        </pre>

        <?php

            $servername = "localhost";
            $username = "root";
            $password = "123456";
            $db = "sqliDB";

            // Create connection
            $conn = new mysqli($servername, $username, $password, $db);

            // Check connection
            if ($conn->connect_error) {
            die("Connection failed: " . $conn->connect_error);
            }
        ?>

        <h2>SQL Union Injection on page.</h2>


        <h2> Task 1 get 数字型注入</h2>
         <form action="get_number.php" method="get">
          ID <input type="text" name="id"></br></br>
                      <input type="hidden" name="difficulty" id="difficulty" value="union">

          Submit Request: <button type="submit">Go</button>
        </form>

        <h2> Task 2 post 数字型注入</h2>
            <form action="post_number.php" method="post">
                id <input type="text" name="id"></br></br>
                <input type="hidden" name="difficulty" id="difficulty" value="union">

                Submit Request: <button type="submit">Go</button>
            </form>



        <h2> Task 3 get 单引号型注入</h2>
        <form action="get_single_quotation_mark.php" method="get">
            id <input type="text" name="id"></br></br>
            <input type="hidden" name="difficulty" id="difficulty" value="union">

            Submit Request: <button type="submit">Go</button>
        </form>



        <h2> Task 4 post 单引号型注入</h2>
        <form action="post_single_quotation_mark.php" method="post">
            id <input type="text" name="id"></br></br>
            <input type="hidden" name="difficulty" id="difficulty" value="union">

            Submit Request: <button type="submit">Go</button>
        </form>


        <h2> Task 5 get 双引号型注入</h2>
        <form action="get_double_quotation_mark.php" method="get">
            id <input type="text" name="id"></br></br>
            <input type="hidden" name="difficulty" id="difficulty" value="union">

            Submit Request: <button type="submit">Go</button>
        </form>



        <h2> Task 6 post 双引号型注入</h2>
        <form action="post_double_quotation_mark.php" method="post">
            id <input type="text" name="id"></br></br>
            <input type="hidden" name="difficulty" id="difficulty" value="union">

            Submit Request: <button type="submit">Go</button>
        </form>


        <h2> Task 7 get 括号+单引号型注入</h2>
        <form action="get_single_quotation_mark_bracket.php" method="get">
            id <input type="text" name="id"></br></br>
            <input type="hidden" name="difficulty" id="difficulty" value="union">

            Submit Request: <button type="submit">Go</button>
        </form>



        <h2> Task 8 post 括号+单引号型注入</h2>
        <form action="post_single_quotation_mark_bracket.php" method="post">
            id <input type="text" name="id"></br></br>
            <input type="hidden" name="difficulty" id="difficulty" value="union">

            Submit Request: <button type="submit">Go</button>
        </form>



        <h2> Task 9 get 括号+双引号型注入</h2>
        <form action="get_double_quotation_mark_bracket.php" method="get">
            id <input type="text" name="id"></br></br>
            <input type="hidden" name="difficulty" id="difficulty" value="union">

            Submit Request: <button type="submit">Go</button>
        </form>

        <h2> Task 10 post 括号+双引号型注入</h2>
        <form action="post_double_quotation_mark_bracket.php" method="post">
            id <input type="text" name="id"></br></br>
            <input type="hidden" name="difficulty" id="difficulty" value="union">

            Submit Request: <button type="submit">Go</button>
        </form>

        <h2> Task 11 get 单引号+百分号型注入</h2>
        <form action="get_single_quotation_mark_percent.php" method="get">
            id <input type="text" name="id"></br></br>
            <input type="hidden" name="difficulty" id="difficulty" value="union">

            Submit Request: <button type="submit">Go</button>
        </form>

        <h2> Task 12 post 单引号+百分号型注入</h2>
        <form action="post_single_quotation_mark_percent.php" method="post">
            id <input type="text" name="id"></br></br>
            <input type="hidden" name="difficulty" id="difficulty" value="union">

            Submit Request: <button type="submit">Go</button>
        </form>

        <h2> Task 13 get 双引号+百分号型注入</h2>
        <form action="get_double_quotation_mark_percent.php" method="get">
            id <input type="text" name="id"></br></br>
            <input type="hidden" name="difficulty" id="difficulty" value="union">

            Submit Request: <button type="submit">Go</button>
        </form>

        <h2> Task 14 get 双引号+百分号型注入</h2>
        <form action="get_double_quotation_mark_percent.php" method="post">
            id <input type="text" name="id"></br></br>
            <input type="hidden" name="difficulty" id="difficulty" value="union">

            Submit Request: <button type="submit">Go</button>
        </form>


    </body>
</html>
