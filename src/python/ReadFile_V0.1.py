import time

fobj = open("switch.inf","r")
i = 1
iRecordsOk = 0
sInData=[]

for line in fobj:
#    print("Record Number :", str(i))
    i = i + 1
#    print("Read          :", line.strip())
    sOutBuf = line.split(",")
    if sOutBuf[0].find("error") == -1:
        iRecordsOk = iRecordsOk +1
        sInData.append(sOutBuf)
#        print("Switch        :", sOutBuf[0].strip())
#        print("Time          :", sOutBuf[1].strip(), " = ", time.ctime(int(sOutBuf[1])))
#        print("Status        :", sOutBuf[2].strip(), "\n")



print("Number of records read :", str(i), " Records ok : ", str(iRecordsOk), "\n")
print("Switch        :", sOutBuf[0].strip())
print("Time          :", sOutBuf[1].strip(), " = ", time.ctime(int(sOutBuf[1])))
print("Status        :", sOutBuf[2].strip(), "\n")

for i in range(len(sInData[12])):
    print(sInData[12][i])

print("Last Record          :", line.strip(), "\n")

t = time.gmtime(int(sOutBuf[1]))

sMDay = str(t.tm_mday)
sMDay = sMDay.strip()

print(len(sMDay),"\n")

print("{}{}.{}.{}\n".format("Last Record date : ", str(t.tm_mday).strip(), str(t.tm_mon).strip(), str(t.tm_year).strip()))
print("{}{}\n".format("Last record day of week : ", str(t.tm_wday).strip()))


fobj.close()
