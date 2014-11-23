import time

fobj = open("SwitchState.txt","r")
i = 1

for line in fobj:
    print("Record Number :", str(i))
    i = i + 1
    print("Read          :", line.strip())
    sOutBuf = line.split(",")
    print("Switch        :", sOutBuf[0].strip())
    print("Time          :", sOutBuf[1].strip(), " = ", time.ctime(int(sOutBuf[1])))
    print("Status        :", sOutBuf[2].strip(), "\n")

fobj.close()
