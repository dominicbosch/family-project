import time
import datetime
import random

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
iStartUDay = -1
sWorkData=[]
sWorkBuf=[]

iOldDay = 0
iWeekCount = 0

for line in fobj:
    i = i + 1
    sOutBuf = line.split(",")
    if sOutBuf[0].find("error") == -1:

        if iStartUDay == -1:
            iStartUDay = int(sOutBuf[1])
        elif int(sOutBuf[1]) < iStartUDay:
            iStartUDay = int(sOutBuf[1])

        iRecordsOk = iRecordsOk +1

        t = time.gmtime(int(sOutBuf[1]))

        if int(t.tm_wday) != iOldDay :
            iOldDay = int(t.tm_wday)
            print(t, int(t.tm_wday))
            time.sleep(1)

#        if (int(t.tm_wday) == 0) and (iOldDay == 6):
#            iWeekCount = iWeekCount + 1
#            print("IWeekDay {}\n".format(int(t.tm_wday)))
#            print("IWeekCount {}\n".format(iWeekCount))
#        iOldDay = int(t.tm_wday)

        sWorkBuf = [sOutBuf[0], int(t.tm_year), int(t.tm_mon), iWeekCount, int(t.tm_wday), int(t.tm_mday), int(t.tm_yday), int(t.tm_hour), int(t.tm_min), int(t.tm_sec), sOutBuf[2]]
        sWorkData.append(sWorkBuf)

fobj.close()

if iStartUDay != 0:
    t = time.gmtime(iStartUDay)
    iStartDay = int(t.tm_yday)
    iStartYear = int(t.tm_year)
else:
    iStartDay = 1
    iStartYear = 2014

t = time.gmtime(int(sOutBuf[1]))
iEndDay = int(t.tm_yday)
iEndYear = int(t.tm_year)

# for x in range(len(sWorkData)):
#    print("{} -> {}, {}, {}, {}, {}, {}, {}, {}, {}".format(x, sWorkData[x][0],sWorkData[x][1],sWorkData[x][2],sWorkData[x][3],sWorkData[x][4],sWorkData[x][5],sWorkData[x][6],sWorkData[x][7],sWorkData[x][8]))

#    for i in range(len(sWorkData[x])):
#        print("{} ".format(sWorkData[x][i]))
    
print("Number of records read :", str(i), " Records ok : ", str(iRecordsOk), "\n")
print("Start day : {} - Start year : {}\n".format(str(iStartDay).strip(), str(iStartYear).strip()))
print("End day   : {} - End year   : {}\n".format(str(iEndDay).strip(), str(iEndYear).strip()))


iStartDay = (iStartYear * 365) + iStartDay
iEndDay = (iEndYear * 365) + iEndDay
iNWeeks = int((iEndDay - iStartDay)/7)
print("Number of weeks in file {}\n".format(iNWeeks))

iSelWeek = random.randint(0, iNWeeks)
d = datetime.date.today()
iSelDay = d.isoweekday()

print("For today I would choose week number : {} and day number : {}\n".format (iSelWeek, iSelDay))

#for x in range(len(sWorkData)):
