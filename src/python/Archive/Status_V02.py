
import httplib2
import json
import time

#SFileName = "/mnt/nas/switch.inf"
#STempFileName = "/mnt/nas/temp.inf"
#SStopFileName = "/mnt/nas/stop.yes"

STempFileName = "temp.inf"
SFileName = "switch.inf"
SStopFileName = "stop.yes"

#ISleepTime = 60
ISleepTime = 5

h = httplib2.Http()

def compile_httprefresh(IDeviceNum):
    sOutBuf = "http://192.168.0.79:8083/ZWaveAPI/Run/devices[" + str(IDeviceNum)
    sOutBuf = sOutBuf + "].instances[0].commandClasses[0x25].Get()"
    return sOutBuf

def compile_httpgetstat(IDeviceNum):
    sOutBuf = "http://192.168.0.79:8083/ZWaveAPI/Run/devices[" + str(IDeviceNum)
    sOutBuf = sOutBuf + "].instances[0].commandClasses[0x25].data.level"
    return sOutBuf

def compile_httpgettemp(IDeviceNum, ICmdClass):
    sOutBuf = "http://192.168.0.79:8083/ZWaveAPI/Run/devices[" + str(IDeviceNum)
    sOutBuf = sOutBuf + "].instances[0].commandClasses[" + str(ICmdClass)
    sOutBuf = sOutBuf + "].data[1].val.value"
    return sOutBuf

def get_currentstat(IDeviceNum):
    resp, content = h.request(compile_httprefresh(IDeviceNum), "GET")
    resp, content = h.request(compile_httpgetstat(IDeviceNum), "GET")
    DDevInfo = json.loads(content.decode('ascii'))
    return DDevInfo

def get_currenttemp(IDeviceNum, ICmdClass):
    resp, content = h.request(compile_httpgettemp(IDeviceNum, ICmdClass), "GET")
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

def get_openfile(SFileName):
    try:
        tobj = open(SFileName, "r")
        tobj.close()
        return True
    except (IOError, TypeError):
        return False

print("Application started !")
ILoopCounter = 1
StopRun = False

while StopRun == False:

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

    if ILoopCounter == 1:
        sDevTemp = get_currenttemp(5, 49)
        print("{} {}\n".format(time.ctime(time.time()),sDevTemp))
        fobiT = open(STempFileName, "a")
        fobiT.write("{} {}\n".format(time.ctime(time.time()),sDevTemp))
        fobiT.close()

    ILoopCounter = ILoopCounter + 1

    if ILoopCounter == 10:
        ILoopCounter = 0

    print("Loop Counter : ", ILoopCounter, "\n")

    time.sleep(ISleepTime)
    StopRun = get_openfile(SStopFileName)
        
print("Application halted !")
