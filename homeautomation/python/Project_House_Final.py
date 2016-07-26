import httplib2
import json
import time
import datetime
import RPi.GPIO as GPIO

sServerAddress = "192.168.0.79:8083"
httpRequest = httplib2.Http()

#sDeviceConfigFileName = "/mnt/nas/config.txt"
#SfName = "/mnt/nas/switch.inf"

sDeviceConfigFileName = "config.txt"
sSFileName = "SwitchDevices.inf"
sOFileName = "OtherDevices.inf"

#OUTPUTS: map GPIO to LCD lines
LCD_RS = 7                 # Pin 26
LCD_E  = 8                 # Pin 24
LCD_D4 = 17                # Pin 11
LCD_D5 = 18                # Pin 12
LCD_D6 = 27                # Pin 13
LCD_D7 = 22                # Pin 15
OUTPUTS = [LCD_RS, LCD_E, LCD_D4, LCD_D5, LCD_D6, LCD_D7]

#INPUTS: map GPIO to Switches
SW1 = 10
SW2 = 23
SW3 = 4
SW4 = 9
INPUTS = [SW1, SW2, SW3, SW4]

#HD44780 Controller Commands
CLEARDISPLAY = 0x01
RETURNHOME   = 0x02
RIGHTTOLEFT  = 0x04
LEFTTORIGHT  = 0x06
DISPLAYOFF   = 0x08
CURSOROFF    = 0x0C
CURSORON     = 0x0E
CURSORBLINK  = 0x0F
CURSORLEFT   = 0x10
CURSORRIGHT  = 0x14
LOADSYMBOL   = 0x40
SETCURSOR    = 0x80

#Line Adress
LINE = [0x00, 0x40]

#My Symbols
aLight  = [
[0x1F, 0x11, 0x11, 0x11, 0x11, 0x11, 0x11, 0x1F],
[0x1F, 0x1F, 0x1F, 0x1F, 0x1F, 0x1F, 0x1F, 0x1F] 
]

#### Low level routines

def initIO():
    #Sets GPIO pins to input & ouput
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    for lcdLine in OUTPUTS:
        GPIO.setup(lcdLine, GPIO.OUT)
    for switch in INPUTS:
        GPIO.setup(switch, GPIO.IN, pull_up_down=GPIO.PUD_UP)

def initEvents():
    GPIO.add_event_detect(SW1, GPIO.FALLING, callback=callBack)
    GPIO.add_event_detect(SW2, GPIO.FALLING, callback=callBack)
    GPIO.add_event_detect(SW3, GPIO.FALLING, callback=callBack)
    GPIO.add_event_detect(SW4, GPIO.FALLING, callback=callBack)

def checkSwitches():
    #Check status of the Switches
    #Does return 4 boolean values as a tuple
    val1 = not GPIO.input(SW1)
    val2 = not GPIO.input(SW2)
    val3 = not GPIO.input(SW3)
    val4 = not GPIO.input(SW4)
    return (val4, val3, val2, val1)

def callBack(channel):
    #Handle events (switch pressed)
    pass

def pulseEnableLine():
    #Pules the LCD enable line, used for clocking in data
    mSec = 0.0005
    time.sleep(mSec)
    GPIO.output(LCD_E, GPIO.HIGH)
    time.sleep(mSec)
    GPIO.output(LCD_E, GPIO.LOW)
    time.sleep(mSec)

def sendNibble(data):
    #does send upper 4 bits of data byte to LCD data pins D4-D7
    GPIO.output(LCD_D4, bool(data & 0x10))
    GPIO.output(LCD_D5, bool(data & 0x20))
    GPIO.output(LCD_D6, bool(data & 0x40))
    GPIO.output(LCD_D7, bool(data & 0x80))

def sendByte(data, charMode=False):
    #send one byte to LCD controller
    GPIO.output(LCD_RS,charMode)
    sendNibble(data)
    pulseEnableLine()
    data = (data & 0x0F) << 4
    sendNibble(data)
    pulseEnableLine()

def initLCD():
    #initialize the LCD controller and clear display
    sendByte(0x33)          # initialize
    sendByte(0x32)          # set to 4-bit mode
    sendByte(0x28)          # 2 line, 5 *7 matrix
    sendByte(0x0C)          # turn cursor off (0x0E to enable)
    sendByte(0x06)          # shift cursor right
    sendByte(CLEARDISPLAY)  #remove any stray characters on display

### Higher level routines

def clearDisplay():
    sendByte(CLEARDISPLAY)
    time.sleep(0.0015)

def cursorOn():
    sendByte(CURSORON)

def cursorOff():
    sendByte(CURSOROFF)

def cursorBlink():
    sendByte(CURSORBLINK)

