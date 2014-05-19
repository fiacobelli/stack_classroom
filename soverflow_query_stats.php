<!-- This file has parameters to query stack overflow and produce summaries.
    Given a list of user IDs and a timeframe, it produces a summary of:
    1. reputation change during that time (per user)
    2. The number of questions asked
    3. The number of questions answered.
-->
<?php
$users=$_GET["uids"];
$site=$_GET["site"];
$from=$_GET["from"];
$to=$_GET["to"];
if (!isset($site))
   $site="stackoverflow";

$out = exec("python soverflow_query.py '".$users."' '".$from."' '".$to."' -s ".$site,$data);
$str_data = "<table>\n";
foreach ($data as $line){
        if (trim($line)==="")
            $str_data = $str_data."</table>";
        else
            #echo $line."<br/>";
            $str_data = $str_data."<tr><td>".$line."</td></tr>";
}
$str_data = preg_replace('/,/','</td><td>',$str_data);
echo $str_data;

?>
<html>
    <head>
        <script>
            response = "<?=$str_data?>"
            document.getElementById("message").innerHTML = response
        </script>
    </head>
    <body>
        <div id="message"></div>
    </body>
</html>
