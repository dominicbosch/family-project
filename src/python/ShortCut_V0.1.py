import httplib2
import json
import time

#sStopFileName = "/mnt/nas/stop.yes"
#iSleepTimme = 600

sStopFileName = "stop.yes"
iSleepTime = 10

h = httplib2.Http()

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
    try:
        DDevInfo = json.loads(content.decode('ascii'))
        return DDevInfo
    except (ValueError):
        return ""
    else:
        return ""

def set_light(IDeviceNum, IFromHour, IToHour, iCurrHour):

    DDevInfo = get_currentstat(IDeviceNum)
    if DDevInfo != "":
        BDevStatus = DDevInfo['value']
        print ("Current Status of Switch : ", str(IDeviceNum), " is ", BDevStatus)

        if (iCurrHour > IFromHour) and (iCurrHour < IToHour):
            if BDevStatus == False: 
                resp, content = h.request(compile_httpset(IDeviceNum, 1))
        else:
            if BDevStatus == True:
                resp, content = h.request(compile_httpset(IDeviceNum, 0))
    else:
        print("Error thrown")
        return False
        
    DDevInfo = get_currentstat(i)
    if DDevInfo != "":
        BDevStatus = DDevInfo['value']
        print ("Current Status of Switch : ", str(i), " is ", BDevStatus)
    else:
        print ("Error thrown")
        return False

    return True

def get_openfile(SFileName):
    try:
        tobj = open(SFileName, "r")
        tobj.close()
        return True
    except (IOError, TypeError):
        return False

BForever = True

while BForever == True:

    iSUDay = time.localtime(time.time())
    iCurrHour = iSUDay.tm_hour

    print("{}.{}.{} {}.{}".format(iSUDay.tm_mday,iSUDay.tm_mon,iSUDay.tm_year,iSUDay.tm_hour,iSUDay.tm_min))
                                  

# Büro
    i=2
    BRetval = set_light(i,19,21,iCurrHour)

# Fernsehzimmer
    i=6
    BRetval = set_light(i,16,22,iCurrHour)

# Eingang EG
    i=10
    BRetval = set_light(i,20,22,iCurrHour)

    print("\n")
    
    time.sleep(iSleepTime)

    BForever = not get_openfile(sStopFileName)
