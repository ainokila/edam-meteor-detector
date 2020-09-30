#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import time
import logging
import random
import PyIndi

from PIL import Image
from io import BytesIO


from datetime import datetime
from source.utils.image.formats import fits_to_jpg
from source.model.indiclients import CCDClient

logging.basicConfig(format='%(asctime)s %(message)s', level=logging.INFO)

server_host = "localhost"
server_port = 7624
#server_host = "192.168.0.26"
#server_port = 7624
device_name = "QHY CCD QHY5-M-"
#device_name = "indi_simulator_ccd"

# instantiate the client
ccd_client = CCDClient(device_name=device_name, exposure_time=10, gain=15)

# set indi server localhost and port
ccd_client.setServer(server_host, server_port)

# connect to indi server
print("Connecting to indiserver")
if (not(ccd_client.connectServer())):
    print("No indiserver running on "+ccd_client.getHost() +
          ":"+str(ccd_client.getPort())+" - Try to run")
    sys.exit(1)

ccd_client.setBLOBMode(1, device_name, None)
while True:
    pass

# # start endless loop, client works asynchron in background
# time.sleep(1)
# 
# 
# ccd_client.exposure_time = 15 # random.randrange(1, 5)
# exposition_time = datetime.now() 
# ccd_client.takeExposure()
# fitsfilename = "data/image-%s.fit" % (exposition_time.strftime("%m-%d-%Y-%H:%M:%S"))
# _save_blob(ccd_client.blob, fitsfilename, jpg=False)
# ccd_client.logger.info("New image %s", fitsfilename)