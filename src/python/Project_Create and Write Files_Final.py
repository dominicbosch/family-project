import time
import datetime

sSFileName = "SwitchDevices.inf"
sOFileName = "OtherDevices.inf"

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

        if select_week != -1 and tm_wyear == select_week and int(t.tm_wday) == select_day:
                rOutBuf.append(sOutBuf)

def clcTimeDiff(iHour, iMin, iSec):
    t = time.gmtime(time.time())
    iDiff = (iHour - int(t.tm_hour)) * 3600 + (iMin - int(t.tm_min)) * 60 + (iSec - int(t.tm_sec))
    return iDiff

oSFile = getOpenfile(sSFileName, "r")
if oSFile == False:
    quit()

t = time.gmtime(time.time())
tm_wyear = datetime.date(int(t.tm_year), int(t.tm_mon), int(t.tm_mday)).isocalendar()[1] - 2
tm_wday = int(t.tm_wday)

aSBuf = []
readDeviceFile(oSFile, aSBuf, tm_wyear, tm_wday)

oSFile.close()

for x in range(len(aSBuf)):
    print(aSBuf[x])

