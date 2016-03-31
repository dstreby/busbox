#!/usr/bin/env python3

import argparse
import requests
import json
import time
from datetime import datetime
from myconfig import API_KEY

class Bus_info:
  def __init__(self, monitored_stop_visit):
    try:
      ugly_time = monitored_stop_visit['MonitoredVehicleJourney']['MonitoredCall']['ExpectedArrivalTime']
      arriv_time = datetime.strptime(ugly_time[0:19], '%Y-%m-%dT%H:%M:%S')
      delta_time = arriv_time - datetime.now()
      self.time_wait = int(round((delta_time.total_seconds() / 60)))
      self.distance = monitored_stop_visit['MonitoredVehicleJourney']['MonitoredCall']['Extensions']['Distances']['PresentableDistance']
    except:
      self.time_wait = 'UNKNOWN'
      self.distance = monitored_stop_visit['MonitoredVehicleJourney']['MonitoredCall']['Extensions']['Distances']['PresentableDistance']

class Bus_time:
  def __init__(self, stop_num):
    url = 'http://bustime.mta.info/api/siri/stop-monitoring.json'
    keys = {'key' : API_KEY, 'OperatorRef' : 'MTA', 'MonitoringRef' : stop_num}
    bus_data_raw = requests.get(url, params=keys)
    self.bus_data =  bus_data_raw.json()
    self.stop_name = self.bus_data['Siri']['ServiceDelivery']['StopMonitoringDelivery'][0]['MonitoredStopVisit'][0]['MonitoredVehicleJourney']['MonitoredCall']['StopPointName']
    self.dest_name = self.bus_data['Siri']['ServiceDelivery']['StopMonitoringDelivery'][0]['MonitoredStopVisit'][0]['MonitoredVehicleJourney']['DestinationName']
    self.results = len(self.bus_data['Siri']['ServiceDelivery']['StopMonitoringDelivery'][0]['MonitoredStopVisit']) 


#############################
# Setup Arg Parser          #
#############################

parser = argparse.ArgumentParser(description='Get info on busses')

parser.add_argument('-s',
    dest = 'stop',
    action = 'store',
    default = '404137',
    help = 'The bus stop ID code')
parser.add_argument('-c',
    action = 'store_true',
    help = 'Countdown to next bus')

args = parser.parse_args()

#############################
# Begin actual program      #
#############################
stop_num = args.stop

if args.c:
  try:
    while True:
      bus_time = Bus_time(stop_num)
      bus_info = Bus_info(bus_time.bus_data['Siri']['ServiceDelivery']['StopMonitoringDelivery'][0]['MonitoredStopVisit'][0])
      print("%s arriving in approx %s minutes" % (bus_info.distance, bus_info.time_wait), end='\r')
      time.sleep(60)
  except KeyboardInterrupt:
    print("\nExiting")
else:
  bus_time = Bus_time(stop_num)
  print("There are %d busses en route to stop %s heading to %s:" % (bus_time.results, bus_time.stop_name, bus_time.dest_name))
  for b in bus_time.bus_data['Siri']['ServiceDelivery']['StopMonitoringDelivery'][0]['MonitoredStopVisit']:
    bus_info = Bus_info(b)
    print("%s arriving in approx %s minutes" % (bus_info.distance, bus_info.time_wait))
