import PyIndi
import time
import sys
import threading
    
class IndiClient(PyIndi.BaseClient):
    def __init__(self):
        self.camera = None
        super(IndiClient, self).__init__()
    def newDevice(self, d):
        print("Recibo nuevo dispositivo: ", d.getProperties())
        self.camera = d
        pass
    def newProperty(self, p):
        pass
    def removeProperty(self, p):
        pass
    def newBLOB(self, bp):
        global blobEvent
        print("new BLOB ", bp.name)
        blobEvent.set()
        pass
    def newSwitch(self, svp):
        pass
    def newNumber(self, nvp):
        pass
    def newText(self, tvp):
        pass
    def newLight(self, lvp):
        pass
    def newMessage(self, d, m):
        pass
    def serverConnected(self):
        pass
    def serverDisconnected(self, code):
        pass


# connect the server
indiclient=IndiClient()
print("Intento")
indiclient.setServer("localhost", 7624)
print("Conecto")

if (not(indiclient.connectServer())):
     print("No indiserver running on "+indiclient.getHost()+":"+str(indiclient.getPort())+" - Try to run")
     print("  indiserver indi_simulator_telescope indi_simulator_ccd")
     sys.exit(1)

# Let's take some pictures
ccd="QHY CCD QHY5-M-"
print("Devices " + str(indiclient.getDevices()))
device_ccd=indiclient.getDevice(ccd)
while not(device_ccd):
    time.sleep(0.5)
    device_ccd=indiclient.getDevice(ccd)    

ccd_connect=device_ccd.getSwitch("CONNECTION")
while not(ccd_connect):
    time.sleep(0.5)
    ccd_connect=device_ccd.getSwitch("CONNECTION")

if not(device_ccd.isConnected()):
    ccd_connect[0].s=PyIndi.ISS_ON  # the "CONNECT" switch
    ccd_connect[1].s=PyIndi.ISS_OFF # the "DISCONNECT" switch
    indiclient.sendNewSwitch(ccd_connect)

print("Devices " + str(indiclient.getDevices()))

ccd_exposure=device_ccd.getNumber("CCD_EXPOSURE")
while not(ccd_exposure):
    time.sleep(0.5)
    ccd_exposure=device_ccd.getNumber("CCD_EXPOSURE")

# we should inform the indi server that we want to receive the
# "CCD1" blob from this device
indiclient.setBLOBMode(PyIndi.B_ALSO, ccd, "CCD1")

ccd_ccd1=device_ccd.getBLOB("CCD1")
while not(ccd_ccd1):
    time.sleep(0.5)
    ccd_ccd1=device_ccd.getBLOB("CCD1")

# a list of our exposure times
exposures=[1.0, 2.0]

# we use here the threading.Event facility of Python
# we define an event for newBlob event
blobEvent=threading.Event()
blobEvent.clear()
i=0
ccd_exposure[0].value=exposures[i]
indiclient.sendNewNumber(ccd_exposure)
while (i < len(exposures)):
    # wait for the ith exposure
    blobEvent.wait()
    # we can start immediately the next one
    if (i + 1 < len(exposures)):
        ccd_exposure[0].value=exposures[i+1]
        blobEvent.clear()
        indiclient.sendNewNumber(ccd_exposure)
    # and meanwhile process the received one
    for blob in ccd_ccd1:
        print("name: ", blob.name," size: ", blob.size," format: ", blob.format)
        # pyindi-client adds a getblobdata() method to IBLOB item
        # for accessing the contents of the blob, which is a bytearray in Python
        fits=blob.getblobdata()
        print("fits data type: ", type(fits))
        # here you may use astropy.io.fits to access the fits data
        # and perform some computations while the ccd is exposing
        # but this is outside the scope of this tutorial
    i+=1
    

