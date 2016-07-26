import sched
import time
import httplib2

iSwitchNo=10
iOn=1
iOff=0
httpOut = httplib2.Http()
scheduler = sched.scheduler(time.time, time.sleep)

def compile_httpset(IDeviceNum, IDeviceSet):
    sOutBuf = "http://192.168.0.79:8083/ZWaveAPI/Run/devices[" + str(IDeviceNum)
    sOutBuf = sOutBuf + "].instances[0].commandClasses[0x25].Set(" + str(IDeviceSet)
    sOutBuf = sOutBuf + ")"
    return sOutBuf

def switch_light(iDeviceNum, iDeviceSet):
    resp, content = httpOut.request(compile_httpset(iDeviceNum, iDeviceSet), "GET")

def print_event(name):
    print('EVENT:', time.time(), name)

now = time.time()

print( 'START:', now)

vRetVal = scheduler.enterabs(now+10, 1, switch_light,(iSwitchNo, iOn))
print(vRetVal)
vRetVal = scheduler.enterabs(now+20, 1, switch_light,(iSwitchNo, iOff))
print(vRetVal)
vRetVal = scheduler.enterabs(now+30, 1, switch_light,(iSwitchNo, iOn))
print(vRetVal)
vRetVal = scheduler.enterabs(now+40, 1, switch_light,(iSwitchNo, iOff))
print(vRetVal)
scheduler.run()

print( 'END:', now)
