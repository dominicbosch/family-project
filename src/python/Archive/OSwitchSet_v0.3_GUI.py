import time
import httplib2
import json
import tkinter

sServerAddress = "192.168.0.79:8083"
httpRequest = httplib2.Http()

#sDeviceConfigFileName = "/mnt/nas/config.txt#
sDeviceConfigFileName = "config.txt"

class FirstGUI(tkinter.Frame):
    def __init__(self, master=None):
        tkinter.Frame.__init__(self, master)
        self.pack()
        self.createWidgets()

    def createWidgets(self):
        self.nameEntry = tkinter.Entry(self)
        self.nameEntry.pack()
        self.name = tkinter.StringVar()
        self.name.set("Your Name...")
        self.nameEntry["textvariable"] =self.name

        self.ok = tkinter.Button(self)
        self.ok["text"] = "Ok"
        self.ok["command"] = self.quit
        self.ok.pack(side="right")

        self.rev = tkinter.Button(self)
        self.rev["text"] = "Reverse"
        self.rev["command"] = self.onReverse
        self.rev.pack(side="right")

    def onReverse(self):
        self.name.set(self.name.get()[::-1])

class SecondGUI(tkinter.Frame):
    def __init__(self, master=None):
        tkinter.Frame.__init__(self, master)
        self.pack()
        self.createWidgets()
        self.createBindings()

    def createWidgets(self):
        self.label = tkinter.Label(self)
        self.label.pack()
        self.label["text"] = "Please send an event"

        self.entry = tkinter.Entry(self)
        self.entry.pack()

        self.ok = tkinter.Button(self)
        self.ok.pack()
        self.ok["text"] = "End"
        self.ok["command"] = self.quit

    def createBindings(self):
        self.entry.bind("Entenhausen", self.eventEntenhausen)
        self.entry.bind("<ButtonPress-1>", self.eventMouseClick)
        self.entry.bind("<MouseWheel>", self.eventMouseWheel)

    def eventEntenhausen(self, event):
        self.label["text"] = "You know the secret password"

    def eventMouseClick(self, event):
        self.label["text"] = "Mouseclick at position " \
                             "({},{}".format(event.x, event.y)
    def eventMouseWheel(self, event):
        if event.delta < 0:
            self.label["text"] = "Please turn the other way"
        else:
            self.label["text"] = "Thank you"

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
    print("\nSwitch status report.\n")
    for x in range(len(aSwitchArr)):
        print("Switch ", aSwitchArr[x].iSwitchNum, " - ", aSwitchArr[x].sSwitchName, " is ", aSwitchArr[x].sStatus())

# MAIN START 

aSwitchArr =  []
bRetval = aReadConfigFile(sDeviceConfigFileName, aSwitchArr)
    
root = tkinter.Tk()
#app = FirstGUI(root)
app = SecondGUI(root)
app.mainloop()

#if aReadConfigFile(sDeviceConfigFileName, aSwitchArr) != False:

#    bForEver = True
#    while bForEver == True:
#        DisplayAllSwitchStat(aSwitchArr)
#        iDeviceNum = get_lighttoswitch(aSwitchArr)

#        if iDeviceNum !=0:
#            iSwitchNum = iFindSwitchNum(iDeviceNum, aSwitchArr)
#            if aSwitchArr[iSwitchNum].iStatus() == 0:
#                aSwitchArr[iSwitchNum].On()
#            else:
#                aSwitchArr[iSwitchNum].Off()
#        else:
#            bForEver = False

