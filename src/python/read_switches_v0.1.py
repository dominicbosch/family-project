import time
import httplib2
import json

# Conifguration Record,
# Device Id (Assigned manually)
# Device Type (S = Switch)
# Device Number (Assigned by Server)
# Device Instance
# Device Name

iSleepTime = 10

#sFileName = "/mnt/nas/switch.inf"
#sStopFileName = "/mnt/nas/stop.yes"
#sDeviceConfigFileName = "config.txt"

sFileName = "switch.inf"
sDeviceConfigFileName = "config.txt"
sStopFileName = "stop.yes"
sServerAddress = "192.168.0.79:8083"

h = httplib2.Http()

def compile_httprefresh(iDeviceNum, iDeviceInstance):
    sOutBuf = "http://" + sServerAddress + "/ZWaveAPI/Run/devices[" + str(iDeviceNum)
    sOutBuf = sOutBuf + "].instances[" + str(iDeviceInstance) + "].commandClasses[0x25].Get()"
    return sOutBuf

def compile_httpgetstat(iDeviceNum, iDeviceInstance):
    sOutBuf = "http://" + sServerAddress + "/ZWaveAPI/Run/devices[" + str(iDeviceNum)
    sOutBuf = sOutBuf + "].instances[" + str(iDeviceInstance) + "].commandClasses[0x25].data.level"
    return sOutBuf

def get_currentstat(iDeviceNum, iDeviceInstance):
    resp, content = h.request(compile_httprefresh(iDeviceNum, iDeviceInstance), "GET")
    resp, content = h.request(compile_httpgetstat(iDeviceNum, iDeviceInstance), "GET")
    try:
        DDevInfo = json.loads(content.decode('ascii'))
        return DDevInfo
    except (ValueError):
        return ""

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

StopRun = False

print("Application started !\n")

while StopRun == False:

    fConfFile = open(sDeviceConfigFileName, "r")
    fObiS = open(sFileName, "a")

    for sLine in fConfFile:

        rConfigRecord = sLine.split(",")
    
        iDeviceId = int(rConfigRecord[0])
        sDeviceType = rConfigRecord[1].strip()
        iDeviceNum = int(rConfigRecord[2])
        iDeviceInst = int(rConfigRecord[3])
        sDeviceName = rConfigRecord[4].strip()

        sDevResp = get_currentstat(iDeviceNum, iDeviceInst)
        if sDevResp != "":
            sDevStatus = get_switchstat(sDevResp)
            lRequestTime = get_currenttime(sDevResp)
            sRequestTime = time.ctime(lRequestTime)
            print("Device :", str(iDeviceNum), ":", sDeviceName, "- Time :", sRequestTime, "- Status :", sDevStatus, "\n")
            fObiS.write("{}, {}, {}\n".format(str(iDeviceNum), lRequestTime, sDevStatus))
        else:
            print("Value Error thrown - ", time.ctime(time.time()))
            fObiS.write("{} {}\n".format("Value erroro at :", time.ctime(time.time()),sDevTemp))

    fObiS.close()
    fConfFile.close()

    time.sleep(iSleepTime)
    StopRun = get_openfile(sStopFileName)    

print("\nApplication halted !\n")
