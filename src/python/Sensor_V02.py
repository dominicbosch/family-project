import httplib2
import json
import time

h = httplib2.Http()

def compile_httpgettemp(IDeviceNum, ICmdClass):
    sOutBuf = "http://192.168.0.79:8083/ZWaveAPI/Run/devices[" + str(IDeviceNum)
    sOutBuf = sOutBuf + "].instances[2].commandClasses[" + str(ICmdClass)
    sOutBuf = sOutBuf + "].data[1].val.value"
    return sOutBuf

def get_currenttemp(IDeviceNum, ICmdClass):
    resp, content = h.request(compile_httpgettemp(IDeviceNum, ICmdClass), "GET")
    DDevInfo = json.loads(content.decode('ascii'))
    return DDevInfo

QDevice = 8
ICmdClass = 49

print ("Device : ", str(QDevice), " does read", get_currenttemp(QDevice, ICmdClass), "Degrees Celsius")
# print("{} {}\n".format(time.ctime(time.time()),get_currenttemp(8, 49)))
