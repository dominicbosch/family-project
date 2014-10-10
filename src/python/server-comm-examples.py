#Setzen:
#http://192.168.0.79:8083/ZWaveAPI/Run/devices[2].instances[0].commandClasses[0x25].Set(0)

#Status Update:
#http://192.168.0.79:8083/ZWaveAPI/Run/devices[2].instances[0].commandClasses[0x25].Get()

#Status abfragen:
#http://192.168.0.79:8083/ZWaveAPI/Run/devices[2].instances[0].commandClasses[0x25].data.level


#PYTHON:
import httplib2
# conn = httplib2.HTTPConnection("http://192.168.0.79:8083/")
import json
h = httplib2.Http(".cache")

SwitchStat = 1
print(type(SwitchStat))

print(str(SwitchStat))

resp, content = h.request("http://192.168.0.79:8083/ZWaveAPI/Run/devices[2].instances[0].commandClasses[0x25].Set(1)", "GET")
resp, content = h.request("http://192.168.0.79:8083/ZWaveAPI/Run/devices[3].instances[0].commandClasses[0x25].Set(1)", "GET")

resp2, content2 = h.request("http://192.168.0.79:8083/ZWaveAPI/Run/devices[2].instances[0].commandClasses[0x25].Get()", "GET")
resp2, content2 = h.request("http://192.168.0.79:8083/ZWaveAPI/Run/devices[2].instances[0].commandClasses[0x25].data.level", "GET")

resp3, content3 = h.request("http://192.168.0.79:8083/ZWaveAPI/Run/devices[2].instances[0].commandClasses[0x25].Get()", "GET")
resp3, content3 = h.request("http://192.168.0.79:8083/ZWaveAPI/Run/devices[2].instances[0].commandClasses[0x25].data.level", "GET")

mydict2 = json.loads(content2.decode('ascii'))
mydict3 = json.loads(content3.decode('ascii'))

print("Switch # 2 on : ", mydict2['value'])
print("Switch # 3 on : ", mydict3['value'])

#print(content)

#print(content[1])
#for c in content: print(c)
#mydict = json.loads(content.decode('ascii'))
#print("Mydict : ", mydict)

#print(len(mydict))

#print(mydict['updateTime'])

#print(mydict['value'])

#conn = httplib2.Http("http://192.168.0.79:8083/")
# conn.request("GET", "/index.html")
#conn.request("GET", "/ZWaveAPI/Run/devices[2].instances[0].commandClasses[0x25].Set(0)")
