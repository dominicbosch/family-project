import time
import datetime
import random
import sched
import httplib2

#sFile Structure
#0 Device Number
#1 Date / Time Stamp
#2 Status (on/off)

#sWorkData Array
#0   = Switch Number
#1   = Year
#2   = Month
#3   = Week Count
#4   = Day in week
#5   = Day in month
#6   = Day in year
#7   = Hour
#8   = Minute
#9   = Second
#10  = Status (On/Off)

SfName = "/mnt/debian/switch.inf"
#SfName = "/mnt/nas/switch.inf"

httpOut = httplib2.Http()
scheduler = sched.scheduler(time.time, time.sleep)
i = 1
iRecordsOk = 0
sWorkData=[]
sWorkBuf=[]

iOldDay = 0
iWeekCount = 1

def print_event(event_text):
    print('EVENT:', event_text)

def compile_httpset(IDeviceNum, IDeviceSet):
    sOutBuf = "http://192.168.0.79:8083/ZWaveAPI/Run/devices[" + str(IDeviceNum)
    sOutBuf = sOutBuf + "].instances[0].commandClasses[0x25].Set(" + str(IDeviceSet)
    sOutBuf = sOutBuf + ")"
    return sOutBuf

def switch_light(iDeviceNum, iDeviceSet):
    print("Switching device : ", str(iDeviceNum), " to : ", str(iDeviceSet))
    resp, content = httpOut.request(compile_httpset(iDeviceNum, iDeviceSet), "GET")

def IsDevInArr(iDevNum, iVarArr):
    iFoundDev = -1
    if len(iVarArr) > 0:
        ix = 0
        while iFoundDev == -1 and ix < len(iVarArr):
            if iDevNum == iVarArr[ix] [0]:
                iFoundDev = ix
            ix += 1
    return iFoundDev

def ClcTimeDiff(iHour, iMin, iSec):
    t = time.localtime(time.time())
    iDiff = (iHour - t.tm_hour) * 3600 + (iMin - t.tm_min) * 60 + (iSec - t.tm_sec)
    return iDiff

def InitSwitches(vSwitchArr):
    if len(vSwitchArr) > 0:
        ix = 0
        while ix < len(vSwitchArr):
            switch_light(vSwitchArr[ix] [0], vSwitchArr[ix][1])
            print("Initializing switch ", vSwitchArr[ix] [0], " to ", vSwitchArr[ix] [1])
            ix += 1

def LimitArray(sInBuf, iWeek, iDay):

    now = time.time()

    iSwitchNum = 2

    iTimeDiff = ClcTimeDiff(19, 30, 00)
    iSwitchStat = 1
    vRetVal = scheduler.enterabs(now + iTimeDiff, 1, switch_light, (iSwitchNum, iSwitchStat))                       
    print("New Event for Switch : ", iSwitchNum, " -> Return value : ", vRetVal)

    iTimeDiff = ClcTimeDiff(19, 40, 00)
    iSwitchStat = 0
    vRetVal = scheduler.enterabs(now + iTimeDiff, 1, switch_light, (iSwitchNum, iSwitchStat))                       
    print("New Event for Switch : ", iSwitchNum, " -> Return value : ", vRetVal)

    iTimeDiff = ClcTimeDiff(20, 30, 00)
    iSwitchStat = 1
    vRetVal = scheduler.enterabs(now + iTimeDiff, 1, switch_light, (iSwitchNum, iSwitchStat))                       
    print("New Event for Switch : ", iSwitchNum, " -> Return value : ", vRetVal)

    iTimeDiff = ClcTimeDiff(19, 40, 00)
    iSwitchStat = 0
    vRetVal = scheduler.enterabs(now + iTimeDiff, 1, switch_light, (iSwitchNum, iSwitchStat))                       
    print("New Event for Switch : ", iSwitchNum, " -> Return value : ", vRetVal)

    iSwitchNum = 9

    iTimeDiff = ClcTimeDiff(19, 30, 00)
    iSwitchStat = 1
    vRetVal = scheduler.enterabs(now + iTimeDiff, 1, switch_light, (iSwitchNum, iSwitchStat))                       
    print("New Event for Switch : ", iSwitchNum, " -> Return value : ", vRetVal)

    iTimeDiff = ClcTimeDiff(19, 40, 00)
    iSwitchStat = 0
    vRetVal = scheduler.enterabs(now + iTimeDiff, 1, switch_light, (iSwitchNum, iSwitchStat))                       
    print("New Event for Switch : ", iSwitchNum, " -> Return value : ", vRetVal)

    iTimeDiff = ClcTimeDiff(20, 30, 00)
    iSwitchStat = 1
    vRetVal = scheduler.enterabs(now + iTimeDiff, 1, switch_light, (iSwitchNum, iSwitchStat))                       
    print("New Event for Switch : ", iSwitchNum, " -> Return value : ", vRetVal)

    iTimeDiff = ClcTimeDiff(19, 40, 00)
    iSwitchStat = 0
    vRetVal = scheduler.enterabs(now + iTimeDiff, 1, switch_light, (iSwitchNum, iSwitchStat))                       
    print("New Event for Switch : ", iSwitchNum, " -> Return value : ", vRetVal)

    scheduler.run()
                    
