stack_classroom
===============

Here you will find several scripts to interact with StackExchange sites to use in the classroom

You can setup these scripts in two ways:
1. Set up on your own server: If you have a web server with PHP and python --the vast majority of web servers, you can just copy these files into a folder you can access from the web and voila.
2. No setup: You can use the scripts directly from http://cs.neiu.edu/~fiacobelli/so2/ 

How to use
===========
1. StackExchange users have ids on the discussion fora. Ask the ids of your students and record them. For example: 5192, 4240, 6777 and 6093
2. Your class will use one of the discussion fora available. Know the name of the forum. For example, if they have to go to philosophy.stackexchange.com, the name of the forum is "philosophy". If they go to math.stackexchange.com, the name of the forum is "math". If they go to stackoverflow.com, the name of the forum is stackoverflow.
3. Knowing the forum name and the ids of your students you can:
 a. See what questions your students are posting by going to http://cs.neiu.edu/~fiacobelli/so2/users.php?uids=<student ids separated by semi-colon>&site=<name of the forum>. So, if your student ids are 5192, 4240, 6777 and 6093 and the forum is philosphy, you should go to http://cs.neiu.edu/~fiacobelli/so2/users.php?uids=5192;4240;6777;6093&site=philosphy
 b. To see the reputation change by quarter and total reputation of your users, the drill is the same, but instead of users.php, you type reps.php. In our example: http://cs.neiu.edu/~fiacobelli/so2/reps.php?uids=5192;4240;6777;6093&site=philosphy
 c. To see a summary of student's activity within a given period of time, you go to: http://cs.neiu.edu/~fiacobelli/so2/soverflow_query_stats.php?uids=5192;4240;6777;6093&site=philosophy&from=05.01.2014+00:00:00&to=05.20.2014+00:00:00
In this last case you specify a "from" and a "to" date in the format MM.DD.YYY+hh:mm:ss (that is the month number, the day, the year (separated by a dot), a PLUS sign, the hours, minutes and seconds (separated by colon).
