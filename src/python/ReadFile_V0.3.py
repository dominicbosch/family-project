import time

fobj = open("switch.inf","r")
i = 1
iRecordsOk = 0
iStartUDay = -1
sWorkData=[]
sWorkBuf=[]

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

        sWorkBuf = [sOutBuf[0], int(t.tm_year), int(t.tm_mon), int(t.tm_mday), int(t.tm_hour), int(t.tm_min), int(t.tm_sec), sOutBuf[2]]
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

for x in range(len(sWorkData)):
    print("{} -> {}, {}, {}, {}, {}, {}, {}, {}".format(x, sWorkData[x][0],sWorkData[x][1],sWorkData[x][2],sWorkData[x][3],sWorkData[x][4],sWorkData[x][5],sWorkData[x][6],sWorkData[x][7]))

#    for i in range(len(sWorkData[x])):
#        print("{} ".format(sWorkData[x][i]))
    
print("Number of records read :", str(i), " Records ok : ", str(iRecordsOk), "\n")
print("Start day : {} - Start year : {}\n".format(str(iStartDay).strip(), str(iStartYear).strip()))
print("End day   : {} - End year   : {}\n".format(str(iEndDay).strip(), str(iEndYear).strip()))

iNWeeks = int((iEndDay - iStartDay)/7)
print("Number of weeks in file {}\n".format(iNWeeks))


