import time
import httplib2
import json
#import tkinter
from tkinter import *

sServerAddress = "192.168.0.79:8083"
httpRequest = httplib2.Http()

#sDeviceConfigFileName = "/mnt/nas/config.txt#
sDeviceConfigFileName = "config.txt"

class SwitchGUI():
    def __init__(self, root, master):
        self.root = root
        self.master = master
        self.createWidgets()

    def createWidgets(self):
        Label(self.master, text="Your sex:").grid(row=0, sticky=W)
        self.var1 = IntVar()
        Checkbutton(self.master, text="male", variable=self.var1).grid(row=1, sticky=W)
        self.var2 = IntVar()
        Checkbutton(self.master, text="female", variable=self.var2).grid(row=2, sticky=W)
        Button(self.master, text='Quit', command=self.quit).grid(row=3, sticky=W, pady=4)
        Button(self.master, text='Show', command=self.var_states).grid(row=4, sticky=W, pady=4)

    def var_states(self):
        print("male: ", self.var1.get(), " female ", self.var2.get())
        if self.var1.get() == 1:
            self.var1.put(0)

    def quit(self):
        exit

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

# Temp


# MAIN START 

aSwitchArr =  []
bRetval = aReadConfigFile(sDeviceConfigFileName, aSwitchArr)

root = Tk()
app = SwitchGUI(root, None)
mainloop()


