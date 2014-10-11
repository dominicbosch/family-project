
import httplib2
import json

h = httplib2.Http(".cache")

def compile_httpset(IDeviceNum, IDeviceSet):
    sOutBuf = "http://192.168.0.79:8083/ZWaveAPI/Run/devices[" + str(IDeviceNum)
    sOutBuf = sOutBuf + "].instances[0].commandClasses[0x25].Set(" + str(IDeviceSet)
    sOutBuf = sOutBuf + ")"
    return sOutBuf

def compile_httprefresh(IDeviceNum):
    sOutBuf = "http://192.168.0.79:8083/ZWaveAPI/Run/devices[" + str(IDeviceNum)
    sOutBuf = sOutBuf + "].instances[0].commandClasses[0x25].Get()"
    return sOutBuf

def compile_httpgetstat(IDeviceNum):
    sOutBuf = "http://192.168.0.79:8083/ZWaveAPI/Run/devices[" + str(IDeviceNum)
    sOutBuf = sOutBuf + "].instances[0].commandClasses[0x25].data.level"
    return sOutBuf

def get_currentstat(IDeviceNum):
    resp, content = h.request(compile_httprefresh(IDeviceNum), "GET")
    resp, content = h.request(compile_httpgetstat(IDeviceNum), "GET")
    DDevInfo = json.loads(content.decode('ascii'))
    BDevStatus = DDevInfo['value']
    if BDevStatus == True:
        SDevStatus = "On"
    else:
        SDevStatus = "Off"
    return SDevStatus

def get_currenttime(IDeviceNum):
    resp, content = h.request(compile_httprefresh(IDeviceNum), "GET")
    resp, content = h.request(compile_httpgetstat(IDeviceNum), "GET")
    DDevInfo = json.loads(content.decode('ascii'))
    return DDevInfo["updateTime"]

def get_lighttoswitch():
    iInVal = 0
    bForEver = False
    while bForEver == False:
        vTmpIn = input("Light to switch (0 for exit) : ")
        try:
            iInVal = int(vTmpIn)
        except ValueError:
            print("Please enter an integer")
            iInVal = 0
        if iInVal in range(2,4):
            return iInVal
        elif iInVal !=0:
            print("Currently only light switch 2 and 3 are active")
        else:
            return 0

def get_statetoswitch():
    iInVal = 0
    bForEver = False
    while bForEver == False:
        vTmpIn = input("Off = 0, On = 1 : ")
        try:
            iInVal = int(vTmpIn)
        except ValueError:
            print("Please enter an integer")
            iInVal = 0
        if iInVal in range(0,2):
            return iInVal
        else:
            print("You can only select 0 = Off or 1 = On")

i = get_lighttoswitch()

while i != 0:
    print ("Current Status of Switch : ", str(i), " is ", get_currentstat(i))
    
    resp, content = h.request(compile_httpset(i, get_statetoswitch()), "GET")

    sDevStatus = get_currentstat(i)

    fobj = open("SwitchInfo.txt", "a")
    sOutBuf = "Switch : " + str(i) + " is " + sDevStatus
    print(sOutBuf)
    fobj.write("{}\n".format(sOutBuf))
    fobj.close()

    fobiS = open("SwitchState.txt", "a")
    fobiS.write("{}, {}, {}\n".format(str(i), get_currenttime(i), sDevStatus))
    fobiS.close()

    i = get_lighttoswitch()
    
