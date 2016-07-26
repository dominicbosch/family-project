
import httplib2
import json
import time

#SFileName = "/mnt/nas/switch.inf"
SFileName = "switch.inf"
ISleepTime = 10
h = httplib2.Http()

def compile_httprefresh(IDeviceNum):
    sOutBuf = "http://192.168.0.79:8083/ZWaveAPI/Run/devices[" + str(IDeviceNum)
    sOutBuf = sOutBuf + "].instances[0].commandClasses[0x25].Get()"
    return sOutBuf

def compile_httpgetstat(IDeviceNum):
    sOutBuf = "http://192.168.0.79:8083/ZWaveAPI/Run/devices[" + str(IDeviceNum)
    sOutBuf = sOutBuf + "].instances[0].commandClasses[0x25].data.level"
    return sOutBuf

def get_currentstat(IDeviceNum):
    resp, content = h.request(compile_httprefresh(IDeviceNum), "GET")
    resp, content = h.request(compile_httpgetstat(IDeviceNum), "GET")
    DDevInfo = json.loads(content.decode('ascii'))
    return DDevInfo

def get_switchstat(DDevInfo):
    BDevStatus = DDevInfo['value']
    if BDevStatus == True:
        SDevStatus = "On"
    else:
        SDevStatus = "Off"
    return SDevStatus

def get_currenttime(DDevInfo):
    return DDevInfo["updateTime"]

while True:

    IDevice = 2
    print ("Current Status of Switch : ", str(IDevice), " is ", get_switchstat(get_currentstat(IDevice)))

    
    dDevStatus = get_currentstat(IDevice)
    sDevStatus = get_switchstat(dDevStatus)
    fobiS = open(SFileName, "a")
    fobiS.write("{}, {}, {}\n".format(str(IDevice), get_currenttime(dDevStatus), dDevStatus['value']))
    fobiS.close()

    IDevice = 3
    print ("Current Status of Switch : ", str(IDevice), " is ", get_switchstat(get_currentstat(IDevice)))

    dDevStatus = get_currentstat(IDevice)
    sDevStatus = get_switchstat(dDevStatus)
    fobiS = open(SFileName, "a")
    fobiS.write("{}, {}, {}\n".format(str(IDevice), get_currenttime(dDevStatus), dDevStatus['value']))
    fobiS.close()

    IDevice = 4
    print ("Current Status of Switch : ", str(IDevice), " is ", get_switchstat(get_currentstat(IDevice)))

    dDevStatus = get_currentstat(IDevice)
    sDevStatus = get_switchstat(dDevStatus)
    fobiS = open(SFileName, "a")
    fobiS.write("{}, {}, {}\n".format(str(IDevice), get_currenttime(dDevStatus), dDevStatus['value']))
    fobiS.close()

    time.sleep(ISleepTime)
    
#    resp, content = h.request(compile_httpset(i, get_statetoswitch()), "GET")

#    dDevStatus = get_currentstat(i)
#    sDevStatus = get_switchstat(dDevStatus)

#    fobj = open("SwitchInfo.txt", "a")
#    sOutBuf = "Switch : " + str(i) + " is " + sDevStatus
#    print(sOutBuf)
#    fobj.write("{}\n".format(sOutBuf))
#    fobj.close()


#    print("Current Time : ", time.ctime(), "\nTime from Switch", str(i), ":", time.ctime(get_currenttime(dDevStatus)))    

#    i = get_lighttoswitch()
    
