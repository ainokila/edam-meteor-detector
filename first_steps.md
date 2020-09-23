# Download SDK for QHY5 Camera

Url sdk: https://www.qhyccd.com/download.html
Install: 
```
chmod +x install.sh
sudo ./install.sh
```

Configure the rules for the device in usb rules:
File: /etc/udev/rules.d/85-qhyccd.rules
```
ACTION=="add", SUBSYSTEM=="usb", ATTRS{idVendor}=="16c0", ATTRS{idProduct}=="296a", RUN+="/sbin/fxload -t fx2 -I /lib/firmware/qhy/QHY5.HEX -D $env{DEVNAME} -s /lib/firmware/qhy/QHY5LOADER.HEX"
```

# Install INDI Server and Kstars client

URL: https://indilib.org/download.html
Steps:
```
sudo apt-add-repository ppa:mutlaqja/ppa
sudo apt-get update

sudo apt-get install indi-full gsc
sudo apt-get install indi-full kstars-bleeding
```

# Create the firt client using Python3.x
URL: https://indilib.org/support/tutorials/166-installing-and-using-the-python-pyndi-client-on-raspberry-pi.html

## Install PyIndi
```
sudo apt-get install python-setuptools python-dev libindi-dev swig libz3-dev libcfitsio-dev libnova-dev
sudo apt-get install g++
sudo apt-get install python3.6-dev
```