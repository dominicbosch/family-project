from tkinter import *
import time
import httplib2
import json

sServerAddress = "192.168.0.79:8083"
httpRequest = httplib2.Http()

sDeviceConfigFileName = "config.txt"

class Application(Frame):
    def __init__(self, aSwitchArr, master=None):
        Frame.__init__(self, master)
        self.aSwitchArr = aSwitchArr
        self.label = []
        self.status = []
        self.pack()
        self.createWidgets()

    def displaySwitch(self):
        rowpos = 1
#
        if aSwitchArr[0].sStatus() == "On":
            self.init_status_1["text"] = "   On   "
            self.init_status_1["bg"] = "yellow"
            self.init_status_1["fg"] = "black"
        else:
            self.init_status_1["text"] = "  Off   "
            self.init_status_1["bg"] = "black"
            self.init_status_1["fg"] = "yellow"

        if aSwitchArr[1].sStatus() == "On":
            self.init_status_2["text"] = "   On   "
            self.init_status_2["bg"] = "yellow"
            self.init_status_2["fg"] = "black"
        else:
            self.init_status_2["text"] = "  Off   "
            self.init_status_2["bg"] = "black"
            self.init_status_2["fg"] = "yellow"

        if aSwitchArr[2].sStatus() == "On":
            self.init_status_3["text"] = "   On   "
            self.init_status_3["bg"] = "yellow"
            self.init_status_3["fg"] = "black"
        else:
            self.init_status_3["text"] = "  Off   "
            self.init_status_3["bg"] = "black"
            self.init_status_3["fg"] = "yellow"

        if aSwitchArr[3].sStatus() == "On":
            self.init_status_4["text"] = "   On   "
            self.init_status_4["bg"] = "yellow"
            self.init_status_4["fg"] = "black"
        else:
            self.init_status_4["text"] = "  Off   "
            self.init_status_4["bg"] = "black"
            self.init_status_4["fg"] = "yellow"

        if aSwitchArr[4].sStatus() == "On":
            self.init_status_5["text"] = "   On   "
            self.init_status_5["bg"] = "yellow"
            self.init_status_5["fg"] = "black"
        else:
            self.init_status_5["text"] = "  Off   "
            self.init_status_5["bg"] = "black"
            self.init_status_5["fg"] = "yellow"

        if aSwitchArr[5].sStatus() == "On":
            self.init_status_6["text"] = "   On   "
            self.init_status_6["bg"] = "yellow"
            self.init_status_6["fg"] = "black"
        else:
            self.init_status_6["text"] = "  Off   "
            self.init_status_6["bg"] = "black"
            self.init_status_6["fg"] = "yellow"

    def createWidgets(self):

        self.rowpos = 1
#
        self.init_label_1 = Label(self)
        self.init_label_1["text"] = aSwitchArr[0].sSwitchName
        self.init_label_1.grid(row  = self.rowpos, column = 1, sticky = W)

        self.init_status_1 = Label(self)
        if aSwitchArr[0].sStatus() == "On":
            self.init_status_1["text"] = "   On   "
            self.init_status_1["bg"] = "yellow"
            self.init_status_1["fg"] = "black"
        else:
            self.init_status_1["text"] = "  Off   "
            self.init_status_1["bg"] = "black"
            self.init_status_1["fg"] = "yellow"
        self.init_status_1.grid(row = self.rowpos, column = 2)

        self.rowpos = self.rowpos + 1
#

#
        self.init_label_2 = Label(self)
        self.init_label_2["text"] = aSwitchArr[1].sSwitchName
        self.init_label_2.grid(row  = self.rowpos, column = 1, sticky = W)

        self.init_status_2 = Label(self)
        if aSwitchArr[1].sStatus() == "On":
            self.init_status_2["text"] = "   On   "
            self.init_status_2["bg"] = "yellow"
            self.init_status_2["fg"] = "black"
        else:
            self.init_status_2["text"] = "  Off   "
            self.init_status_2["bg"] = "black"
            self.init_status_2["fg"] = "yellow"
        self.init_status_2.grid(row = self.rowpos, column = 2)

        self.rowpos = self.rowpos + 1
