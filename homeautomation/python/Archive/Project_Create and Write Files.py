import time

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

def readDeviceFile(oFile, rOutBuf):
    for line in oFile:
        sOutBuf = line.split(",")
# strip away the carriage return after the last field
        sOutBuf[2] = sOutBuf[2].strip()

# replace On and Off
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
        rOutBuf.append(sOutBuf)

def clcTimeDiff(iHour, iMin, iSec):
    t = time.gmtime(time.time())
    iDiff = (iHour - int(t.tm_hour)) * 3600 + (iMin - int(t.tm_min)) * 60 + (iSec - int(t.tm_sec))
    return iDiff

oSFile = getOpenfile(sSFileName, "a")
if oSFile == False:
    quit()

oOFile = getOpenfile(sOFileName, "a")
if oOFile == False:
    oSFile.close()
    quit()

writeFile(oSFile, 1, "On")
writeFile(oOFile, 12, 144)

oSFile.close()
oOFile.close()

oSFile = getOpenfile(sSFileName, "r")
if oSFile == False:
    quit()

oOFile = getOpenfile(sOFileName, "r")
if oOFile == False:
    oSFile.close()
    quit()

aSBuf = []
readDeviceFile(oSFile, aSBuf)

aOBuf = []
readDeviceFile(oOFile, aOBuf)

oSFile.close()
oOFile.close()

for x in range(len(aSBuf)):
#    print(aSBuf[x])
    print(clcTimeDiff(aSBuf[x] [6] + 1, aSBuf[x] [7], aSBuf[x] [8]))

for x in range(len(aOBuf)):
#    print (aOBuf[x])
    print(clcTimeDiff(aOBuf[x] [6] + 1, aOBuf[x] [7], aOBuf[x] [8]))
