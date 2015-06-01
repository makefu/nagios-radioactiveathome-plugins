#!/bin/zsh
first=$(curl -s http://radioactiveathome.org/boinc/gettrickledata.php?hostid=14364| head -n 1 | cut -d: -f 2 )

current=$(curl  -s "http://radioactiveathome.org/boinc/gettrickledata.php?hostid=14364&start=$(($first-1))" | tail -n 1 )
count=$(echo "$current" | cut -d, -f 3)
timespan=$(echo "$current" |cut -d, -f 7)
printf "Current uSV: %s" $(echo "scale=5;( $count / $timespan ) / 171.232876" | bc)
