import httplib2
import json
import time

h = httplib2.Http()

def compile_httpgettemp(IDeviceNum, ICmdClass, iDataLevel):
    sOutBuf = "http://192.168.0.79:8083/ZWaveAPI/Run/devices[" + str(IDeviceNum)
    sOutBuf = sOutBuf + "].instances[0].commandClasses[" + str(ICmdClass)
    sOutBuf = sOutBuf + "].data[" + str(iDataLevel) + "].val.value"
    return sOutBuf

def get_currenttemp(IDeviceNum, ICmdClass, iDataLevel):
    resp, content = h.request(compile_httpgettemp(IDeviceNum, ICmdClass, iDataLevel), "GET")
    DDevInfo = json.loads(content.decode('ascii'))
    return DDevInfo

iCmdClass = 49
iDevice = 8
iDataLevel = 1
sDevice = "Waschküche"
print (sDevice, " does read", get_currenttemp(iDevice, iCmdClass, iDataLevel), "Degrees Celsius")

iDataLevel = 5
print (sDevice, " does read", str(get_currenttemp(iDevice, iCmdClass, iDataLevel)), "% Humidity")

iDataLevel = 4
print (sDevice, " does read", str(get_currenttemp(iDevice, iCmdClass, iDataLevel)), "W Power Level")

iDevice = 12
iDataLevel = 1
sDevice = "Balkon"
print (sDevice, " does read", str(get_currenttemp(iDevice, iCmdClass, iDataLevel)), "Degree Celcius")

iDataLevel = 3
print (sDevice, " does read", str(get_currenttemp(iDevice, iCmdClass, iDataLevel)), "% Luminiscence")

iDataLevel = 5
print (sDevice, " does read", str(get_currenttemp(iDevice, iCmdClass, iDataLevel)), "% Humidity")

iDataLevel = 6
print (sDevice, " does read", str(get_currenttemp(iDevice, iCmdClass, iDataLevel)), "m/s Velocity")

iDataLevel = 9
print (sDevice, " does read", str(get_currenttemp(iDevice, iCmdClass, iDataLevel)), "kPa Barometric Pressure")

iDataLevel = 11
print (sDevice, " does read", str(get_currenttemp(iDevice, iCmdClass, iDataLevel)), "Degree Celcius Dew Point")

