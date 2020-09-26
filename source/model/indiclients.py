#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys, time, logging
import PyIndi

from source.utils.image.formats import fits_to_jpg
from datetime import datetime
from PIL import Image
from io import BytesIO
  
class CCDClient(PyIndi.BaseClient):
 
    device = None
    exposure_time = 1.0
 
    def __init__(self, device_name, exposure_time=1.0):
        super(CCDClient, self).__init__()
        self.logger = logging.getLogger('PyQtIndi.IndiClient')
        self.exposure_time = exposure_time
        self.device_name = device_name

    def newDevice(self, d):
        self.logger.info("new device " + d.getDeviceName())
        if d.getDeviceName() == self.device_name:
            self.logger.info("Set new device %s", self.device_name)
            # save reference to the device in member variable
            self.device = d

    def newProperty(self, p):
        # self.logger.info("new property "+ p.getName() + " for device "+ p.getDeviceName())
        if self.device is not None and p.getName() == "CONNECTION" and p.getDeviceName() == self.device.getDeviceName():
            self.logger.info("Got property CONNECTION for CCD")
            # connect to device
            self.connectDevice(self.device.getDeviceName())
            # set BLOB mode to BLOB_ALSO
            self.setBLOBMode(1, self.device.getDeviceName(), None)
        if p.getName() == "CCD_EXPOSURE":
            # take first exposure
            self.takeExposure()

    def removeProperty(self, p):
        self.logger.info("remove property "+ p.getName() + " for device "+ p.getDeviceName())

    def newBLOB(self, bp):
        # get image data
        img = bp.getblobdata()
        # write image data to BytesIO buffer

        blobfile = BytesIO(img)
        # open a file and save buffer to disk

        fitsfilename = "data/image-%s.fit" % (datetime.now().strftime("%m-%d-%Y-%H:%M:%S"))
        with open(fitsfilename, "wb") as f:
            f.write(blobfile.getvalue())

        self.logger.info("New image %s", fitsfilename)

        # data = fits_to_jpg(fitsfilename)

        # # Create image from data array and save as jpg
        # image = Image.fromarray(data, 'L')
        # imagename = fitsfilename.replace('.fits', '.jpg')
        # image.save(imagename)

        # start new exposure
        self.takeExposure()

    def newSwitch(self, svp):
        self.logger.info("new Switch "+ svp.name + " for device "+ svp.device)

    def newNumber(self, nvp):
        # self.logger.info("new Number "+ nvp.name + " for device "+ str(nvp.device))
        pass

    def newText(self, tvp):
        self.logger.info("new Text "+ tvp.name + " for device "+ tvp.device)

    def newLight(self, lvp):
        self.logger.info("new Light "+ lvp.name + " for device "+ lvp.device)

    def newMessage(self, d, m):
        #self.logger.info("new Message "+ d.messageQueue(m))
        pass

    def serverConnected(self):
        print("Server connected ("+self.getHost()+":"+str(self.getPort())+")")

    def serverDisconnected(self, code):
        self.logger.info("Server disconnected (exit code = "+str(code)+","+str(self.getHost())+":"+str(self.getPort())+")")

    def takeExposure(self):

        self.logger.info("Request a new exposure using %s seconds", self.exposure_time)

        #get current exposure time
        exp = self.device.getNumber("CCD_EXPOSURE")
        # set exposure time
        exp[0].value = self.exposure_time
        # send new exposure time to server/device
        self.sendNewNumber(exp)