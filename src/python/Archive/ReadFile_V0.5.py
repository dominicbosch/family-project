import time
import datetime
import random
import sched

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

fobj = open(SfName,"r")
i = 1
iRecordsOk = 0
sWorkData=[]
sWorkBuf=[]

iOldDay = 0
iWeekCount = 1

def LimitArray(sInBuf, iWeek, iDay):
    sTmpBuf=[]
    for x in range(len(sInBuf)):
        if (sInBuf[x] [3] == iWeek) and (sInBuf[x] [4] == iDay):
            sSwitchStat = sInBuf[x] [10]
            if sSwitchStat.find("Off") != -1:
                iSwitchStat = 0
            else: 
                iSwitchStat = 1       

#            sWorkBuf = [int(sInBuf[x] [0]), iSwitchStat, sInBuf[x] [7], sInBuf[x] [8], sInBuf[x] [9]]
#            sTmpBuf.append(sWorkBuf)
    return sTmpBuf

for line in fobj:
    i = i + 1
    sOutBuf = line.split(",")
    if sOutBuf[0].find("error") == -1:

        t = time.gmtime(float(sOutBuf[1]))
        
        iRecordsOk = iRecordsOk +1

        if iRecordsOk >= 2:
            if (int(t.tm_wday) == 0) and (int(sWorkBuf[4]) == 6):
                iWeekCount = iWeekCount+1
        
        sWorkBuf = [sOutBuf[0], int(t.tm_year), int(t.tm_mon), iWeekCount, int(t.tm_wday), int(t.tm_mday), int(t.tm_yday), int(t.tm_hour), int(t.tm_min), int(t.tm_sec), sOutBuf[2]]
        sWorkData.append(sWorkBuf)
        
fobj.close()

print(sWorkBuf)

iLastIndex = len(sWorkData)-1

iStartDay = int(sWorkData[0][6])
iStartYear = int(sWorkData[0][1])
iEndDay = int(sWorkData[iLastIndex][6])
iEndYear = int(sWorkData[iLastIndex][1])
   
print("Number of records read :", str(i), " Records ok : ", str(iRecordsOk), "\n")
print("Start day : {} - Start year : {}\n".format(str(iStartDay).strip(), str(iStartYear).strip()))
print("End day   : {} - End year   : {}\n".format(str(iEndDay).strip(), str(iEndYear).strip()))

iStartDay = (iStartYear * 365) + iStartDay
iEndDay = (iEndYear * 365) + iEndDay
iNWeeks = int((iEndDay - iStartDay)/7)
print("Number of weeks in file {} - counted {}\n".format(iNWeeks, iWeekCount))

iSelWeek = random.randint(1, iNWeeks)
d = datetime.date.today()
iSelDay = d.isoweekday()-1

print("For today I would choose week number : {} and day number : {}\n".format (iSelWeek, iSelDay))

sSelData = LimitArray(sWorkData, iSelWeek, iSelDay)

print(str(len(sSelData)))

#for x in range(len(sSelData)):
#    pass

#print(str(sSelData[x-1] [0]), sSelData[x-1] [1], sSelData[x-1] [2], sSelData[x-1] [3], sSelData[x-1] [4])
    
    
