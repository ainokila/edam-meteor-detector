#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
import time
import logging
import PyIndi
import cv2

from multiprocessing import Process, Pipe

from source.model.indiclients import CCDClient
from source.model.image.fits import ImageFits

logging.basicConfig(format='%(asctime)s %(message)s', level=logging.INFO)

server_host = "localhost"
server_port = 7624
#server_host = "192.168.0.26"
#server_port = 7624
device_name = "QHY CCD QHY5-M-"
#device_name = "indi_simulator_ccd"

consumer, producer = Pipe()

# instantiate the client
ccd_client = CCDClient(device_name=device_name, exposure_time=1, gain=10, pipe=producer)

# set indi server localhost and port
ccd_client.setServer(server_host, server_port)

# connect to indi server
print("Connecting to indiserver")
if (not(ccd_client.connectServer())):
    print("No indiserver running on "+ccd_client.getHost() +
          ":"+str(ccd_client.getPort())+" - Try to run")
    sys.exit(1)

ccd_client.setBLOBMode(1, device_name, None)

previous_image = None
while True:
    data = consumer.recv()
    if not previous_image:
        previous_image = ImageFits()
        previous_image.load_data_from_file(data)
    else:
        new_image = ImageFits()
        new_image.load_data_from_file(data)
        diff_image = previous_image.diff(new_image).data[0].data
        cv2.imshow('Viewer', diff_image)
        previous_image = new_image

        # print(fits.HDUList(hdus=[fits.ImageHDU(data=backSub.apply(img2))])[0].data)
        # 
        if cv2.waitKey(1000) & 0xFF == ord('q'):
            exit
        break
