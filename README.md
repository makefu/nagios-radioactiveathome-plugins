# nukular_tools
radioactive.org auxilary tools which utilize the raw data export `gettrickledata.php`

# scripts
The scripts are working with the radioactiveathome.org api. 
Forum Post: http://radioactiveathome.org/boinc/forum_thread.php?id=60
Exporter:  http://radioactiveathome.org/boinc/gettrickledata.php?start=X&hostid=Y
Output according to icinga guidelines: https://nagios-plugins.org/doc/guidelines.html

# check_geiger

nagios script to check geiger uSV data:
    
    usage: rah-check-geiger [options]

    Options:
        -w --warning <uSv>               Warning level in uSv [default: 0.3]
        -c --critical <uSv>              Critical level in uSv [default: 0.8]
        -h --hostid <id>                 Host Identity in radioactiveathome [default: 14364]
        -u --url <URL>                  radioactivehome trickledata [default: http://radioactiveathome.org/boinc/gettrickledata.php]


    $ python rah-check-geiger
    radiation OK at 0.106uSv/h - below 0.3uSv/h
    <- exit code 0
    $ python rah-check-geiger -w 0.01
    radiation WARNING at 0.106uSv/h - above 0.01uSv/h
    <- exit code 1
    $ python rah-check-geiger -c 0.01
    radiation CRITICAL at 0.106uSv/h - above 0.01uSv/h
    <- exit code 2


# check_geiger_last_data

nagios script to check geiger trickledata last entry

    usage: check_geiger_last_data [options]

    Options:
        -w --warning <hours>            Warning threshold for hours since last data entry [default: 24]
        -c --critical <hours>           Warning threshold for hours since last data entry [default: 72]
        -h --hostid <id>                Host Identity in radioactiveathome [default: 14364]
        -u --url <URL>                  radioactivehome trickledata [default: http://radioactiveathome.org/boinc/gettrickledata.php]


    $ python rah-check-geiger-last-data 
    radiation timeout OK - last data 126 minutes ago
    <- exit code 0
    $ python rah-check-geiger-last-data -w 1
    radiation timeout WARNING - no data since 2 hours
    <- exit code 1
    $ python rah-check-geiger-last-data -c 1
    radiation timeout CRITICAL  - no data since 2 hours
    <- exit code 2

## legacy/current_geiger.sh
returns the uSV value of the last data point

## legacy/last_data.sh
returns the seconds since the last data entry
