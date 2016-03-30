#!/usr/bin/env python

import argparse
import requests
import json
from datetime import datetime
from myconfig import API_KEY

url = 'http://bustime.mta.info/api/siri/stop-monitoring.json'

parser = argparse.ArgumentParser(description='Get info on busses')

parser.add_argument('-s',
    dest = 'stop',
    action = 'store',
    default = '404137',
    help = 'The bus stop ID code')

args = parser.parse_args()

keys = {'key' : API_KEY, 'OperatorRef' : 'MTA', 'MonitoringRef' : args.stop}

bus_data_raw = requests.get(url, params=keys)
bus_data = bus_data_raw.json()

stop_name = bus_data['Siri']['ServiceDelivery']['StopMonitoringDelivery'][0]['MonitoredStopVisit'][0]['MonitoredVehicleJourney']['MonitoredCall']['StopPointName']
dest_name = bus_data['Siri']['ServiceDelivery']['StopMonitoringDelivery'][0]['MonitoredStopVisit'][0]['MonitoredVehicleJourney']['DestinationName']
results = len(bus_data['Siri']['ServiceDelivery']['StopMonitoringDelivery'][0]['MonitoredStopVisit']) 

print "There are %d busses en route to stop %s heading to %s:" % (results, stop_name, dest_name)

for b in bus_data['Siri']['ServiceDelivery']['StopMonitoringDelivery'][0]['MonitoredStopVisit']:
  try:
    ugly_time = b['MonitoredVehicleJourney']['MonitoredCall']['ExpectedArrivalTime']
    arriv_time = datetime.strptime(ugly_time[0:19], '%Y-%m-%dT%H:%M:%S')
    distance = b['MonitoredVehicleJourney']['MonitoredCall']['Extensions']['Distances']['PresentableDistance']
    print "%s arriving approximately %s" % (distance, arriv_time)
  except:
    distance = b['MonitoredVehicleJourney']['MonitoredCall']['Extensions']['Distances']['PresentableDistance']
    print "%s (no ETA available)" % distance

