# SDM630-Modbus-v2
*This fork is a quick hack off the SDM120 to make it work for the SDM630. Feel free to use the code to make a more clean or even universal Eastron plugin*

SDM630-Modbus-v2 3-fase power meter with RS485 Port modbus RTU plugin for domoticz

Original code by MFxMF for the SDM630-M power meter https://github.com/MFxMF/SDM630-Modbus
Original code by bbossink for the SDM72-D-M power meter https://github.com/bbossink/SDM72D-Modbus-Domoticz-plugin
Original code by remcovanvugt for the SDM120Modbus power meter https://github.com/remcovanvugt/SDM120Modbus-Domoticz-plugin

Installation: <br>
cd ~/domoticz/plugins<br>
git clone https://github.com/jepke/SDM120Modbus-Domoticz-plugin.git <br>
<br>
Configuration: <br>
Select "Eastron SDM630-ModbusV2" in Hardware configuration screen<br>
If needed modify some parameters and click add<br>
Hint: Set reading interval to 0 if you want updates per "heartbeat" of the system (aprox 10s in my case)<br>
<br>
This fork crafted for SDM630 adds every singel register "86"  new devices will be automatically added. Go to devices tab, there you can find them<br>
Don't forget to restart your Domoticz server<br>
Tested on Version: 2023.1
<br><br><br>
Used python modules: <br>
pyserial -> https://pythonhosted.org/pyserial/ <br>
minimalmodbus -> http://minimalmodbus.readthedocs.io<br>