def cursorLEFT():
    sendByte(CURSORLEFT)

def cursorRIGHT():
    sendByte(CURSORRIGHT)

def sendChar(ch):
    sendByte(ord(ch), True)

def showMessage(string):
    for character in string:
        sendChar(character)

def gotoLine(row):
    addr = LINE[row]
    sendByte(SETCURSOR + addr)

def gotoXY(row, col):
    addr = LINE[row] + col
    sendByte(SETCURSOR + addr)
    
#Custome Character generation

def loadCustomSymbol(addr, data):
    cmd = LOADSYMBOL + (addr<<3)
    sendByte(cmd)
    for byte in data:
        sendByte(byte, True)

def loadSymbolBlock(data):
    for i in range(len(data)):
        loadCustomSymbol(i,data[i])

class powerSwitch:
    def __init__(self, iSwitchNum, iSwitchInst, sSwitchName, sServerAddress):
        self.Num = iSwitchNum
        self.Inst = iSwitchInst
        self.Name = sSwitchName
        self.ServerAddress = sServerAddress
        self.LastStatus = self.iStatus()

    def compile_httprefresh(self):
        sOutBuf = "http://" + self.ServerAddress + "/ZWaveAPI/Run/devices[" + str(self.Num)
        sOutBuf = sOutBuf + "].instances[" + str(self.Inst) + "].commandClasses[0x25].Get()"
        return sOutBuf

    def compile_httpgetstat(self):
        sOutBuf = "http://" + self.ServerAddress + "/ZWaveAPI/Run/devices[" + str(self.Num)
        sOutBuf = sOutBuf + "].instances[" + str(self.Inst) + "].commandClasses[0x25].data.level"
        return sOutBuf

    def compile_httpset(self, iSwitchStat):
        sOutBuf = "http://" + self.ServerAddress+ "/ZWaveAPI/Run/devices[" + str(self.Num)
        sOutBuf = sOutBuf + "].instances[" + str(self.Inst)+ "].commandClasses[0x25].Set(" + str(iSwitchStat)
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
    def __init__(self, iSensorNum, iSensorCommandClass, iSensorDataLevel, sSensorName, sSensorType, sSensorMeasure, sServerAddress):
        self.Num = iSensorNum
        self.CommandClass = iSensorCommandClass
        self.DataLevel = iSensorDataLevel
        self.Name = sSensorName
        self.Type = sSensorType
        self.Measure = sSensorMeasure
        self.ServerAddress = sServerAddress
        self.LastValue = self.get_currentvalue() 

    def compile_httpgetvalue(self):
        sOutBuf = "http://192.168.0.79:8083/ZWaveAPI/Run/devices[" + str(self.Num)
        sOutBuf = sOutBuf + "].instances[0].commandClasses[" + str(self.CommandClass)
        sOutBuf = sOutBuf + "].data[" + str(self.DataLevel) + "].val.value"
        return sOutBuf

    def get_currentvalue(self):
        resp, content = httpRequest.request(self.compile_httpgetvalue(), "GET")
        try:
            DDevInfo = json.loads(content.decode('ascii'))
            return DDevInfo
        except (ValueError):
            return ""

def iFindSwitchNum(iSwitchNum, aSwitchArr):

    iFound = -1
    iArrPtr = 0

    while iArrPtr < len(aSwitchArr) and iFound == -1:
        if iSwitchNum == aSwitchArr[iArrPtr].Num:
            iFound = iArrPtr
        iArrPtr += 1

    return iFound
      
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
            iDeviceNum = int(rConfigRecord[2])
            iDeviceInst = int(rConfigRecord[3])
            sDeviceName = rConfigRecord[4].strip()
            sInit = powerSwitch(iDeviceNum, iDeviceInst, sDeviceName, sServerAddress) 
            aSwitchArr.append(sInit)

    fConfFile.close()
    return True

def getOpenfile(sFileName, mode):
    try:
        tobj = open(sFileName, mode)
        return tobj
    except (IOError, TypeError):
        print("Cannot open/create file :", sFileName)
        return False

def writeFile(oFile, iDeviceNum, dValue):
    lRequestTime = time.time()
    oFile.write("{}, {}, {}\n".format(str(iDeviceNum), lRequestTime, dValue))

def readDeviceFile(oFile, rOutBuf, select_week, select_day):

