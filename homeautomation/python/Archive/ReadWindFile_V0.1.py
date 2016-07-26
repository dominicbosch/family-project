import time

fobj = open("Windspeed.inf","r")

i = 1
iRecordsOk = 0
sInData=[]

for line in fobj:
    i = i + 1
    sOutBuf = line.split(",")
    iRecordsOk = iRecordsOk +1
#    print("Sensor Id      : ", sOutBuf[0].strip())
#    print("Sensor type    : ", sOutBuf[1])
    t = time.gmtime(float(sOutBuf[2]))
    sDay = str(t.tm_mday).strip()
    sMon = str(t.tm_mon).strip()
    sYea = str(t.tm_year).strip()
    sDOut = sDay + "." + sMon + "." + sYea
    sHou = str(t.tm_hour).strip()
    sMin = str(t.tm_min).strip()
    sSec = str(t.tm_sec).strip()
    sTOut = sHou + ":" + sMin + ":" + sSec
    sOut = sDOut + "  " + sTOut
#    print("Time stamp     : ", sOut)
#    print("Temperatur     : ", sOutBuf[3].strip(), "\n")
    sOutTmp = sOutBuf[3].strip()

    sTmpBuf = [sDOut, sTOut, sOutTmp]
    sInData.append(sTmpBuf)

print("Number of records read :", str(i), " Records ok : ", str(iRecordsOk), "\n")


fobj.close()

fobj = open("Windspeed.txt", "a")

for i in range(len(sInData)):

    fobj.write("{}, {}, {}\n".format(sInData[i] [0], sInData[i] [1], sInData[i] [2]))

#    fobj.write("{}, {}, {}, {}\n".format(str(sInData[0]), str(sInData[1]), sInData[2], sInData[3]))

#    fobj.write(sInData[0])

fobj.close()
    
