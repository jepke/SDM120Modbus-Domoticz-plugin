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
        Options = { "Custom" : "1;VAr"}
        if 27 not in Devices:
            Domoticz.Device(Name="Total_System_Reactive_Power", Unit=27,TypeName="Custom",Used=0,Options=Options).Create()
        Options = { "Custom" : "1;PF"}
        if 28 not in Devices:
            Domoticz.Device(Name="Total_Power_Factor", Unit=28,TypeName="Custom",Used=0,Options=Options).Create()
        Options = { "Custom" : "1;°"}
        if 29 not in Devices:
            Domoticz.Device(Name="Total_Phase_Angle", Unit=29,TypeName="Custom",Used=0,Options=Options).Create()
        Options = { "Custom" : "1;Hz"}
        if 30 not in Devices:
            Domoticz.Device(Name="Frequency", Unit=30,TypeName="Custom",Used=0,Options=Options).Create()
        if 31 not in Devices:
            Domoticz.Device(Name="Import_kWh/MWh", Unit=31,TypeName="kWh",Used=0).Create()
        if 32 not in Devices:
            Domoticz.Device(Name="Export_kWh/MWh", Unit=32,TypeName="kWh",Used=0).Create()
        Options = { "Custom" : "1;kVArh"}
        if 33 not in Devices:
            Domoticz.Device(Name="Import_kVArh/MVArh", Unit=33,TypeName="Custom",Used=0,Options=Options).Create()
        if 34 not in Devices:
            Domoticz.Device(Name="Export_kVArh/MVArh", Unit=34,TypeName="Custom",Used=0,Options=Options).Create()
        Options = { "Custom" : "1;kVAh"}
        if 35 not in Devices:
            Domoticz.Device(Name="kVAh", Unit=35,TypeName="Custom",Used=0,Options=Options).Create()
        Options = { "Custom" : "1;kAh"}
        if 36 not in Devices:
            Domoticz.Device(Name="kAh", Unit=36,TypeName="Custom",Used=0,Options=Options).Create()
        if 37 not in Devices:
            Domoticz.Device(Name="Total_System_Power_import", Unit=37,TypeName="Usage",Used=0).Create()
        if 38 not in Devices:
            Domoticz.Device(Name="Max_Total_System_Power_import", Unit=38,TypeName="Usage",Used=0).Create()
        Options = { "Custom" : "1;VA"}
        if 39 not in Devices:
            Domoticz.Device(Name="Total_System_VA_import", Unit=39,TypeName="Custom",Used=0,Options=Options).Create()
        if 40 not in Devices:
            Domoticz.Device(Name="Max_Total_System_VA_import", Unit=40,TypeName="Custom",Used=0,Options=Options).Create()
        Options = { "Custom" : "1;A"}
        if 41 not in Devices:
            Domoticz.Device(Name="Neutral_Current_import", Unit=41,TypeName="Custom",Used=0,Options=Options).Create()
        if 42 not in Devices:
            Domoticz.Device(Name="Max_Neutral_Current_import", Unit=42,TypeName="Custom",Used=0,Options=Options).Create()
        if 43 not in Devices:
            Domoticz.Device(Name="L1_to_L2", Unit=43,TypeName="Voltage",Used=0).Create()
        if 44 not in Devices:
            Domoticz.Device(Name="L2_to_L3", Unit=44,TypeName="Voltage",Used=0).Create()
        if 45 not in Devices:
            Domoticz.Device(Name="L3_to_L1", Unit=45,TypeName="Voltage",Used=0).Create()
        if 46 not in Devices:
            Domoticz.Device(Name="Average_L_to_L", Unit=46,TypeName="Voltage",Used=0).Create()
        Options = { "Custom" : "1;A"}
        if 47 not in Devices:
            Domoticz.Device(Name="Neutral_Current", Unit=47,TypeName="Custom",Used=0,Options=Options).Create()
        if 48 not in Devices:
            Domoticz.Device(Name="L1_N_THD", Unit=48,TypeName="Percentage",Used=0).Create()
        if 49 not in Devices:
            Domoticz.Device(Name="L2_N_THD", Unit=49,TypeName="Percentage",Used=0).Create()
        if 50 not in Devices:
            Domoticz.Device(Name="L3_N_THD", Unit=50,TypeName="Percentage",Used=0).Create()
        if 51 not in Devices:
            Domoticz.Device(Name="L1_Current_THD", Unit=51,TypeName="Percentage",Used=0).Create()
        if 52 not in Devices:
            Domoticz.Device(Name="L1_Current_THD", Unit=52,TypeName="Percentage",Used=0).Create()
        if 53 not in Devices:
            Domoticz.Device(Name="L1_Current_THD", Unit=53,TypeName="Percentage",Used=0).Create()
        if 54 not in Devices:
            Domoticz.Device(Name="Average_L_N_THD", Unit=54,TypeName="Percentage",Used=0).Create()
        if 55 not in Devices:
            Domoticz.Device(Name="Average_L_Current_THD", Unit=55,TypeName="Percentage",Used=0).Create()
        Options = { "Custom" : "1;°"}
        if 56 not in Devices:
            Domoticz.Device(Name="Total_Power_factor_degrees", Unit=56,TypeName="Custom",Used=0,Options=Options).Create()
        Options = { "Custom" : "1;A"}
        if 57 not in Devices:
            Domoticz.Device(Name="L1_Current_import", Unit=57,TypeName="Custom",Used=0,Options=Options).Create()
        if 58 not in Devices:
            Domoticz.Device(Name="L2_Current_import", Unit=58,TypeName="Custom",Used=0,Options=Options).Create()
        if 59 not in Devices:
            Domoticz.Device(Name="L3_Current_import", Unit=59,TypeName="Custom",Used=0,Options=Options).Create()
        if 60 not in Devices:
            Domoticz.Device(Name="Max_L1_Current_import", Unit=60,TypeName="Custom",Used=0,Options=Options).Create()
        if 61 not in Devices:
            Domoticz.Device(Name="Max_L2_Current_import", Unit=61,TypeName="Custom",Used=0,Options=Options).Create()
        if 62 not in Devices:
            Domoticz.Device(Name="Max_L3_Current_import", Unit=62,TypeName="Custom",Used=0,Options=Options).Create()
        if 63 not in Devices:
            Domoticz.Device(Name="L1_L2_THD", Unit=63,TypeName="Percentage",Used=0).Create()
        if 64 not in Devices:
            Domoticz.Device(Name="L2_L3_THD", Unit=64,TypeName="Percentage",Used=0).Create()
        if 65 not in Devices:
            Domoticz.Device(Name="L3_L1_THD", Unit=65,TypeName="Percentage",Used=0).Create()
        if 66 not in Devices:
            Domoticz.Device(Name="Average_L_L_THD", Unit=66,TypeName="Percentage",Used=0).Create()
        if 67 not in Devices:
            Domoticz.Device(Name="Total_active_watts", Unit=67,TypeName="kWh",Used=0).Create()
        Options = { "Custom" : "1;kVArh"}
        if 68 not in Devices:
            Domoticz.Device(Name="Total_reactive_watts", Unit=68,TypeName="Custom",Used=0,Options=Options).Create()
        if 69 not in Devices:
            Domoticz.Device(Name="L1_Import_active", Unit=69,TypeName="kWh",Used=0).Create()
        if 70 not in Devices:
            Domoticz.Device(Name="L2_Import_active", Unit=70,TypeName="kWh",Used=0).Create()
        if 71 not in Devices:
            Domoticz.Device(Name="L3_Import_active", Unit=71,TypeName="kWh",Used=0).Create()
        if 72 not in Devices:
            Domoticz.Device(Name="L1_Export_active", Unit=72,TypeName="kWh",Used=0).Create()
        if 73 not in Devices:
            Domoticz.Device(Name="L2_Export_active", Unit=73,TypeName="kWh",Used=0).Create()
        if 74 not in Devices:
            Domoticz.Device(Name="L3_Export_active", Unit=74,TypeName="kWh",Used=0).Create()
        if 75 not in Devices:
            Domoticz.Device(Name="L1_Total_active", Unit=75,TypeName="kWh",Used=0).Create()
        if 76 not in Devices:
            Domoticz.Device(Name="L2_Total_active", Unit=76,TypeName="kWh",Used=0).Create()
        if 77 not in Devices:
            Domoticz.Device(Name="L3_Total_active", Unit=77,TypeName="kWh",Used=0).Create()
        Options = { "Custom" : "1;kVArh"}
        if 78 not in Devices:
            Domoticz.Device(Name="L1_Import_reactive", Unit=78,TypeName="Custom",Used=0,Options=Options).Create()
        if 79 not in Devices:
            Domoticz.Device(Name="L2_Import_reactive", Unit=79,TypeName="Custom",Used=0,Options=Options).Create()
        if 80 not in Devices:
            Domoticz.Device(Name="L3_Import_reactive", Unit=80,TypeName="Custom",Used=0,Options=Options).Create()
        if 81 not in Devices:
            Domoticz.Device(Name="L1_Export_reactive", Unit=81,TypeName="Custom",Used=0,Options=Options).Create()
        if 82 not in Devices:
            Domoticz.Device(Name="L2_Export_reactive", Unit=82,TypeName="Custom",Used=0,Options=Options).Create()
        if 83 not in Devices:
            Domoticz.Device(Name="L3_Export_reactive", Unit=83,TypeName="Custom",Used=0,Options=Options).Create()
        if 84 not in Devices:
            Domoticz.Device(Name="L1_Total_reactive", Unit=84,TypeName="Custom",Used=0,Options=Options).Create()
        if 85 not in Devices:
            Domoticz.Device(Name="L2_Total_reactive", Unit=85,TypeName="Custom",Used=0,Options=Options).Create()
        if 86 not in Devices:
            Domoticz.Device(Name="L3_Total_reactive", Unit=86,TypeName="Custom",Used=0,Options=Options).Create()

               
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
            Total_System_Reactive_Power = self.rs485.read_float(60, functioncode=4, numberOfRegisters=2)
            Total_Power_Factor = self.rs485.read_float(62, functioncode=4, numberOfRegisters=2)
            Total_Phase_Angle = self.rs485.read_float(66, functioncode=4, numberOfRegisters=2)
            Frequency = self.rs485.read_float(70, functioncode=4, numberOfRegisters=2)
            Import_kWh = self.rs485.read_float(72, functioncode=4, numberOfRegisters=2)
            Export_kWh = self.rs485.read_float(74, functioncode=4, numberOfRegisters=2)
            Import_kVArh = self.rs485.read_float(76, functioncode=4, numberOfRegisters=2)
            Export_kVArh = self.rs485.read_float(78, functioncode=4, numberOfRegisters=2)
            kVAh = self.rs485.read_float(80, functioncode=4, numberOfRegisters=2)
            kAh = self.rs485.read_float(82, functioncode=4, numberOfRegisters=2)
            Total_System_Power_import = self.rs485.read_float(84, functioncode=4, numberOfRegisters=2)
            Max_Total_System_Power_import = self.rs485.read_float(86, functioncode=4, numberOfRegisters=2)
            Total_System_VA_import = self.rs485.read_float(100, functioncode=4, numberOfRegisters=2)
            Max_Total_System_VA_import = self.rs485.read_float(102, functioncode=4, numberOfRegisters=2)
            Neutral_Current_import = self.rs485.read_float(104, functioncode=4, numberOfRegisters=2)
            Max_Neutral_Current_import = self.rs485.read_float(106, functioncode=4, numberOfRegisters=2)
            L1_to_L2 = self.rs485.read_float(200, functioncode=4, numberOfRegisters=2)
            L2_to_L3 = self.rs485.read_float(202, functioncode=4, numberOfRegisters=2)
            L3_to_L1 = self.rs485.read_float(204, functioncode=4, numberOfRegisters=2)
            Average_L_to_L = self.rs485.read_float(206, functioncode=4, numberOfRegisters=2)
            Neutral_Current = self.rs485.read_float(224, functioncode=4, numberOfRegisters=2)
            L1_N_THD = self.rs485.read_float(234, functioncode=4, numberOfRegisters=2)
            L2_N_THD = self.rs485.read_float(236, functioncode=4, numberOfRegisters=2)
            L3_N_THD = self.rs485.read_float(238, functioncode=4, numberOfRegisters=2)
            L1_Current_THD = self.rs485.read_float(240, functioncode=4, numberOfRegisters=2)
            L2_Current_THD = self.rs485.read_float(242, functioncode=4, numberOfRegisters=2)
            L3_Current_THD = self.rs485.read_float(244, functioncode=4, numberOfRegisters=2)
            Average_L_N_THD = self.rs485.read_float(248, functioncode=4, numberOfRegisters=2)
            Average_L_Current_THD = self.rs485.read_float(250, functioncode=4, numberOfRegisters=2)
            Total_Power_factor_degrees = self.rs485.read_float(254, functioncode=4, numberOfRegisters=2)
            L1_Current_import = self.rs485.read_float(258, functioncode=4, numberOfRegisters=2)
            L2_Current_import = self.rs485.read_float(260, functioncode=4, numberOfRegisters=2)
            L3_Current_import = self.rs485.read_float(262, functioncode=4, numberOfRegisters=2)
            Max_L1_Current_import = self.rs485.read_float(264, functioncode=4, numberOfRegisters=2)
            Max_L2_Current_import = self.rs485.read_float(266, functioncode=4, numberOfRegisters=2)
            Max_L3_Current_import = self.rs485.read_float(268, functioncode=4, numberOfRegisters=2)
            L1_L2_THD = self.rs485.read_float(334, functioncode=4, numberOfRegisters=2)
            L2_L3_THD = self.rs485.read_float(336, functioncode=4, numberOfRegisters=2)
            L3_L1_THD = self.rs485.read_float(338, functioncode=4, numberOfRegisters=2)
            Average_L_L_THD = self.rs485.read_float(340, functioncode=4, numberOfRegisters=2)
            Total_active_watts = self.rs485.read_float(342, functioncode=4, numberOfRegisters=2)
            Total_reactive_watts = self.rs485.read_float(344, functioncode=4, numberOfRegisters=2)
            L1_Import_active = self.rs485.read_float(346, functioncode=4, numberOfRegisters=2)
            L2_Import_active = self.rs485.read_float(348, functioncode=4, numberOfRegisters=2)
            L3_Import_active = self.rs485.read_float(350, functioncode=4, numberOfRegisters=2)
            L1_Export_active = self.rs485.read_float(352, functioncode=4, numberOfRegisters=2)
            L2_Export_active = self.rs485.read_float(354, functioncode=4, numberOfRegisters=2)
            L3_Export_active = self.rs485.read_float(356, functioncode=4, numberOfRegisters=2)
            L1_Total_active = self.rs485.read_float(358, functioncode=4, numberOfRegisters=2)
            L2_Total_active = self.rs485.read_float(360, functioncode=4, numberOfRegisters=2)
            L3_Total_active = self.rs485.read_float(362, functioncode=4, numberOfRegisters=2)
            L1_Import_reactive = self.rs485.read_float(364, functioncode=4, numberOfRegisters=2)
            L2_Import_reactive = self.rs485.read_float(366, functioncode=4, numberOfRegisters=2)
            L3_Import_reactive = self.rs485.read_float(368, functioncode=4, numberOfRegisters=2)
            L1_Export_reactive = self.rs485.read_float(370, functioncode=4, numberOfRegisters=2)
            L2_Export_reactive = self.rs485.read_float(372, functioncode=4, numberOfRegisters=2)
            L3_Export_reactive = self.rs485.read_float(374, functioncode=4, numberOfRegisters=2)
            L1_Total_reactive = self.rs485.read_float(376, functioncode=4, numberOfRegisters=2)
            L2_Total_reactive = self.rs485.read_float(378, functioncode=4, numberOfRegisters=2)
            L3_Total_reactive = self.rs485.read_float(380, functioncode=4, numberOfRegisters=2)
            
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
            Devices[26].Update(0,str(Total_System_Apparent_Power))
            Devices[27].Update(0,str(Total_System_Reactive_Power))
            Devices[28].Update(0,str(Total_Power_Factor))
            Devices[29].Update(0,str(Total_Phase_Angle))
            Devices[30].Update(0,str(Frequency))
            Devices[31].Update(0,str(round(Import_kWh, 3)))
            Devices[32].Update(0,str(round(Export_kWh, 3)))
            Devices[33].Update(0,str(round(Import_kVArh, 3)))
            Devices[34].Update(0,str(round(Export_kVArh, 3)))
            Devices[35].Update(0,str(round(kVAh, 3)))
            Devices[36].Update(0,str(round(kAh, 3)))
            Devices[37].Update(0,str(round(Total_System_Power_import, 3)))
            Devices[38].Update(0,str(round(Max_Total_System_Power_import, 3)))
            Devices[39].Update(0,str(round(Total_System_VA_import, 3)))
            Devices[40].Update(0,str(round(Max_Total_System_VA_import, 3)))
            Devices[41].Update(0,str(round(Neutral_Current_import, 3)))
            Devices[42].Update(0,str(round(Max_Neutral_Current_import, 3)))
            Devices[43].Update(0,str(round(L1_to_L2, 3)))
            Devices[44].Update(0,str(round(L2_to_L3, 3)))
            Devices[45].Update(0,str(round(L3_to_L1, 3)))
            Devices[46].Update(0,str(round(Average_L_to_L, 3)))
            Devices[47].Update(0,str(round(Neutral_Current, 3)))
            Devices[48].Update(0,str(L1_N_THD))
            Devices[49].Update(0,str(L2_N_THD))
            Devices[50].Update(0,str(L3_N_THD))
            Devices[51].Update(0,str(L1_Current_THD))
            Devices[52].Update(0,str(L2_Current_THD))
            Devices[53].Update(0,str(L3_Current_THD))
            Devices[54].Update(0,str(Average_L_N_THD))
            Devices[55].Update(0,str(Average_L_Current_THD))
            Devices[56].Update(0,str(Total_Power_factor_degrees))
            Devices[57].Update(0,str(L1_Current_import))
            Devices[58].Update(0,str(L2_Current_import))
            Devices[59].Update(0,str(L3_Current_import))
            Devices[60].Update(0,str(Max_L1_Current_import))
            Devices[61].Update(0,str(Max_L2_Current_import))
            Devices[62].Update(0,str(Max_L3_Current_import))
            Devices[63].Update(0,str(L1_L2_THD))
            Devices[64].Update(0,str(L2_L3_THD))
            Devices[65].Update(0,str(L3_L1_THD))
            Devices[66].Update(0,str(Average_L_L_THD))
            Devices[67].Update(0,str(round(Total_active_watts, 3)))
            Devices[68].Update(0,str(Total_reactive_watts))
            Devices[69].Update(0,str(round(L1_Import_active, 3)))
            Devices[70].Update(0,str(round(L2_Import_active, 3)))
            Devices[71].Update(0,str(round(L3_Import_active, 3)))
            Devices[72].Update(0,str(round(L1_Export_active, 3)))
            Devices[73].Update(0,str(round(L2_Export_active, 3)))
            Devices[74].Update(0,str(round(L3_Export_active, 3)))
            Devices[75].Update(0,str(round(L1_Total_active, 3)))
            Devices[76].Update(0,str(round(L2_Total_active, 3)))
            Devices[77].Update(0,str(round(L3_Total_active, 3)))
            Devices[78].Update(0,str(L1_Import_reactive))
            Devices[79].Update(0,str(L2_Import_reactive))
            Devices[80].Update(0,str(L3_Import_reactive))
            Devices[81].Update(0,str(L1_Export_reactive))
            Devices[82].Update(0,str(L2_Export_reactive))
            Devices[83].Update(0,str(L3_Export_reactive))
            Devices[84].Update(0,str(L1_Total_reactive))
            Devices[85].Update(0,str(L2_Total_reactive))
            Devices[86].Update(0,str(L3_Total_reactive))
            
            
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
                Domoticz.Log('Total_System_Reactive_Power: {0:.3f} VAr'.format(Total_System_Reactive_Power))
                Domoticz.Log('Total_Power_Factor: {0:.3f} PF'.format(Total_Power_Factor))
                Domoticz.Log('Total_Phase_Angle: {0:.3f} °'.format(Total_Phase_Angle))
                Domoticz.Log('Frequency: {0:.3f} Hz'.format(Frequency))
                Domoticz.Log('Import_kWh: {0:.3f} kWh'.format(Import_kWh))
                Domoticz.Log('Export_kWh: {0:.3f} kWh'.format(Export_kWh))
                Domoticz.Log('Import_kVArh: {0:.3f} kVArh'.format(Import_kVArh))
                Domoticz.Log('Export_kVArh: {0:.3f} kVArh'.format(Export_kVArh))
                Domoticz.Log('kVAh: {0:.3f} kVAh'.format(kVAh))
                Domoticz.Log('kAh: {0:.3f} kAh'.format(kAh))
                Domoticz.Log('Total_System_Power_import: {0:.3f} W'.format(Total_System_Power_import))
                Domoticz.Log('Max_Total_System_Power_import: {0:.3f} W'.format(Max_Total_System_Power_import))
                Domoticz.Log('Total_System_VA_import: {0:.3f} VA'.format(Total_System_VA_import))
                Domoticz.Log('Max_Total_System_VA_import: {0:.3f} VA'.format(Max_Total_System_VA_import))
                Domoticz.Log('Neutral_Current_import: {0:.3f} A'.format(Neutral_Current_import))
                Domoticz.Log('Max_Neutral_Current_import: {0:.3f} A'.format(Max_Neutral_Current_import))
                Domoticz.Log('L1_to_L2: {0:.3f} V'.format(L1_to_L2))
                Domoticz.Log('L2_to_L3: {0:.3f} V'.format(L2_to_L3))
                Domoticz.Log('L3_to_L1: {0:.3f} V'.format(L3_to_L1))
                Domoticz.Log('Average_L_to_L: {0:.3f} V'.format(Average_L_to_L))
                Domoticz.Log('Neutral_Current: {0:.3f} A'.format(Neutral_Current))
                Domoticz.Log('L1_N_THD: {0:.3f} %'.format(L1_N_THD))
                Domoticz.Log('L2_N_THD: {0:.3f} %'.format(L2_N_THD))
                Domoticz.Log('L3_N_THD: {0:.3f} %'.format(L3_N_THD))
                Domoticz.Log('L1_Current_THD: {0:.3f} %'.format(L1_Current_THD))
                Domoticz.Log('L2_Current_THD: {0:.3f} %'.format(L2_Current_THD))
                Domoticz.Log('L3_Current_THD: {0:.3f} %'.format(L3_Current_THD))
                Domoticz.Log('Average_L_N_THD: {0:.3f} %'.format(Average_L_N_THD))
                Domoticz.Log('Average_L_Current_THD: {0:.3f} %'.format(Average_L_Current_THD))
                Domoticz.Log('Total_Power_factor_degrees: {0:.3f} °'.format(Total_Power_factor_degrees))
                Domoticz.Log('L1_Current_import: {0:.3f} A'.format(L1_Current_import))
                Domoticz.Log('L2_Current_import: {0:.3f} A'.format(L2_Current_import))
                Domoticz.Log('L3_Current_import: {0:.3f} A'.format(L3_Current_import))
                Domoticz.Log('Max_L1_Current_import: {0:.3f} A'.format(Max_L1_Current_import))
                Domoticz.Log('Max_L2_Current_import: {0:.3f} A'.format(Max_L2_Current_import))
                Domoticz.Log('Max_L3_Current_import: {0:.3f} A'.format(Max_L3_Current_import))
                Domoticz.Log('L1_L2_THD: {0:.3f} %'.format(L1_L2_THD))
                Domoticz.Log('L2_L3_THD: {0:.3f} %'.format(L2_L3_THD))
                Domoticz.Log('L3_L1_THD: {0:.3f} %'.format(L3_L1_THD))
                Domoticz.Log('Average_L_L_THD: {0:.3f} %'.format(Average_L_L_THD))
                Domoticz.Log('Total_active_watts: {0:.3f} %'.format(Total_active_watts))
                Domoticz.Log('Total_reactive_watts: {0:.3f} %'.format(Total_reactive_watts))
                Domoticz.Log('L1_Import_active: {0:.3f} kWh'.format(L1_Import_active))
                Domoticz.Log('L2_Import_active: {0:.3f} kWh'.format(L2_Import_active))
                Domoticz.Log('L3_Import_active: {0:.3f} kWh'.format(L3_Import_active))
                Domoticz.Log('L1_Export_active: {0:.3f} kWh'.format(L1_Export_active))
                Domoticz.Log('L2_Export_active: {0:.3f} kWh'.format(L2_Export_active))
                Domoticz.Log('L3_Export_active: {0:.3f} kWh'.format(L3_Export_active))
                Domoticz.Log('L1_Total_active: {0:.3f} kWh'.format(L1_Total_active))
                Domoticz.Log('L2_Total_active: {0:.3f} kWh'.format(L2_Total_active))
                Domoticz.Log('L3_Total_active: {0:.3f} kWh'.format(L3_Total_active))
                Domoticz.Log('L1_Import_reactive: {0:.3f} kVArh'.format(L1_Import_reactive))
                Domoticz.Log('L2_Import_reactive: {0:.3f} kVArh'.format(L2_Import_reactive))
                Domoticz.Log('L3_Import_reactive: {0:.3f} kVArh'.format(L3_Import_reactive))
                Domoticz.Log('L1_Export_reactive: {0:.3f} kVArh'.format(L1_Export_reactive))
                Domoticz.Log('L2_Export_reactive: {0:.3f} kVArh'.format(L2_Export_reactive))
                Domoticz.Log('L3_Export_reactive: {0:.3f} kVArh'.format(L3_Export_reactive))
                Domoticz.Log('L1_Total_reactive: {0:.3f} kVArh'.format(L1_Total_reactive))
                Domoticz.Log('L2_Total_reactive: {0:.3f} kVArh'.format(L2_Total_reactive))
                Domoticz.Log('L3_Total_reactive: {0:.3f} kVArh'.format(L3_Total_reactive))
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
