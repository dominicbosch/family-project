import time
import httplib2
import json

# Conifguration Record,
# Device Id (Assigned manually)
# Device Type (S = Switch, T = Temp sensor)
# Device Number (Assigned by Server)
# Device Instance
# Device Name

iSleepTime = 20
sServerAddress = "192.168.0.79:8083"

sFileName = "/mnt/nas/switch.inf"
sDeviceConfigFileName = "/mnt/nas/config.txt"
sVelocityConfigFileName = "/mnt/nas/WindDevCOnfig.txt"
sVelocityFileName = "/mnt/nas/Windspeed.inf"
sStopFileName = "/mnt/nas/stop.yes"

#sFileName = "switch.inf"
#sDeviceConfigFileName = "config.txt"
#sVelocityConfigFileName = "WindDevCOnfig.txt"
#sVelocityFileName = "Windspeed.inf"
#sStopFileName = "stop.yes"

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

def get_switchstat(DDevInfo):
    BDevStatus = DDevInfo['value']
    if BDevStatus == True:
        SDevStatus = "On"
    else:
        SDevStatus = "Off"
    return SDevStatus

def get_openfile(SFileName):
    try:
        tobj = open(SFileName, "r")
        tobj.close()
        return True
    except (IOError, TypeError):
        return False

def get_newfile(SFileName):
    try:
        tobj = open(SFileName, "r")
        tobj.close()
        return True
    except (IOError, TypeError):
        print("Creating new file : ", sFileName)    

    try:
        tobj = open(SFileName, "a")
        tobj.close()
        return True
    except (IOError, TypeError):
        return False

StopRun = False
iOldVelocity = 0

print("Application started !\n")

while StopRun == False:

    if get_openfile(sDeviceConfigFileName) == True and get_newfile(sFileName) == True:
        fConfFile = open(sDeviceConfigFileName, "r")
        fObiS = open(sFileName, "a")

        lRequestTime = time.time()
        t = time.gmtime(lRequestTime)
        tDay = int(t.tm_mday)
        tMonth = int(t.tm_mon)
        tYear = int(t.tm_year)
        tHour = int(t.tm_hour)
        tMin = int(t.tm_min)
        tWeekDay = int(t.tm_wday)
        print("\nDate : Time {} {} {} : {} {} - Weekday {}\n".format(tDay, tMonth, tYear, tHour, tMin, tWeekDay))

        for sLine in fConfFile:

            rConfigRecord = sLine.split(",")
    
            iDeviceId = int(rConfigRecord[0])
            sDeviceType = rConfigRecord[1].strip()
            iDeviceNum = int(rConfigRecord[2])
            iDeviceInst = int(rConfigRecord[3])
            sDeviceName = rConfigRecord[4].strip()

            if sDeviceType == "S":
                sDevResp = get_currentstat(iDeviceNum, iDeviceInst)
                if sDevResp != "":
                    sDevStatus = get_switchstat(sDevResp)
                    sRequestTime = time.ctime(lRequestTime)
                    print("Device : {} - Status : {}".format(sDeviceName, sDevStatus))
                    fObiS.write("{}, {}, {}\n".format(str(iDeviceNum), lRequestTime, sDevStatus))
                else:
                    print("Value Error thrown - ", time.ctime(time.time()))
                    fObiS.write("{} {}\n".format("Value error at :", time.ctime(time.time())))

        fObiS.close()
        fConfFile.close()

    if get_openfile(sVelocityConfigFileName) == True and get_newfile(sVelocityFileName) == True:

        fConfFile = open(sVelocityConfigFileName, "r")
        fObiS = open(sVelocityFileName, "a")
    
        for sLine in fConfFile:

            rConfigRecord = sLine.split(",")
    
            iDeviceId = int(rConfigRecord[0])
            iDeviceNum = int(rConfigRecord[2])
            iDeviceInst = int(rConfigRecord[3])
            iDataLevel = int(rConfigRecord[4])
            sDeviceName = rConfigRecord[5].strip()

            if iDataLevel == 6:

                lRequestTime = time.time()

                sDevResp = get_current(iDeviceNum, iDeviceInst, iDataLevel)

                if sDevResp != "":
                    sDevTemp = sDevResp
                    sRequestTime = time.ctime(time.time())
                    if int(sDevTemp) != iOldVelocity:
                        iOldVelocity = int(sDevTemp)
                        print("Device : {} - Speed : {}".format(sDeviceName, sDevTemp))
                        fObiS.write("{}, {}, {}, {}\n".format(str(iDataLevel), sDeviceName, lRequestTime, sDevTemp))
                    else:
                        print("Device : {} - Speed : {} -> Unchanged".format(sDeviceName, sDevTemp))
                else:
                    print("Value Error thrown - ", time.ctime(time.time()))

        fObiS.close()
        fConfFile.close()

    time.sleep(iSleepTime)
    StopRun = get_openfile(sStopFileName)    

print("\nApplication halted !\n")
