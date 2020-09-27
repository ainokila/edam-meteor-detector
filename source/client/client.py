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
server_port = 7625
#server_host = "192.168.0.26"
#server_port = 7624
device_name = "QHY CCD QHY5-M-"

# instantiate the client
ccd_client = CCDClient(device_name=device_name, exposure_time=1)

# set indi server localhost and port
ccd_client.setServer(server_host, server_port)

# connect to indi server
print("Connecting to indiserver")
if (not(ccd_client.connectServer())):
    print("No indiserver running on "+ccd_client.getHost() +
          ":"+str(ccd_client.getPort())+" - Try to run")
    sys.exit(1)


def _save_blob(blobfile, filename, jpg=False):

    with open(filename, "wb") as f:
        f.write(blobfile.getvalue())

    if jpg:
        data = fits_to_jpg(filename)
        # Create image from data array and save as jpg
        # image = Image.fromarray(data, 'L')
        # imagename = filename.replace('.fits', '.jpg')
        # print(image)
        # image.save(imagename)


# start endless loop, client works asynchron in background
while True:

    time.sleep(1)
    ccd_client.exposure_time = 0.1 # random.randrange(1, 5)
    exposition_time = datetime.now() 
    ccd_client.takeExposure()
    fitsfilename = "data/image-%s.fit" % (exposition_time.strftime("%m-%d-%Y-%H:%M:%S"))
    _save_blob(ccd_client.blob, fitsfilename, jpg=False)
    ccd_client.logger.info("New image %s", fitsfilename)
