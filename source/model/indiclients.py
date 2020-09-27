#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import time
import logging
import PyIndi

from datetime import datetime
from io import BytesIO
import threading


class CCDClient(PyIndi.BaseClient):

    device = None
    logger = logging.getLogger('PyQtIndi.IndiClient')

    def __init__(self, device_name, exposure_time=1.0):
        super(CCDClient, self).__init__()
        self.blob_event = threading.Event()
        self.device_name = device_name
        self.exposure_time = exposure_time
        self.blob = None

    def newDevice(self, d):
        self.logger.debug("new device " + d.getDeviceName())
        if d.getDeviceName() == self.device_name:
            self.logger.debug("Set new device %s", self.device_name)
            # save reference to the device in member variable
            self.device = d

    def newProperty(self, p):
        self.logger.debug("new property "+ p.getName() + " for device "+ p.getDeviceName())
        if self.device is not None and p.getName() == "CONNECTION" and p.getDeviceName() == self.device.getDeviceName():
            self.logger.debug("Got property CONNECTION for CCD")
            # connect to device
            self.connectDevice(self.device.getDeviceName())
            # set BLOB mode to BLOB_ALSO
            self.setBLOBMode(1, self.device.getDeviceName(), None)


    def removeProperty(self, p):
        self.logger.info("remove property " + p.getName() +
                         " for device " + p.getDeviceName())

    def newBLOB(self, bp):
        # get image data
        img = bp.getblobdata()

        # write image data to BytesIO buffer
        self.blob = BytesIO(img)
        self.blob_event.set()

    def newSwitch(self, svp):
        self.logger.debug("new Switch " + svp.name +
                         " for device " + svp.device)

    def newNumber(self, nvp):
        # self.logger.info("new Number "+ nvp.name + " for device "+ str(nvp.device))
        pass

    def newText(self, tvp):
        self.logger.debug("new Text " + tvp.name + " for device " + tvp.device)

    def newLight(self, lvp):
        self.logger.debug("new Light " + lvp.name + " for device " + lvp.device)

    def newMessage(self, d, m):
        self.logger.debug("new Message "+ d.messageQueue(m))

    def serverConnected(self):
        self.logger.info("Server connected ("+self.getHost()+":"+str(self.getPort())+")")

    def serverDisconnected(self, code):
        self.logger.info("Server disconnected (exit code = "+str(code) +
                         ","+str(self.getHost())+":"+str(self.getPort())+")")

    def takeExposure(self):

        self.logger.info(
            "Request a new exposure using %s seconds", self.exposure_time)

        # get current exposure time
        exp = self.device.getNumber("CCD_EXPOSURE")

        while(not exp):
            exp = self.device.getNumber("CCD_EXPOSURE")

        if exp:
            # set exposure time
            exp[0].value = self.exposure_time
            # send new exposure time to server/device
            self.sendNewNumber(exp)
            self.blob_event.wait()
            self.blob_event.clear()
