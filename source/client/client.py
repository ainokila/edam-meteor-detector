#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys, time, logging, random
import PyIndi

from source.model.indiclients import CCDClient
  
logging.basicConfig(format='%(asctime)s %(message)s', level=logging.INFO)
 
server_host = "localhost"
server_port = 7625
device_name = "QHY CCD QHY5-M-"

# instantiate the client
ccd_client=CCDClient(device_name=device_name, exposure_time=1)

# set indi server localhost and port
ccd_client.setServer(server_host, server_port)


# connect to indi server
print("Connecting to indiserver")
if (not(ccd_client.connectServer())):
     print("No indiserver running on "+ccd_client.getHost()+":"+str(ccd_client.getPort())+" - Try to run")
     sys.exit(1)
  
# start endless loop, client works asynchron in background
while True:
    time.sleep(1)
    ccd_client.exposure_time = random.randrange(1, 5)
