import httplib2
import json

sServerAddress = "192.168.0.79:8083"
h = httplib2.Http()

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
        
    def status(self):
        resp, content = h.request(self.compile_httprefresh(), "GET")
        resp, content = h.request(self.compile_httpgetstat(), "GET")
        try:
            dDevInfo = json.loads(content.decode('ascii'))
            bDevStatus = dDevInfo['value']
            if bDevStatus == True:
                sDevStatus = "On"
            else:
                sDevStatus = "Off"
            print("Switch : ", self.sSwitchName, " - Status : ", sDevStatus)
            return sDevStatus
        except (ValueError):
            return ""
    
    def On(self):
        resp, content = h.request(self.compile_httpset(1), "GET")
        iLoopCounter = 0
        while self.status() != "On" and iLoopCounter < 10:
            resp, content = h.request(self.compile_httpset(1), "GET")
            iLoopCounter = iLoopCounter + 1
        if self.status() != "On":
            print("Did not Switch to on")
        else:
            print("Set to on")

    def Off(self):
        resp, content = h.request(self.compile_httpset(0), "GET")


sInit = powerSwitch(2, 0, "Büro", sServerAddress)
sRetval = sInit.status()

sInit.On()

sInit.Off()
sRetval = sInit.status()


#s=[]

#sInit=powerSwitch("1", "Uno", sServerAddress)
#s.append(sInit)
#sInit=powerSwitch("2", "Due", sServerAddress)
#s.append(sInit)

#s[0].status()
#s[1].status()
