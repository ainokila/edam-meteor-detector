#!/bin/bash

if [[ $EUID -ne 0 ]]; then
    echo "This setup script must be run as root" 1>&2
    exit 1
fi

apt-add-repository ppa:mutlaqja/ppa -y
apt-get update -y

# Requirements for PyIndi
# https://indilib.org/support/tutorials/166-installing-and-using-the-python-pyndi-client-on-raspberry-pi.html
PYINDI_REQ="python-setuptools python-dev swig libz3-dev libcfitsio-dev libnova-dev"
echo "[+] Installing dependencies for PyIndi..."
apt-get install -y $PYINDI_REQ

# Install indi-full
# https://indilib.org/download.html
INDI_REQ="indi-full gsc kstars-bleeding libindi1 indi-bin libindi-dev"
echo "[+] Installing Indi and kstars"
apt-get install -y $INDI_REQ 

# Install pip3
echo "[+] Installing pip3"
apt-get install -y python3-pip

# QHY5 SDK Install
echo "[+] Installing QHY5 controller"
QHY5_PATH="./sdk_linux64_20.08.26.tgz"
QHY5_EXTRACT="./qhy5"
curl -X GET https://www.qhyccd.com/file/repository/publish/SDK/200826/sdk_linux64_20.08.26.tgz --output $QHY5_PATH
tar -xvzf $QHY5_PATH
cd sdk_linux64_20.08.26
chmod 700 ./install.sh
./install.sh