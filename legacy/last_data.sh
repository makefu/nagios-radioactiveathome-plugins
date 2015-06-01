#!/bin/sh
first=$(curl -s http://radioactiveathome.org/boinc/gettrickledata.php?hostid=14364| head -n 1 | cut -d: -f 2 )

last_date=$(curl  -s "http://radioactiveathome.org/boinc/gettrickledata.php?hostid=14364&start=$(($first-1))" \
  | tail -n 1 |  cut -d, -f4)
date_ts=$(date -d"$last_date" +%s )
date_now=$(date +%s)

echo "Seconds since last data:" $(($date_now -  $date_ts))
if test  $(($date_now -  $date_ts < 60*60*24)) -eq '0' ;then
  echo "bad"
  exit 1
else
  echo "good"
  exit 0
fi
