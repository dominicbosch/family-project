from tkinter import *
import time
import httplib2
import json

sServerAddress = "192.168.0.79:8083"
httpRequest = httplib2.Http()

sDeviceConfigFileName = "/mnt/debian/config.txt"

class Application(Frame):
    def __init__(self, aSwitchArr, master=None):
        Frame.__init__(self, master)
        self.aSwitchArr = aSwitchArr
        self.pack()
        self.createWidgets()

    def displaySwitch(self):
        self.second_r_label["bg"] = "yellow"
        print("update switch status")

    def createWidgets(self):

        self.first_label = Label(self)
        self.first_label["text"] = "Büro"

        self.first_label.grid(row=1, column=1)
    
        self.first_r_label = Label(self)
        self.first_r_label["text"] = "     "
        self.first_r_label["bg"] = "yellow"

        self.first_r_label.grid(row=1, column=2)

        self.second_label = Label(self)
        self.second_label["text"] = "Gang"

        self.second_label.grid(row=2, column=1)
    
        self.second_r_label = Label(self)
        self.second_r_label["text"] = "     "
        self.second_r_label["bg"] = "black"

        self.second_r_label.grid(row=2, column=2)

        self.updateSwitch = Button(self)
        self.updateSwitch["text"] = "Update",
        self.updateSwitch["command"] = self.displaySwitch

        self.updateSwitch.grid(row=3, column=1)

        self.QUIT = Button(self)
        self.QUIT["text"] = "QUIT"
        self.QUIT["fg"]   = "red"
        self.QUIT["command"] =  self.quit

        self.QUIT.grid(row=3, column=2)
    
    
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

aSwitchArr =  []
bRetval = aReadConfigFile(sDeviceConfigFileName, aSwitchArr)

root = Tk()
app = Application(aSwitchArr, master=root)
app.mainloop()
root.destroy()
