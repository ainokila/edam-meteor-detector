#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
import signal
import time
import logging
import PyIndi
import cv2
import argparse
import os
import json

from multiprocessing import Process, Pipe

from source.model.indiclients import CCDClient
from source.model.image.fits import ImageFits
from source.model.analyzer import ImageAnalyzer
from source.model.config.ccd import CCDConfig
from source.utils.variables import CLIENT_CONFIG_PATH, ANALYZER_CONFIG_PATH

logging.basicConfig(format='%(asctime)s %(message)s', level=logging.INFO)
logger = logging.getLogger('Client')

# Create the parser
args_parser = argparse.ArgumentParser(
    description='Client interface to control a CCD camera', 
    allow_abbrev=False)

# Arguments
args_parser.add_argument('--host', default='localhost', action='store', type=str)
args_parser.add_argument('--port', default=7624, action='store', type=int)

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

ccd_config = CCDConfig.create_from_file(CLIENT_CONFIG_PATH)

args = args_parser.parse_args()

server_host = args.host
server_port = args.port
consumer, producer = Pipe()

# instantiate the client
ccd_client = CCDClient(device_name=ccd_config.device_name,
                       exposure_time=ccd_config.exposure_time,
                       gain=ccd_config.gain,
                       pipe=producer)
logger.info("Created client with the following properties:\n\t %s", ccd_config)


analyzer = ImageAnalyzer(consumer_pipe=consumer)

# set indi server localhost and port
ccd_client.setServer(server_host, server_port)

# connect to indi server
logger.info("Connecting to indiserver host %s port %s", ccd_client.getHost(), ccd_client.getPort())
if (not(ccd_client.connectServer())):
    logger.error("No connection to server - Aborted.")
    sys.exit(-1)

analyzer.start()
ccd_client.setBLOBMode(1, ccd_config.device_name, None)

while not stop:

    time.sleep(1)
    ccd_config_new = CCDConfig.create_from_file(CLIENT_CONFIG_PATH)

    if hash(ccd_config_new) != hash(ccd_config):
        logger.info("Detected a change in the configuration for ccd client")
        ccd_config = ccd_config_new

        ccd_client.update_exposure_time(ccd_config.exposure_time)
        ccd_client.update_gain(ccd_config.gain)
