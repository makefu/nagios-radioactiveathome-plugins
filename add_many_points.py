#!/usr/bin/env python
""" RadioactiveAtHome fetch geiger uSv data

usage: rah-check-geiger [options] [loop [TIMEOUT]]

Options:
    -h --hostid <id>        Host Identity in radioactiveathome [default: 14364]
    -u --url <URL>          radioactivehome trickledata [default: http://radioactiveathome.org/boinc/gettrickledata.php]
    --carbon-host <HOST>    the carbon host [default: heidi.shack]
    --carbon-port <PORT>    the carbon port [default: 2003]
    --back <NUM>            the number of datapoints we should check in the past [default: 1000000]

if using loop mode the TIMEOUT defines the number of minutes between fetching points
The backlog does not correlate with the number of total data points for a given
sensor as the api returns the data for all sensors

"""



def send_all_data(sensor,kv,target):
    import socket
    data=""
    now=datetime.now()
    sock = socket.socket()
    for value,ts in kv:
        data+="sensors.radiation.{} {} {}\n".format(sensor,value,ts)
    sock.connect(target)
    print(data.strip())
    sock.sendall(data.encode())
    sock.close()

def fetch_live_data(url,hostid,backwards=1000000):
    payload = {'hostid':hostid}
    try:
        ret = requests.get(url,params=payload)
        current_data_field = int(ret.text.split('\n')[0].split(':')[1])
        payload['start'] = current_data_field - backwards
        all_data = requests.get(url,params=payload).text.split('\n')[1:-1]
    except:
        print("radiation UNKNOWN - cannot retrieve data from {}".format(url))
        raise

    for current_data in all_data:
        current_data = current_data.split(',')
        ticks = float(current_data[2])
        timespan = float(current_data[6])
        now = datetime.strptime(current_data[3]+"+0000","%Y-%m-%d %H:%M:%S%z")
        usv = (( ticks / timespan) / 171.232876)
        yield [usv,int(now.timestamp())]

from docopt import docopt
import requests,csv,sys
from datetime import datetime
import time
if __name__ == "__main__":
    args = docopt(__doc__)
    hostid = args['--hostid']
    backwards= int(args['--back'])
    url = args['--url']
    target = (args['--carbon-host'],int(args['--carbon-port']))
    loop = args['loop']
    timeout = int( args['TIMEOUT'] or 10) * 60
    while loop:
        begin = time.clock()
        try:
            print("Fetching Data")
            kv = list(fetch_live_data(url,hostid,backwards))
            print("sending {} data points to graphite".format(len(kv)))
            send_all_data(1,kv,target)
        except Exception as e:
            print("unable to fetch or relay live data")
            print(e)
        sleeptime = timeout - time.clock() + begin
        print("sleeping for {} minutes".format(sleeptime/60))
        time.sleep(sleeptime)
    else:
        send_all_data(1,list(fetch_live_data(url,hostid,backwards)),target)
