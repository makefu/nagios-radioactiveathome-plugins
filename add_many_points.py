#!/usr/bin/env python
""" RadioactiveAtHome check geiger uSv 

usage: rah-check-geiger [options] [loop [TIMEOUT]]

Options:
    -h --hostid <id>        Host Identity in radioactiveathome [default: 14364]
    -u --url <URL>          radioactivehome trickledata [default: http://radioactiveathome.org/boinc/gettrickledata.php]
    --carbon-host <HOST>    the carbon host [default: heidi.shack]
    --carbon-port <PORT>    the carbon port [default: 2003]
    --back <NUM>            the number of datapoints we should check in the past [default: 1000000]

if using loop mode the TIMEOUT defines the number of minutes between fetching points

"""



def send_all_data(sensor,kv):
    import socket
    data=""
    now=datetime.now()
    sock = socket.socket()
    for value,ts in kv:
        data+="sensors.radiation.{} {} {}\n".format(sensor,value,ts)
    sock.connect((CARBON_HOST, CARBON_PORT))
    print(data.strip())
    sock.sendall(data.encode())
    sock.close()

def sensor_to_graphite(sensor,value,ts):
    import socket
    now=datetime.now()
    sock = socket.socket()
    data="sensors.radiation.{} {} {}\n".format(sensor,value,ts)
    sock.connect((CARBON_HOST, CARBON_PORT))
    print(data.strip())
    sock.sendall(data.encode())
    sock.close()
    return

def fetch_live_data(url,hostid)
    payload = {'hostid':hostid}
    try:
        ret = requests.get(url,params=payload)
        current_data_field = int(ret.text.split('\n')[0].split(':')[1])
        payload['start'] =current_data_field - backwards
        all_data= requests.get(url,params=payload).text.split('\n')[1:-1]
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

if __name__ == "__main__":
    args = docopt(__doc__)
    hostid = args['--hostid']
    backwards= int(args['--back'])
    url = args['--url']
    CARBON_HOST = args['--carbon-host']
    CARBON_PORT = int(args['--carbon-port'])
    loop = args['loop']
    timeout = int( args['TIMEOUT'] or 10) * 60
    while loop:
        begin = time.clock()
        try:
            send_all_data(1,list(fetch_live_data(url,hostid)))
        except:
            print("unable to fetch live data")
        sleeptime = timeout - time.clock() + begin
        print("sleeping for {} minutes".format(sleeptime/60)
        time.sleep()
    else:
        send_all_data(1,list(fetch_live_data(url,hostid)))
