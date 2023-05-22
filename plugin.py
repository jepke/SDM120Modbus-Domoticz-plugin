#!/usr/bin/env python
"""
Eastron SDM630-ModbusV2 Smart Meter Three Phase Electrical System. The Python plugin for Domoticz
Original author: MFxMF,  bbossink, remocovanvugt
Modified by: Jepke
Requirements: 
    1.python module minimalmodbus -> http://minimalmodbus.readthedocs.io/en/master/
        (pi@raspberrypi:~$ sudo pip3 install minimalmodbus)
    2.Communication module Modbus USB to RS485 converter module
"""
"""
<plugin key="SDM630ModbusV2" name="Eastron SDM630-ModbusV2" version="2.0.0" author="Jepke">
    <params>
        <param field="SerialPort" label="Modbus Port" width="200px" required="true" default="/dev/ttyUSB0" />
        <param field="Mode1" label="Baud rate" width="40px" required="true" default="9600"  />
        <param field="Mode2" label="Device ID" width="40px" required="true" default="1" />
        <param field="Mode3" label="Reading Interval min." width="40px" required="true" default="1" />
        <param field="Mode6" label="Debug" width="75px">
            <options>
                <option label="True" value="Debug"/>
                <option label="False" value="Normal"  default="true" />
            </options>
        </param>
    </params>
</plugin>

"""

import minimalmodbus
import serial
import Domoticz