#fobj = open(SfName,"r")
#for line in fobj:
#    i = i + 1
#    sOutBuf = line.split(",")
#    if sOutBuf[0].find("error") == -1:

#        t = time.gmtime(float(sOutBuf[1]))
        
#        iRecordsOk = iRecordsOk +1

#        if iRecordsOk >= 2:
#            if (int(t.tm_wday) == 0) and (int(sWorkBuf[4]) == 6):
#                iWeekCount = iWeekCount+1
        
#        sWorkBuf = [sOutBuf[0], int(t.tm_year), int(t.tm_mon), iWeekCount, int(t.tm_wday), int(t.tm_mday), int(t.tm_yday), int(t.tm_hour), int(t.tm_min), int(t.tm_sec), sOutBuf[2]]
#        sWorkData.append(sWorkBuf)
        
# fobj.close()

# iLastIndex = len(sWorkData)-1

#iStartDay = int(sWorkData[0][6])
#iStartYear = int(sWorkData[0][1])
#iEndDay = int(sWorkData[iLastIndex][6])
#iEndYear = int(sWorkData[iLastIndex][1])
   
#print("Number of records read :", str(i), " Records ok : ", str(iRecordsOk), "\n")
#print("Start day : {} - Start year : {}\n".format(str(iStartDay).strip(), str(iStartYear).strip()))
#print("End day   : {} - End year   : {}\n".format(str(iEndDay).strip(), str(iEndYear).strip()))

#iStartDay = (iStartYear * 365) + iStartDay
#iEndDay = (iEndYear * 365) + iEndDay
#iNWeeks = int((iEndDay - iStartDay)/7)
#print("Number of weeks in file {} - counted {}\n".format(iNWeeks, iWeekCount))

bForEver = True

while bForEver:

#    iSelWeek = random.randint(1, iNWeeks)

#    iSelWeek = iNWeeks-2
#    d = datetime.date.today()
#    iSelDay = d.isoweekday()-1

#    print("For today I would choose week number : {} and day number : {}\n".format (iSelWeek, iSelDay))

    sWorkData = []
    iSelWeek = 1
    iSelDay = 1
#    LimitArray(sWorkData, iSelWeek, iSelDay)

    now = time.time()
#    iSecWait = ClcTimeDiff(23, 59, 59) + 10

    iSecWait = 10

    print("Waiting ", str(iSecWait), " seconds !")
    vRetVal = scheduler.enterabs(now + iSecWait, 1, print_event, ("Starting a new day.",))
    scheduler.run()

