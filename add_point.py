#!/usr/bin/env python
""" RadioactiveAtHome check geiger uSv 

usage: rah-check-geiger [options]

Options:
    -h --hostid <id>        Host Identity in radioactiveathome [default: 14364]
    -u --url <URL>          radioactivehome trickledata [default: http://radioactiveathome.org/boinc/gettrickledata.php]
    --carbon-host <HOST>    the carbon host [default: heidi.shack]
    --carbon-port <PORT>    the carbon port [default: 2003]

"""



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


from docopt import docopt
import requests,csv,sys
from datetime import datetime

if __name__ == "__main__":
    args = docopt(__doc__)
    hostid = args['--hostid']
    url = args['--url']
    CARBON_HOST = args['--carbon-host']
    CARBON_PORT = int(args['--carbon-port'])
    payload = {'hostid':hostid}
    try:
        ret = requests.get(url,params=payload)
        current_data_field = int(ret.text.split('\n')[0].split(':')[1])
        payload['start'] =current_data_field -1
        current_data = requests.get(url,params=payload).text.split('\n')[-2].split(',')
    except:
        print("radiation UNKNOWN - cannot retrieve data from {}".format(url))
        sys.exit(3)
    ticks = float(current_data[2])
    timespan = float(current_data[6])
    now = datetime.strptime(current_data[3]+"+0000","%Y-%m-%d %H:%M:%S%z")
    usv = (( ticks / timespan) / 171.232876)
    sensor_to_graphite(1,usv,int(now.timestamp()))