class BasePlugin:
    def __init__(self):
        self.runInterval = 1
        self.rs485 = "" 
        return

    def onStart(self):
        self.rs485 = minimalmodbus.Instrument(Parameters["SerialPort"], int(Parameters["Mode2"]))
        self.rs485.serial.baudrate = Parameters["Mode1"]
        self.rs485.serial.bytesize = 8
        self.rs485.serial.parity = minimalmodbus.serial.PARITY_NONE
        self.rs485.serial.stopbits = 1
        self.rs485.serial.timeout = 1
        self.rs485.debug = False
                          

        self.rs485.mode = minimalmodbus.MODE_RTU
        devicecreated = []
        Domoticz.Log("Eastron SDM630 Modbus V2 plugin start")
        self.runInterval = int(Parameters["Mode3"]) * 1 
       
        if 1 not in Devices:
            Domoticz.Device(Name="Voltage_L1", Unit=1,TypeName="Voltage",Used=0).Create()
        if 2 not in Devices:
            Domoticz.Device(Name="Voltage_L2", Unit=2,TypeName="Voltage",Used=0).Create()
        if 3 not in Devices:
            Domoticz.Device(Name="Voltage_L3", Unit=3,TypeName="Voltage",Used=0).Create()
        Options = { "Custom" : "1;A"}
        if 4 not in Devices:
            Domoticz.Device(Name="Current_L1", Unit=4,TypeName="Custom",Used=0,Options=Options).Create()
        if 5 not in Devices:
            Domoticz.Device(Name="Current_L2", Unit=5,TypeName="Custom",Used=0,Options=Options).Create()
        if 6 not in Devices:
            Domoticz.Device(Name="Current_L3", Unit=6,TypeName="Custom",Used=0,Options=Options).Create()
        if 7 not in Devices:
            Domoticz.Device(Name="Power_L1", Unit=7,TypeName="Usage",Used=0).Create()
        if 8 not in Devices:
            Domoticz.Device(Name="Power_L2", Unit=8,TypeName="Usage",Used=0).Create()
        if 9 not in Devices:
            Domoticz.Device(Name="Power_L3", Unit=9,TypeName="Usage",Used=0).Create()
        Options = { "Custom" : "1;VA"}
        if 10 not in Devices:
            Domoticz.Device(Name="Apparent_Power_L1", Unit=10,TypeName="Custom",Used=0,Options=Options).Create()
        if 11 not in Devices:
            Domoticz.Device(Name="Apparent_Power_L2", Unit=11,TypeName="Custom",Used=0,Options=Options).Create()
        if 12 not in Devices:
            Domoticz.Device(Name="Apparent_Power_L3", Unit=12,TypeName="Custom",Used=0,Options=Options).Create()
        Options = { "Custom" : "1;VAr"}
        if 13 not in Devices:
            Domoticz.Device(Name="Reactive_Power_L1", Unit=13,TypeName="Custom",Used=0,Options=Options).Create()
        if 14 not in Devices:
            Domoticz.Device(Name="Reactive_Power_L2", Unit=14,TypeName="Custom",Used=0,Options=Options).Create()
        if 15 not in Devices:
            Domoticz.Device(Name="Reactive_Power_L3", Unit=15,TypeName="Custom",Used=0,Options=Options).Create()
        Options = { "Custom" : "1;PF"}
        if 16 not in Devices:
            Domoticz.Device(Name="Power_Factor_L1", Unit=16,TypeName="Custom",Used=0,Options=Options).Create()
        if 17 not in Devices:
            Domoticz.Device(Name="Power_Factor_L2", Unit=17,TypeName="Custom",Used=0,Options=Options).Create()
        if 18 not in Devices:
            Domoticz.Device(Name="Power_Factor_L3", Unit=18,TypeName="Custom",Used=0,Options=Options).Create()
        Options = { "Custom" : "1;°"}
        if 19 not in Devices:
            Domoticz.Device(Name="Phase_Angle_L1", Unit=19,TypeName="Custom",Used=0,Options=Options).Create()
        if 20 not in Devices:
            Domoticz.Device(Name="Phase_Angle_L2", Unit=20,TypeName="Custom",Used=0,Options=Options).Create()
        if 21 not in Devices:
            Domoticz.Device(Name="Phase_Angle_L3", Unit=21,TypeName="Custom",Used=0,Options=Options).Create()
        if 22 not in Devices:
            Domoticz.Device(Name="Average_Voltage_To_Neutral", Unit=22,TypeName="Voltage",Used=0).Create()
        Options = { "Custom" : "1;A"}
        if 23 not in Devices:
            Domoticz.Device(Name="Average_Line_Current", Unit=23,TypeName="Custom",Used=0,Options=Options).Create()
        if 24 not in Devices:
            Domoticz.Device(Name="Sum_Line_Current", Unit=24,TypeName="Custom",Used=0,Options=Options).Create()
        if 25 not in Devices:
            Domoticz.Device(Name="Total_System_Power", Unit=25,TypeName="Usage",Used=0).Create()
        Options = { "Custom" : "1;VA"}
        if 26 not in Devices:
            Domoticz.Device(Name="Total_System_Apparent_Power", Unit=26,TypeName="Custom",Used=0,Options=Options).Create()

               
    def onStop(self):
        Domoticz.Log("Eastron SDM630Modbus plugin stop")

    def onHeartbeat(self):
        self.runInterval -=1;
        if self.runInterval <= 0:
            # Get data from SDM72D
            Voltage_L1 = self.rs485.read_float(0, functioncode=4, numberOfRegisters=2)
            Voltage_L2 = self.rs485.read_float(2, functioncode=4, numberOfRegisters=2)
            Voltage_L3 = self.rs485.read_float(4, functioncode=4, numberOfRegisters=2)
            Current_L1 = self.rs485.read_float(6, functioncode=4, numberOfRegisters=2)
            Current_L2 = self.rs485.read_float(8, functioncode=4, numberOfRegisters=2)
            Current_L3 = self.rs485.read_float(10, functioncode=4, numberOfRegisters=2)
            Power_L1 = self.rs485.read_float(12, functioncode=4, numberOfRegisters=2)
            Power_L2 = self.rs485.read_float(14, functioncode=4, numberOfRegisters=2)
            Power_L3 = self.rs485.read_float(16, functioncode=4, numberOfRegisters=2)
            Apparent_Power_L1 = self.rs485.read_float(18, functioncode=4, numberOfRegisters=2)
            Apparent_Power_L2 = self.rs485.read_float(20, functioncode=4, numberOfRegisters=2)
            Apparent_Power_L3 = self.rs485.read_float(22, functioncode=4, numberOfRegisters=2)
            Reactive_Power_L1 = self.rs485.read_float(24, functioncode=4, numberOfRegisters=2)
            Reactive_Power_L2 = self.rs485.read_float(26, functioncode=4, numberOfRegisters=2)
            Reactive_Power_L3 = self.rs485.read_float(28, functioncode=4, numberOfRegisters=2)
            Power_Factor_L1 = self.rs485.read_float(30, functioncode=4, numberOfRegisters=2)
            Power_Factor_L2 = self.rs485.read_float(32, functioncode=4, numberOfRegisters=2)
            Power_Factor_L3 = self.rs485.read_float(34, functioncode=4, numberOfRegisters=2)
            Phase_Angle_L1 = self.rs485.read_float(36, functioncode=4, numberOfRegisters=2)
            Phase_Angle_L2 = self.rs485.read_float(38, functioncode=4, numberOfRegisters=2)
            Phase_Angle_L3 = self.rs485.read_float(40, functioncode=4, numberOfRegisters=2)
            Average_Voltage_To_Neutral = self.rs485.read_float(42, functioncode=4, numberOfRegisters=2)
            Average_Line_Current = self.rs485.read_float(46, functioncode=4, numberOfRegisters=2)
            Sum_Line_Current = self.rs485.read_float(48, functioncode=4, numberOfRegisters=2)
            Total_System_Power = self.rs485.read_float(52, functioncode=4, numberOfRegisters=2)
            Total_System_Apparent_Power = self.rs485.read_float(56, functioncode=4, numberOfRegisters=2)
            
            #Update devices
            Devices[1].Update(0,str(Voltage_L1))
            Devices[2].Update(0,str(Voltage_L2))
            Devices[3].Update(0,str(Voltage_L3))
            Devices[4].Update(0,str(round(Current_L1, 3)))
            Devices[5].Update(0,str(round(Current_L2, 3)))
            Devices[6].Update(0,str(round(Current_L3, 3)))
            Devices[7].Update(0,str(round(Power_L1, 3)))
            Devices[8].Update(0,str(round(Power_L2, 3)))
            Devices[9].Update(0,str(round(Power_L3, 3)))
            Devices[10].Update(0,str(Apparent_Power_L1))
            Devices[11].Update(0,str(Apparent_Power_L2))
            Devices[12].Update(0,str(Apparent_Power_L3))
            Devices[13].Update(0,str(Reactive_Power_L1))
            Devices[14].Update(0,str(Reactive_Power_L2))
            Devices[15].Update(0,str(Reactive_Power_L3))
            Devices[16].Update(0,str(Power_Factor_L1))
            Devices[17].Update(0,str(Power_Factor_L2))
            Devices[18].Update(0,str(Power_Factor_L3))
            Devices[19].Update(0,str(Phase_Angle_L1))
            Devices[20].Update(0,str(Phase_Angle_L2))
            Devices[21].Update(0,str(Phase_Angle_L3))
            Devices[22].Update(0,str(Average_Voltage_To_Neutral))
            Devices[23].Update(0,str(Average_Line_Current))
            Devices[24].Update(0,str(Sum_Line_Current))
            Devices[25].Update(0,str(Total_System_Power))
            Devices[25].Update(0,str(Total_System_Apparent_Power))
            
            
            if Parameters["Mode6"] == 'Debug':
                Domoticz.Log("############ Eastron SD630Modbus Data #################")
                Domoticz.Log('Voltage_L1: {0:.3f} V'.format(Voltage_L1))
                Domoticz.Log('Voltage_L2: {0:.3f} V'.format(Voltage_L2))
                Domoticz.Log('Voltage_L3: {0:.3f} V'.format(Voltage_L3))
                Domoticz.Log('Current_L1: {0:.3f} A'.format(Current_L1))
                Domoticz.Log('Current_L2: {0:.3f} A'.format(Current_L2))
                Domoticz.Log('Current_L3: {0:.3f} A'.format(Current_L3))
                Domoticz.Log('Power_L1: {0:.3f} W'.format(Power_L1))
                Domoticz.Log('Power_L2: {0:.3f} W'.format(Power_L2))
                Domoticz.Log('Power_L3: {0:.3f} W'.format(Power_L3))
                Domoticz.Log('Apparent_Power_L1: {0:.3f} VA'.format(Apparent_Power_L1))
                Domoticz.Log('Apparent_Power_L2: {0:.3f} VA'.format(Apparent_Power_L2))
                Domoticz.Log('Apparent_Power_L3: {0:.3f} VA'.format(Apparent_Power_L3))
                Domoticz.Log('Reactive_Power_L1: {0:.3f} VA'.format(Reactive_Power_L1))
                Domoticz.Log('Reactive_Power_L2: {0:.3f} VA'.format(Reactive_Power_L2))
                Domoticz.Log('Reactive_Power_L3: {0:.3f} VA'.format(Reactive_Power_L3))
                Domoticz.Log('Power_Factor_L1: {0:.3f} PF'.format(Power_Factor_L1))
                Domoticz.Log('Power_Factor_L2: {0:.3f} PF'.format(Power_Factor_L2))
                Domoticz.Log('Power_Factor_L3: {0:.3f} PF'.format(Power_Factor_L3))
                Domoticz.Log('Phase_Angle_L1: {0:.3f} °'.format(Phase_Angle_L1))
                Domoticz.Log('Phase_Angle_L2: {0:.3f} °'.format(Phase_Angle_L2))
                Domoticz.Log('Phase_Angle_L3: {0:.3f} °'.format(Phase_Angle_L3))
                Domoticz.Log('Average_Voltage_To_Neutral: {0:.3f} V'.format(Average_Voltage_To_Neutral))
                Domoticz.Log('Average_Line_Current: {0:.3f} A'.format(Average_Line_Current))
                Domoticz.Log('Sum_Line_Current: {0:.3f} A'.format(Sum_Line_Current))
                Domoticz.Log('Total_System_Power: {0:.3f} W'.format(Total_System_Power))
                Domoticz.Log('Total_System_Apparent_Power: {0:.3f} VA'.format(Total_System_Apparent_Power))
            self.runInterval = int(Parameters["Mode3"]) * 6


global _plugin
_plugin = BasePlugin()


def onStart():
    global _plugin
    _plugin.onStart()


def onStop():
    global _plugin
    _plugin.onStop()


def onHeartbeat():
    global _plugin
    _plugin.onHeartbeat()

# Generic helper functions
def DumpConfigToLog():
    for x in Parameters:
        if Parameters[x] != "":
            Domoticz.Debug("'" + x + "':'" + str(Parameters[x]) + "'")
    Domoticz.Debug("Device count: " + str(len(Devices)))
    for x in Devices:
        Domoticz.Debug("Device:           " + str(x) + " - " + str(Devices[x]))
        Domoticz.Debug("Device ID:       '" + str(Devices[x].ID) + "'")
        Domoticz.Debug("Device Name:     '" + Devices[x].Name + "'")
        Domoticz.Debug("Device nValue:    " + str(Devices[x].nValue))
        Domoticz.Debug("Device sValue:   '" + Devices[x].sValue + "'")
        Domoticz.Debug("Device LastLevel: " + str(Devices[x].LastLevel))
    return
