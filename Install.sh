YC="\033[1;33m"
RC="\033[0;31m"
DC="\033[0m"

echo "${YC}Checking for sudo..."
if [ "$(id -u)" != "0" ]; then
	echo "${RC}ERROR: Please run this script as sudo.${DC}"
	exit 1
fi

echo "${YC}Extracting BCM library...${DC}"
cd Setup
mkdir "BCM"
unzip BCMLibrary.zip -d BCM/

echo "${YC}Installing BCM library...${DC}"
cd BCM
make install

echo "${YC}Installing Python serial library...${DC}"
cd ..
sh InstallSerial.sh

echo "${YC}Installing PiGo Python library...${DC}"
python setup.py install

echo "${YC}De-blacklisting i2c device module...${DC}"
#!/bin/bash
grep '^\w*blacklist i2c-bcm2708\w*$' /etc/modprobe.d/raspi-blacklist.conf > /dev/null && (cp /etc/modprobe.d/raspi-blacklist.conf /etc/modprobe.d/raspi-blacklist.conf.orig && sed 's/^\w*blacklist i2c-bcm2708\w*$/# blacklist i2c-bcm2708/' /etc/modprobe.d/raspi-blacklist.conf.orig > /etc/modprobe.d/raspi-blacklist.conf)
grep '^\w*i2c-dev\w*$' /etc/modules > /dev/null || echo i2c-dev >> /etc/modules

echo "${YC}Installing i2c-tools...${DC}"
apt-get install i2c-tools

echo "${YC}Adding i2c user...${DC}"
adduser pi i2c

cd ..

sudo chown -R pi .


echo "${YC}PiGo library install complete"
echo "Please reboot the Raspberry Pi to apply changes"
echo "${RC}Please follow instructions in the manual to enable "
echo "UART interface if needed${DC}"
