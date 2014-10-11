
import httplib2
import json

h = httplib2.Http(".cache")

def compile_httpset(IDeviceNum, IDeviceSet):
    sOutBuf = "http://192.168.0.79:8083/ZWaveAPI/Run/devices[" + str(IDeviceNum)
    sOutBuf = sOutBuf + "].instances[0].commandClasses[0x25].Set(" + str(IDeviceSet)
    sOutBuf = sOutBuf + ")"
    return sOutBuf

def compile_httprefresh(IDeviceNum):
    sOutBuf = "http://192.168.0.79:8083/ZWaveAPI/Run/devices[" + str(IDeviceNum)
    sOutBuf = sOutBuf + "].instances[0].commandClasses[0x25].Get()"
    return sOutBuf

def compile_httpgetstat(IDeviceNum):
    sOutBuf = "http://192.168.0.79:8083/ZWaveAPI/Run/devices[" + str(IDeviceNum)
    sOutBuf = sOutBuf + "].instances[0].commandClasses[0x25].data.level"
    return sOutBuf

ISwitchStat = 0

i = 2
while i <= 3:
    resp, content = h.request(compile_httpset(i, ISwitchStat), "GET")
    resp, content = h.request(compile_httprefresh(i), "GET")
    resp, content = h.request(compile_httpgetstat(i), "GET")
    DDevInfo = json.loads(content.decode('ascii'))
    BDevStatus = DDevInfo['value']

    if BDevStatus == True:
        SDevStatus = "On"
    else:
        SDevStatus = "Off"

    print("Switch : ", i, " is ", SDevStatus)
    
    i = i + 1
    

    
