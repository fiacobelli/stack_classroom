<?php
$users=$_GET["uids"];
$site=$_GET["site"];
if (!isset($site))
   $site="stackoverflow";
$ch = curl_init();
$url = "https://api.stackexchange.com/2.0/users/".$users."?order=desc&sort=reputation&site=".$site;
#echo $url;
curl_setopt($ch,CURLOPT_URL, $url);
curl_setopt($ch,CURLOPT_RETURNTRANSFER,1);
curl_setopt ($ch, CURLOPT_CONNECTTIMEOUT,10);
curl_setopt ($ch, CURLOPT_ENCODING, "");
#curl_setopt($ch, CURLOPT_HEADER, 1);
#curl_setopt($ch, CURLOPT_HTTP_VERSION, CURL_HTTP_VERSION_1_1);
$resp = curl_exec($ch);
?>
<html>
<head>
</head>
<body>
<div id="content">
</div>

<br><br>
<script type="text/javascript">
 var responseJ = <?=$resp?>;
 var items = responseJ.items;
 var isOdd = true;
 var bgcolor = new Array();
 bgcolor[0] = "99CCFF";
 bgcolor[1] = "FFFFFF";
 for(var i = 0;i< items.length;i++){
	 s = document.getElementById("content");
	 // Alternate colors
	 var bg = ""; 
	 if (isOdd)
	    bg = bgcolor[1];
	 else
	    bg = bgcolor[0];
         isOdd = !isOdd;

	 // Create the html.
	 s.innerHTML += generateHTML(items[i],bg);
}

function generateHTML(item,bgcol){
 	 uname = item.display_name;
	 uid = item.user_id;
	 reputation = item.reputation;
	 repChngQuarter = item.reputation_change_quarter;
	 photo = item.profile_image;
         img = "<img src='"+photo+"' height=30px; width=30px;/>";
         style="clear:both; background-color:"+bgcol+"; height:40; font-family:sans-serif;";
         div = "<div style='"+style+"'><div style='float:left;font-size:10px;width:80px;height:35px; border-right:thin solid black; margin-top:5px;margin-left:5px;'>"+img+"</div>"+uname+"("+uid+"): Total Rep:<b>"+reputation+"</b> - Rep change by quarter:<b>"+repChngQuarter+"</b></div>";
	 return div;
 
}

</script>

</body>
</html>
