import time

fobj = open("switch.inf","r")
i = 1

for line in fobj:
    print("Record Number :", str(i))
    i = i + 1
    print("Read          :", line.strip())
    sOutBuf = line.split(",")
    if sOutBuf[0].find("error") == -1:
        print("Switch        :", sOutBuf[0].strip())
        print("Time          :", sOutBuf[1].strip(), " = ", time.ctime(int(sOutBuf[1])))
        print("Status        :", sOutBuf[2].strip(), "\n")

fobj.close()
