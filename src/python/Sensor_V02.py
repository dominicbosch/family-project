import httplib2
import json
import time

h = httplib2.Http()

def compile_httpgettemp(IDeviceNum, ICmdClass):
    sOutBuf = "http://192.168.0.79:8083/ZWaveAPI/Run/devices[" + str(IDeviceNum)
    sOutBuf = sOutBuf + "].instances[0].commandClasses[" + str(ICmdClass)
    sOutBuf = sOutBuf + "].data[1].val.value"
    return sOutBuf

def get_currenttemp(IDeviceNum, ICmdClass):
    resp, content = h.request(compile_httpgettemp(IDeviceNum, ICmdClass), "GET")
    DDevInfo = json.loads(content.decode('ascii'))
    return DDevInfo

QDevice = 5
ICmdClass = 49

#print ("Current Status of Device : ", str(QDevice), " is ", get_currenttemp(QDevice, ICmdClass))
print("{} {}\n".format(time.ctime(time.time()),get_currenttemp(5, 49)))