#

#
        self.init_label_3 = Label(self)
        self.init_label_3["text"] = aSwitchArr[2].sSwitchName
        self.init_label_3.grid(row  = self.rowpos, column = 1, sticky = W)

        self.init_status_3 = Label(self)
        if aSwitchArr[2].sStatus() == "On":
            self.init_status_3["text"] = "   On   "
            self.init_status_3["bg"] = "yellow"
            self.init_status_3["fg"] = "black"
        else:
            self.init_status_3["text"] = "  Off   "
            self.init_status_3["bg"] = "black"
            self.init_status_3["fg"] = "yellow"
        self.init_status_3.grid(row = self.rowpos, column = 2)

        self.rowpos = self.rowpos + 1
#

#
        self.init_label_4 = Label(self)
        self.init_label_4["text"] = aSwitchArr[3].sSwitchName
        self.init_label_4.grid(row  = self.rowpos, column = 1, sticky = W)

        self.init_status_4 = Label(self)
        if aSwitchArr[3].sStatus() == "On":
            self.init_status_4["text"] = "   On   "
            self.init_status_4["bg"] = "yellow"
            self.init_status_4["fg"] = "black"
        else:
            self.init_status_4["text"] = "  Off   "
            self.init_status_4["bg"] = "black"
            self.init_status_4["fg"] = "yellow"
        self.init_status_4.grid(row = self.rowpos, column = 2)

        self.rowpos = self.rowpos + 1
#

#
        self.init_label_5 = Label(self)
        self.init_label_5["text"] = aSwitchArr[4].sSwitchName
        self.init_label_5.grid(row  = self.rowpos, column = 1, sticky = W)

        self.init_status_5 = Label(self)
        if aSwitchArr[4].sStatus() == "On":
            self.init_status_5["text"] = "   On   "
            self.init_status_5["bg"] = "yellow"
            self.init_status_5["fg"] = "black"
        else:
            self.init_status_5["text"] = "  Off   "
            self.init_status_5["bg"] = "black"
            self.init_status_5["fg"] = "yellow"
        self.init_status_5.grid(row = self.rowpos, column = 2)

        self.rowpos = self.rowpos + 1
#

#
        self.init_label_6 = Label(self)
        self.init_label_6["text"] = aSwitchArr[5].sSwitchName
        self.init_label_6.grid(row  = self.rowpos, column = 1, sticky = W)

        self.init_status_6 = Label(self)
        if aSwitchArr[5].sStatus() == "On":
            self.init_status_6["text"] = "   On   "
            self.init_status_6["bg"] = "yellow"
            self.init_status_6["fg"] = "black"
        else:
            self.init_status_6["text"] = "  Off   "
            self.init_status_6["bg"] = "black"
            self.init_status_6["fg"] = "yellow"
        self.init_status_6.grid(row = self.rowpos, column = 2)

        self.rowpos = self.rowpos + 1

#

        self.updateSwitch = Button(self)
        self.updateSwitch["text"] = "Update",
        self.updateSwitch["command"] = self.displaySwitch

        self.updateSwitch.grid(row=self.rowpos, column=1)

        self.QUIT = Button(self)
        self.QUIT["text"] = "QUIT"
        self.QUIT["fg"]   = "red"
        self.QUIT["command"] =  self.quit

        self.QUIT.grid(row=self.rowpos, column=2)
    
    
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

def task():
    print("After ")
    app.displaySwitch
    root.after(2000,task)

print("Application started")

aSwitchArr =  []
bRetval = aReadConfigFile(sDeviceConfigFileName, aSwitchArr)

root = Tk()
print("Init Application")
app = Application(aSwitchArr, master=root)
print("Root After")
task()

#app.mainloop()
#root.destroy()
