import time
import httplib2
import json

# Conifguration Record,
# Device Id (Assigned manually)
# Device Type (S = Switch, T = Temp sensor)
# Device Number (Assigned by Server)
# Device Instance
# Device Name

iSleepTime = 10

#sFileName = "/mnt/nas/switch.inf"
#sStopFileName = "/mnt/nas/stop.yes"
#sDeviceConfigFileName = "config.txt"

sFileName = "temp.inf"
sDeviceConfigFileName = "config.txt"
sStopFileName = "stop.yes"
sServerAddress = "192.168.0.79:8083"

h = httplib2.Http()


def compile_httprefresh(iDeviceNum, iDeviceInstance):
    sOutBuf = "http://" + sServerAddress + "/ZWaveAPI/Run/devices[" + str(iDeviceNum)
    sOutBuf = sOutBuf + "].instances[" + str(iDeviceInstance) + "].commandClasses[0x25].Get()"
    return sOutBuf

def compile_httpgettemp(IDeviceNum, ICmdClass):
    sOutBuf = "http://192.168.0.79:8083/ZWaveAPI/Run/devices[" + str(IDeviceNum)
    sOutBuf = sOutBuf + "].instances[0].commandClasses[" + str(ICmdClass)
    sOutBuf = sOutBuf + "].data[1].val.value"
    return sOutBuf

def get_currenttemp(iDeviceNum, iDeviceInstance):
    resp, content = h.request(compile_httprefresh(iDeviceNum, iDeviceInstance), "GET")
    resp, content = h.request(compile_httpgettemp(iDeviceNum, 49), "GET")
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
        sDeviceType = rConfigRecord[1].strip()
        iDeviceNum = int(rConfigRecord[2])
        iDeviceInst = int(rConfigRecord[3])
        sDeviceName = rConfigRecord[4].strip()

        if sDeviceType == "T":
            sDevResp = get_currenttemp(iDeviceNum, iDeviceInst)
            if sDevResp != "":
                sDevTemp = sDevResp
                sRequestTime = time.ctime(time.time())
                print("Device :", str(iDeviceNum), ":", sDeviceName, "- Time :", sRequestTime, "- Temparatur : ", sDevTemp)
                fObiS.write("{}, {}, {}\n".format(str(iDeviceNum), sRequestTime, sDevTemp))
            else:
                print("Value Error thrown - ", time.ctime(time.time()))
                fObiS.write("{} {}\n".format("Value erroro at :", time.ctime(time.time())))

    fObiS.close()
    fConfFile.close()

    time.sleep(iSleepTime)
    StopRun = get_openfile(sStopFileName)    

print("\nApplication halted !\n")
