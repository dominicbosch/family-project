import time
import httplib2
import json

#sFile Structure
#0 Device Number
#1 Date / Time Stamp
#2 Status (on/off)

sServerAddress = "192.168.0.79:8083"
httpRequest = httplib2.Http()

#sDeviceConfigFileName = "/mnt/nas/config.txt"
#SfName = "/mnt/nas/switch.inf"

sDeviceConfigFileName = "/mnt/debian/config.txt"
SfName = "/mnt/debian/switch.inf"

class powerSwitch:
    def __init__(self, iSwitchNum, iSwitchInst, sSwitchName, sServerAddress):
        self.iSwitchNum = iSwitchNum
        self.iSwitchInst = iSwitchInst
        self.sSwitchName = sSwitchName
        self.sServerAddress = sServerAddress

    def compile_httprefresh(self):
        sOutBuf = "http://" + self.sServerAddress + "/ZWaveAPI/Run/devices[" + str(self.iSwitchNum)
        sOutBuf = sOutBuf + "].instances[" + str(self.iSwitchInst) + "].commandClasses[0x25].Get()"
        return sOutBuf

    def compile_httpgetstat(self):
        sOutBuf = "http://" + self.sServerAddress + "/ZWaveAPI/Run/devices[" + str(self.iSwitchNum)
        sOutBuf = sOutBuf + "].instances[" + str(self.iSwitchInst) + "].commandClasses[0x25].data.level"
        return sOutBuf

    def compile_httpset(self, iSwitchStat):
        sOutBuf = "http://" + self.sServerAddress+ "/ZWaveAPI/Run/devices[" + str(self.iSwitchNum)
        sOutBuf = sOutBuf + "].instances[" + str(self.iSwitchInst)+ "].commandClasses[0x25].Set(" + str(iSwitchStat)
        sOutBuf = sOutBuf + ")"
        return sOutBuf
        
    def sStatus(self):
        resp, content = httpRequest.request(self.compile_httprefresh(), "GET")
        resp, content = httpRequest.request(self.compile_httpgetstat(), "GET")

        try:
            dDevInfo = json.loads(content.decode('ascii'))
            bDevStatus = dDevInfo['value']
            if bDevStatus == True:
                sDevStatus = "On"
            else:
                sDevStatus = "Off"
            return sDevStatus
        except (ValueError):
            return ""

    def iStatus(self):
        resp, content = httpRequest.request(self.compile_httprefresh(), "GET")
        resp, content = httpRequest.request(self.compile_httpgetstat(), "GET")

        try:
            dDevInfo = json.loads(content.decode('ascii'))
            bDevStatus = dDevInfo['value']
            if bDevStatus == True:
                iDevStatus = 1
            else:
                iDevStatus = 0
            return iDevStatus
        except (ValueError):
            return -1

    def SwitchTo(self,iSwitchStat):
        resp, content = httpRequest.request(self.compile_httprefresh(), "GET")
        resp, content = httpRequest.request(self.compile_httpset(iSwitchStat), "GET")
        iLoopCounter = 0

        while self.iStatus() != iSwitchStat and iLoopCounter < 10:
            print("Retrying ... \n")
            time.sleep(1)
            resp, content = httpRequest.request(self.compile_httprefresh(), "GET")
            resp, content = httpRequest.request(self.compile_httpset(iSwitchStat), "GET")
            iLoopCounter += 1
        if self.iStatus() != iSwitchStat:
            return False
        else:
            return True   
    
    def On(self):
        bRetval = self.SwitchTo(1)
        return bRetval

    def Off(self):
        bRetval = self.SwitchTo(0)
        return bRetval

def bReadSwitchInfoFile(sFileName, aWorkDataArr):

    iWeekCount = 1
    iRecordsOk = 0

    try:
        fobj = open(sFileName, "r")
    except IOError:
        print("Cannot open file : ", sFileName)
        return False

    print("Source File is open")

    for line in fobj:
        sOutBuf = line.split(",")
        if sOutBuf[0].find("error") == -1:

            t = time.gmtime(float(sOutBuf[1]))
        
            iRecordsOk = iRecordsOk +1

            if iRecordsOk >= 2:
                if (int(t.tm_wday) == 0) and (int(sWorkBuf[4]) == 6):
                    iWeekCount = iWeekCount+1
        
            sWorkBuf = [sOutBuf[0], int(t.tm_year), int(t.tm_mon), iWeekCount, int(t.tm_wday), int(t.tm_mday), int(t.tm_yday), int(t.tm_hour), int(t.tm_min), int(t.tm_sec), sOutBuf[2]]
            sWorkData.append(sWorkBuf)
        
    fobj.close()
    return True

def aReadConfigFile(sConfFileName, aSwitchArr):

    try:
        fConfFile = open(sConfFileName, "r")
    except IOError:
        print("Cannot open file : ", sConfFileName)
        return False

    for sLine in fConfFile:
        rConfigRecord = sLine.split(",")

        iDeviceId = int(rConfigRecord[0])
        sDeviceType = rConfigRecord[1].strip()
        iDeviceNum = int(rConfigRecord[2])
        iDeviceInst = int(rConfigRecord[3])
        sDeviceName = rConfigRecord[4].strip()
        if sDeviceType == "S":
            sInit = powerSwitch(iDeviceNum, iDeviceInst, sDeviceName, sServerAddress) 
            aSwitchArr.append(sInit)
    fConfFile.close()
    return True

def iFindSwitchNum(iSwitchNum, aSwitchArr):

    iFound = -1
    iArrPtr = 0

    while iArrPtr < len(aSwitchArr) and iFound == -1:
        if iSwitchNum == aSwitchArr[iArrPtr].iSwitchNum:
            iFound = iArrPtr
        iArrPtr += 1

    return iFound

def get_lighttoswitch(aSwitchArr):
    iInVal = 0
    bForEver = False
    while bForEver == False:
        vTmpIn = input("\nLight to switch (0 for exit) : ")
        try:
            iInVal = int(vTmpIn)
        except ValueError:
            print("Please enter an integer")
            iInVal = 0
        if iInVal == 0:
            return 0
        if iFindSwitchNum(iInVal, aSwitchArr) != -1:
            return iInVal
        else:
            print("Switch number : ", iInVal, " does not exist!")

def DisplayAllSwitchStat(aSwitchArr):
#    print("\nSwitch status report.\n")
    sTmpBuf = ""        
    for x in range(len(aSwitchArr)):
        sTmpBuf = sTmpBuf + str(aSwitchArr[x].iStatus())
#        print("Switch ", aSwitchArr[x].iSwitchNum, " - ", aSwitchArr[x].sSwitchName, " is ", aSwitchArr[x].sStatus())
    return sTmpBuf


# MAIN START 

aSwitchArr =  []
if aReadConfigFile(sDeviceConfigFileName, aSwitchArr) != False:

    bForEver = True

    while bForEver == True:

        print(DisplayAllSwitchStat(aSwitchArr))

        time.sleep(10)
