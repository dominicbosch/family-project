import time
import httplib2
import json

# Conifguration Record,
# Device Type (S = Switch, T = Temp sensor, ...)
# Device Number (Assigned by Server)
# Device Instance
# Data Level
# Device Name

iSleepTime = 60
#sFileName = "/mnt/nas/Windspeed.inf"
#sStopFileName = "/mnt/nas/stop.yes"
#sDeviceConfigFileName = "WindDevCOnfig.txt"

sFileName = "Windspeed.inf"
sDeviceConfigFileName = "WindDevCOnfig.txt"
sStopFileName = "stop.yes"
sServerAddress = "192.168.0.79:8083"

h = httplib2.Http()


def compile_httprefresh(iDeviceNum, iDeviceInstance):
    sOutBuf = "http://" + sServerAddress + "/ZWaveAPI/Run/devices[" + str(iDeviceNum)
    sOutBuf = sOutBuf + "].instances[" + str(iDeviceInstance) + "].commandClasses[0x25].Get()"
    return sOutBuf

def compile_httpgettemp(IDeviceNum, ICmdClass, iDataLevel):
    sOutBuf = "http://192.168.0.79:8083/ZWaveAPI/Run/devices[" + str(IDeviceNum)
    sOutBuf = sOutBuf + "].instances[0].commandClasses[" + str(ICmdClass)
    sOutBuf = sOutBuf + "].data[" + str(iDataLevel) + "].val.value"
    return sOutBuf

def get_current(iDeviceNum, iDeviceInstance, iDataLevel):
    resp, content = h.request(compile_httprefresh(iDeviceNum, iDeviceInstance), "GET")
    resp, content = h.request(compile_httpgettemp(iDeviceNum, 49, iDataLevel), "GET")
    try:
        DDevInfo = json.loads(content.decode('ascii'))
        return DDevInfo
    except (ValueError):
        return ""
    
def get_currenttime(DDevInfo):
    return DDevInfo["updateTime"]

def get_openfile(SFileName):
    try:
        tobj = open(SFileName, "r")
        tobj.close()
        return True
    except (IOError, TypeError):
        return False

StopRun = False

print("Application started !\n")

while StopRun == False:

    fConfFile = open(sDeviceConfigFileName, "r")
    fObiS = open(sFileName, "a")
    
    for sLine in fConfFile:

        rConfigRecord = sLine.split(",")
    
        iDeviceId = int(rConfigRecord[0])
        iDeviceNum = int(rConfigRecord[2])
        iDeviceInst = int(rConfigRecord[3])
        iDataLevel = int(rConfigRecord[4])
        sDeviceName = rConfigRecord[5].strip()

        lRequestTime = time.time()

        sDevResp = get_current(iDeviceNum, iDeviceInst, iDataLevel)

        if sDevResp != "":
            sDevTemp = sDevResp
            sRequestTime = time.ctime(time.time())
            print(sDeviceName, " -> ", sDevTemp, " - Time :", sRequestTime)
            fObiS.write("{}, {}, {}, {}\n".format(str(iDataLevel), sDeviceName, lRequestTime, sDevTemp))
        else:
            print("Value Error thrown - ", time.ctime(time.time()))
            fObiS.write("{} {}\n".format("Value error at :", time.ctime(time.time())))

    fObiS.close()
    fConfFile.close()

    print("\n")

    time.sleep(iSleepTime)
    StopRun = get_openfile(sStopFileName)    

print("\nApplication halted !\n")
