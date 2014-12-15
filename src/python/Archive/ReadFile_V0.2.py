import time

fobj = open("switch.inf","r")
i = 1
iRecordsOk = 0
iStartUDay = -1
sInData=[]
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
        sInData.append(sOutBuf)

        t = time.gmtime(int(sOutBuf[1]))

        sWorkBuf = [sOutBuf[0], int(t.tm_year), int(t.tm_mon), int(t.tm_mday), int(t.tm_hour), int(t.tm_min), int(t.tm_sec), sOutBuf[2]]
        sWorkData.append(sWorkBuf)

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

print(sWorkBuf)

x = len(sWorkData)-1
print(x)
for i in range(len(sWorkData[x])):
    print(sWorkData[x][i])
#print(sWorkData(len(sWorkData)))
    
print("Number of records read :", str(i), " Records ok : ", str(iRecordsOk), "\n")
print("Start day : {} - Start year : {}\n".format(str(iStartDay).strip(), str(iStartYear).strip()))
print("End day   : {} - End year   : {}\n".format(str(iEndDay).strip(), str(iEndYear).strip()))

iNWeeks = int((iEndDay - iStartDay)/7)
print(iNWeeks)

fobj.close()
