#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
import signal
import time
import logging
import PyIndi
import cv2
import argparse

from multiprocessing import Process, Pipe

from source.model.indiclients import CCDClient
from source.model.image.fits import ImageFits
from source.model.analyzer import ImageAnalyzer

logging.basicConfig(format='%(asctime)s %(message)s', level=logging.INFO)

# Create the parser
args_parser = argparse.ArgumentParser(
    description='Client interface to control a CCD camera', 
    allow_abbrev=False)

# Arguments
args_parser.add_argument('--host', default='localhost', action='store', type=str)
args_parser.add_argument('--port', default=7624, action='store', type=int)
args_parser.add_argument('--ccd_device_name', default='QHY CCD QHY5-M-', action='store', type=str)
args_parser.add_argument('--ccd_exposition', default=1, action='store', type=int)
args_parser.add_argument('--ccd_gain', default=50, action='store', type=int)

stop = False
analyzer = None

def term_signal(signum, frame):
    global stop
    global analyzer
    analyzer.stop.set()
    stop = True

# Signal handlers
signal.signal(signal.SIGTERM, term_signal)
signal.signal(signal.SIGINT, term_signal)

args = args_parser.parse_args()

server_host = args.host
server_port = args.port
ccd_device_name = args.ccd_device_name
ccd_exposition = args.ccd_exposition
ccd_gain = args.ccd_gain

consumer, producer = Pipe()

# instantiate the client
ccd_client = CCDClient(device_name=ccd_device_name,
                       exposure_time=ccd_exposition,
                       gain=ccd_gain,
                       pipe=producer)

analyzer = ImageAnalyzer(consumer_pipe=consumer)

# set indi server localhost and port
ccd_client.setServer(server_host, server_port)

# connect to indi server
print("Connecting to indiserver")
if (not(ccd_client.connectServer())):
    print("No indiserver running on "+ccd_client.getHost() +
          ":"+str(ccd_client.getPort())+" - Try to run")
    sys.exit(1)

analyzer.start()
ccd_client.setBLOBMode(1, ccd_device_name, None)

while not stop:
    time.sleep(1)
