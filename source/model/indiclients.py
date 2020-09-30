#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import time
import logging
from io import StringIO
import PyIndi
import pyfits

from datetime import datetime
from threading import Thread
from io import BytesIO
import threading


class CCDClient(PyIndi.BaseClient):

    device = None
    logger = logging.getLogger('PyQtIndi.IndiClient')

    def __init__(self, device_name, exposure_time=1.0, gain = 15.0):
        super(CCDClient, self).__init__()
        self.blob_event = threading.Event()
        self.device_name = device_name
        self.exposure_time = exposure_time
        self.blob = None
        self.gain = gain
        self.run = True
        self.roi = None

    def newDevice(self, d):
        self.logger.debug("New device " + d.getDeviceName())
        if d.getDeviceName() == self.device_name:
            self.logger.debug("Set new device %s", self.device_name)
            # save reference to the device in member variable
            self.device = d

    def newProperty(self, p):
        self.logger.info("new property "+ p.getName() + " for device "+ p.getDeviceName())
        if p.getName() == "CONNECTION":
            self.connectDevice(self.device.getDeviceName())
        if p.getName() == "CCD_EXPOSURE":
            self.takeExposure()
        if p.getName() == "CCD_GAIN":
            gain = self.device.getNumber("CCD_GAIN")
            gain[0].value = self.gain
            self.sendNewNumber(gain)

    def removeProperty(self, p):
        self.logger.info("remove property " + p.getName() +
                         " for device " + p.getDeviceName())

    def newBLOB(self, bp):
        img = bp.getblobdata()
        ### process data in new Thread
        exposition_time = datetime.now() 
        Thread(target=self.process_image, args=(img, exposition_time,)).start()
        if self.run:
            self.takeExposure()

    def newSwitch(self, svp):
        self.logger.debug("new Switch " + svp.name +
                         " for device " + svp.device)

    def newNumber(self, nvp):
        self.logger.info("new Number "+ nvp.name + " for device "+ str(nvp.device) + " value " + str(nvp.np.value))
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
        self.logger.info("<<<<<<<< Exposure >>>>>>>>>")
        exp = self.device.getNumber("CCD_EXPOSURE")
        exp[0].value = self.exposure_time
        self.sendNewNumber(exp)

    def process_image(self, blobfile, exposition_time):
        fitsfilename = "./data/image-%s" % (exposition_time.strftime("%m-%d-%Y-%H:%M:%S"))
        self.logger.info("New image %s", fitsfilename)
        with open(fitsfilename + '.fit', "wb") as f:
            f.write(blobfile)

        # if True:
        #     blobio=StringIO(blobfile)
        #     hdulist=pyfits.open(fitsfilename)
        #     scidata = hdulist[0].data
        #     if self.roi is not None:
        #         scidata = scidata[self.roi[1]:self.roi[1]+self.roi[3], self.roi[0]:self.roi[0]+self.roi[2]]
        #     hdulist[0].data = scidata
        #     #hdulist.writeto("%s.fit" % datetime.now())
        #     #cv2.imwrite("%s.png" % datetime.now() , scidata)
        #     cv2.imwrite(fitsfilename + '.jpg' , scidata)