#Outbuf [0]  = Switch Number
#       [1]  = Time Stamp
#       [2]  = 0 / Off - 1 / On
#       [3]  = Year
#       [4]  = Month
#       [5]  = Day of Month
#       [6]  = Hour
#       [7]  = Minute
#       [8]  = Second
#       [9]  = Week in Year
#       [10] = Week Day
#       [11] = Processed ? (initial = False)

    recordsRead = -1

    for line in oFile:

        sOutBuf = line.split(",")
        sOutBuf[2] = sOutBuf[2].strip()

        if sOutBuf[2].find("Off") != -1:
            sOutBuf[2] = 0
        else:
            if sOutBuf[2].find("On") != -1:
                sOutBuf[2] = 1

        t = time.gmtime(float(sOutBuf[1]))
        sOutBuf.append(int(t.tm_year))
        sOutBuf.append(int(t.tm_mon))
        sOutBuf.append(int(t.tm_mday))
        sOutBuf.append(int(t.tm_hour))
        sOutBuf.append(int(t.tm_min))
        sOutBuf.append(int(t.tm_sec))
        tm_wyear = datetime.date(int(t.tm_year), int(t.tm_mon), int(t.tm_mday)).isocalendar()[1]
        sOutBuf.append(tm_wyear)
        sOutBuf.append(int(t.tm_wday))
        sOutBuf.append(False)

        if select_week != -1 and tm_wyear == select_week and int(t.tm_wday) == select_day:
                recordsRead = recordsRead + 1
                rOutBuf.append(sOutBuf)

    return recordsRead

def clcTimeDiff(iHour, iMin, iSec):
    t = time.gmtime(time.time())
    iDiff = (iHour - int(t.tm_hour)) * 3600 + (iMin - int(t.tm_min)) * 60 + (iSec - int(t.tm_sec))
    return iDiff

def processQueue(Queue, Switch):

    t = time.gmtime(time.time())
    print("Start -> ", t.tm_hour, ":", t.tm_min)

    for x in range(len(Queue)):
        if Queue[x] [11] == False:
            currTime = (t.tm_hour * 60) + t.tm_min
            if currTime >= ((Queue[x] [6] * 60) + Queue[x] [7]):
                print(Queue[x] [6], ":", Queue[x] [7], " - Switch #", Queue[x] [0], " to ", Queue[x] [2])
                sNum = iFindSwitchNum(int(Queue[x] [0]), Switch)
                if sNum != -1:
                    Queue[x] [11] = True
                    Switch[sNum].LastStatus = int(Queue[x] [2])
    for x in range(len(Switch)):
        print("Initializing Switch ", Switch[x].Num, " to ", Switch[x].LastStatus)
        Switch[x].SwitchTo(Switch[x].LastStatus)            

    afterOne = False
    forToday = True

    while forToday:

        if t.tm_hour > 1:
            afterOne = True

        for x in range(len(Queue)):
            if Queue[x] [11] == False:
                currTime = (t.tm_hour * 60) + t.tm_min
                if currTime >= ((Queue[x] [6] * 60) + Queue[x] [7]):
                    print(Queue[x] [6], ":", Queue[x] [7], " - Switch #", Queue[x] [0], " to ", Queue[x] [2])
                    iSwitch = iSwitchNum(Queue[x] [0])
                    Switch[iSwitch].SwitchTo(Queue[x] [2])
                    Queue[x] [11] = True

        if t.tm_hour == 0 and afterOne == True:
            forToday = False

        time.sleep(5)

# MAIN 

print("Program started !")

initIO()
initEvents()
initLCD()
loadSymbolBlock(aLight)

showMessage('Pi Symbol Test !')

#gotoXY(1,0)
#sendByte(0,True)
#gotoXY(1,1)
#sendByte(1,True)

#gotoXY(1,3)
#showMessage("Waiting")

Switch = []
Sensor = []

if aReadConfigFile(sDeviceConfigFileName, Switch, Sensor) != False:

    print("Configuration read !")

    Forever = True
    while Forever:

        t = time.gmtime(time.time())
        tm_wyear = datetime.date(int(t.tm_year), int(t.tm_mon), int(t.tm_mday)).isocalendar()[1] - 3
        sa_wyear = datetime.date(int(t.tm_year), int(t.tm_mon), int(t.tm_mday)).isocalendar()[1]
        tm_wday = int(t.tm_wday)

        print("Reading switch file, for today")

        oSFile = getOpenfile(sSFileName, "r")
        if oSFile != False:
            pass
        else:
            Forever = False

        aSBuf = []
        while readDeviceFile(oSFile, aSBuf, tm_wyear, tm_wday) == -1:
            tm_wday = tm_wday + 1
            if tm_wday == 7:
                tm_wyear = tm_wyear + 1 
                tm_wday = 0
            if tm_wyear >= sa_wyear:
                print("Could not find data for week ", sa_wyear)
                sys.exit(0)
                
        print("Set all switches to off")

        for x in range(len(Switch)):
            Switch[x].Off()
            Switch[x].lastStatus = 0
            
        processQueue(aSBuf, Switch)
