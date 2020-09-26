#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys, time, logging
import PyIndi

from source.model.indiclient import IndiClient
  
logging.basicConfig(format='%(asctime)s %(message)s', level=logging.INFO)
 
# instantiate the client
indiclient=IndiClient()
# set indi server localhost and port 7624
indiclient.setServer("localhost",7625)
# connect to indi server
print("Connecting to indiserver")
if (not(indiclient.connectServer())):
     print("No indiserver running on "+indiclient.getHost()+":"+str(indiclient.getPort())+" - Try to run")
     print("  indiserver indi_simulator_telescope indi_simulator_ccd")
     sys.exit(1)
  
# start endless loop, client works asynchron in background
while True:
    time.sleep(1)