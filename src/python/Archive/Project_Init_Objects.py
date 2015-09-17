import httplib2
import json

sServerAddress = "192.168.0.79:8083"
httpRequest = httplib2.Http()

#sDeviceConfigFileName = "/mnt/nas/config.txt"
#SfName = "/mnt/nas/switch.inf"

sDeviceConfigFileName = "config.txt"

class powerSwitch:
    def __init__(self, iSwitchNum, iSwitchInst, sSwitchName, sServerAddress):
        self.iSwitchNum = iSwitchNum
        self.iSwitchInst = iSwitchInst
        self.sSwitchName = sSwitchName
        self.sServerAddress = sServerAddress
        self.iSwitchLastStatus = self.iStatus()

#    def compile_httprefresh(self):
#        sOutBuf = "http://" + self.sServerAddress + "/ZWaveAPI/Run/devices[" + str(self.iSwitchNum)
#        sOutBuf = sOutBuf + "].instances[" + str(self.iSwitchInst) + "].commandClasses[0x25].Get()"
#        return sOutBuf

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

class multiSensor:
    def __init__(self, iSensorNum, iSensorCommandClass, iSensorDataLevel, sSensorName, sSensorType, sSensorValue, sServerAddress):
        self.iSensorNum = iSensorNum
        self.iSensorCommandClass = iSensorCommandClass
        self.iSensorDataLevel = iSensorDataLevel
        self.sSensorName = sSensorName
        self.sSensorType = sSensorType
        self.sSensorValue = sSensorValue
        self.sServerAddress = sServerAddress
        self.iSensorLastValue = self.get_currentvalue() 

    def compile_httpgetvalue(self):
        sOutBuf = "http://192.168.0.79:8083/ZWaveAPI/Run/devices[" + str(self.iSensorNum)
        sOutBuf = sOutBuf + "].instances[0].commandClasses[" + str(self.iSensorCommandClass)
        sOutBuf = sOutBuf + "].data[" + str(self.iSensorDataLevel) + "].val.value"
        return sOutBuf

    def get_currentvalue(self):
        resp, content = httpRequest.request(self.compile_httpgetvalue(), "GET")
        try:
            DDevInfo = json.loads(content.decode('ascii'))
            return DDevInfo
        except (ValueError):
            return ""
      
def aReadConfigFile(sConfFileName, aSwitchArr, aSensorArr):

    try:
        fConfFile = open(sConfFileName, "r")
    except IOError:
        print("Cannot open file : ", sConfFileName)
        return False

    for sLine in fConfFile:
        rConfigRecord = sLine.split(",")

        if rConfigRecord[1].strip() =="M":
            iSensorId = int(rConfigRecord[0])
            sDeviceType = rConfigRecord[1].strip()
            iSensorNum = int(rConfigRecord[2])
            iSensorCommandClass = 49
            iSensorDataLevel = int(rConfigRecord[3])
            sSensorName = rConfigRecord[4].strip()
            sSensorType = rConfigRecord[5].strip()
            sSensorValue = rConfigRecord[6].strip()
            sInit = multiSensor(iSensorNum, iSensorCommandClass, iSensorDataLevel, sSensorName, sSensorType, sSensorValue, sServerAddress)
            aSensorArr.append(sInit)
        else:        
            iDeviceId = int(rConfigRecord[0])
            sDeviceType = rConfigRecord[1].strip()
            iDeviceNum = int(rConfigRecord[2])
            iDeviceInst = int(rConfigRecord[3])
            sDeviceName = rConfigRecord[4].strip()
            sInit = powerSwitch(iDeviceNum, iDeviceInst, sDeviceName, sServerAddress) 
            aSwitchArr.append(sInit)

    fConfFile.close()
    return True

# MAIN 

aSwitchArr = []
aSensorArr = []

if aReadConfigFile(sDeviceConfigFileName, aSwitchArr, aSensorArr) != False:
	
    for x in range(len(aSwitchArr)):
        print("Switch ", aSwitchArr[x].iSwitchNum, " - ", aSwitchArr[x].sSwitchName, " is ", aSwitchArr[x].sStatus(), " i :", aSwitchArr[x].iSwitchLastStatus)


    for x in range(len(aSensorArr)):
        print("Sensor ", aSensorArr[x].iSensorNum, " - ", aSensorArr[x].sSensorName, " - ", aSensorArr[x].sSensorType, " = ", aSensorArr[x].iSensorLastValue, aSensorArr[x].sSensorValue)
              
