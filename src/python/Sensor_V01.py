import httplib2
import json
import time

h = httplib2.Http()

def compile_httprefresh(IDeviceNum, ICmdClass):
    sOutBuf = "http://192.168.0.79:8083/ZWaveAPI/Run/devices[" + str(IDeviceNum)
    sOutBuf = sOutBuf + "].instances[0].commandClasses[" + str(ICmdClass)
    sOutBuf = sOutBuf + "].Get()"
    return sOutBuf

def compile_httpgetstat(IDeviceNum, ICmdClass):
    sOutBuf = "http://192.168.0.79:8083/ZWaveAPI/Run/devices[" + str(IDeviceNum)
    sOutBuf = sOutBuf + "].instances[0].commandClasses[" + str(ICmdClass)
    sOutBuf = sOutBuf + "].data[3].val.value"
    return sOutBuf

#.data[1].val.value
#.data[3].val.value

def get_currentstat(IDeviceNum, ICmdClass):
#    resp, content = h.request(compile_httprefresh(IDeviceNum, ICmdClass), "GET")
    resp, content = h.request(compile_httpgetstat(IDeviceNum, ICmdClass), "GET")
    DDevInfo = json.loads(content.decode('ascii'))
    return DDevInfo

#def get_switchstat(DDevInfo):
#    BDevStatus = DDevInfo['value']
#    if BDevStatus == True:
#        SDevStatus = "On"
#    else:
#        SDevStatus = "Off"
#    return SDevStatus

QDevice = 5
ICmdClass = 49

print ("Current Status of Device : ", str(QDevice), " is ", get_currentstat(QDevice, ICmdClass))
