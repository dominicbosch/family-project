import time
import httplib2
import json
import RPi.GPIO as GPIO

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

#OUTPUTS: map GPIO to LCD lines
LCD_RS = 7                 # Pin 26
LCD_E  = 8                 # Pin 24
LCD_D4 = 17                # Pin 11
LCD_D5 = 18                # Pin 12
LCD_D6 = 27                # Pin 13 (21 on Rev.1)
LCD_D7 = 22                # Pin 15
OUTPUTS = [LCD_RS, LCD_E, LCD_D4, LCD_D5, LCD_D6, LCD_D7]

#INPUTS: map GPIO to Switches
#SW1 = 4                    # Pin 7
#SW2 = 23                   # Pin 16
#SW3 = 10                   # Pin 19

SW1 = 10
SW2 = 23
SW3 = 4
SW4 = 9                    # Pin 21
INPUTS = [SW1, SW2, SW3, SW4]

#HD44780 Controller Commands
CLEARDISPLAY = 0x01
SETCURSOR    = 0x80

#Line Adress
LINE = [0x00, 0x40]

#### Low level GPIO routines

def initIO():
    #Sets GPIO pins to input & ouput
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    for lcdLine in OUTPUTS:
        GPIO.setup(lcdLine, GPIO.OUT)
    for switch in INPUTS:
        GPIO.setup(switch, GPIO.IN, pull_up_down=GPIO.PUD_UP)

def checkSwitches():
    #Check status of the Switches
    #Does return 4 boolean values as a tuple
    val1 = not GPIO.input(SW1)
    val2 = not GPIO.input(SW2)
    val3 = not GPIO.input(SW3)
    val4 = not GPIO.input(SW4)
    return (val4, val3, val2, val1)

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

### Higher level GPIO routines

def sendChar(ch):
    sendByte(ord(ch), True)

def showMessage(string):
    for character in string:
        sendChar(character)

def gotoLine(row):
    addr = LINE[row]
    sendByte(SETCURSOR + addr)

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

def IsDevInArr(iDevNum, iVarArr):
    iFoundDev = -1
    if len(iVarArr) > 0:
        ix = 0
        while iFoundDev == -1 and ix < len(iVarArr):
            if iDevNum == iVarArr[ix] [0]:
                iFoundDev = ix
            ix += 1
    return iFoundDev

h = httplib2.Http()

StopRun = False
iOldVelocity = 0
iSched = []
iCounter = 0

print("Application started, Ctrl-C to stop !\n")

initIO()
initLCD()

while StopRun == False:

    if iCounter == 0:

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
                        iRetVal = IsDevInArr(iDeviceId, iSched)
                        if iRetVal != -1:
                            if iSched[iRetVal] [2] != sDevStatus:
                                iSched[iRetVal] [1] = lRequestTime
                                iSched[iRetVal] [2] = sDevResp
                                print("Device updated : {} - Status : {}".format(sDeviceName, sDevStatus))
                                fObiS.write("{}, {}, {}\n".format(str(iDeviceNum), lRequestTime, sDevStatus))            
                            else:
                                print("Device unchanged : {}".format(sDeviceName))
                        else:
                            iOutBuf = [iDeviceId, lRequestTime, sDevStatus]
                            iSched.append(iOutBuf)
                            print("Device initialized : {} - Status : {}".format(sDeviceName, sDevStatus))
                            fObiS.write("{}, {}, {}\n".format(str(iDeviceNum), lRequestTime, sDevStatus))            
                    else:
                        print("Value Error thrown - ", time.ctime(time.time()))
              
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
                            print("Device changed : {} - Speed : {}".format(sDeviceName, sDevTemp))
                            fObiS.write("{}, {}, {}, {}\n".format(str(iDataLevel), sDeviceName, lRequestTime, sDevTemp))
                        else:
                            print("Device unchanged : {} - Speed : {}".format(sDeviceName, sDevTemp))
                    else:
                        print("Value Error thrown - ", time.ctime(time.time()))

            fObiS.close()
            fConfFile.close()
            
    gotoLine(0)
    sWindSpeedResult = "Wind " + str(iOldVelocity)
    showMessage(sWindSpeedResult)

    sOutBuf = ""
    for aSwitch in iSched:
        if iSched [aSwitch] [2] == "Off":
            sOutBuf = sOutBuf + "0"
        else:
            sOutBuf = sOutBuf + "1"

    gotoLine(1)
    showMessage(sOutBuf)
    time.sleep(0.1)

    StopRun = get_openfile(sStopFileName)    

    iCounter = iCounter + 1
    if iCounter >= 50:
        iCounter = 0

print("\nApplication halted !\n")
