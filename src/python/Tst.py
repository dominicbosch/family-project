import time
import sched

def IsDevInArr(iDevNum, iVarArr):
    iFoundDev = -1
    if len(iVarArr) > 0:
        x = 0
        while iFoundDev == -1 and x <= len(iVarArr):
            if iDevNum == iVarArr[x] [0]:
                iFoundDev = x
    return iFoundDev

def ClcTimeDiff(iLvar):
    t = time.localtime(time.time())
    iDiff = (iLvar[1] - t.tm_hour) * 3600 + (iLvar[2] - t.tm_min) * 60 + (iLvar[3] - t.tm_sec)
    return iDiff
    
sWorkData = []

print(len(sWorkData))

print(IsDevInArr(10, sWorkData))

t = time.localtime(time.time())
print(str(t.tm_hour), str(t.tm_min), str(t.tm_sec))

iDevNum = 10
iHour = 19
iMin = 20
iSec = 30
iDevStatus = 0

sOutBuf = [iDevNum, iHour, iMin, iSec]

sWorkData.append(sOutBuf)

print(len(sWorkData))

print("Dev In arr = ", IsDevInArr(10, sWorkData))

print(ClcTimeDiff(sWorkData[0]))

