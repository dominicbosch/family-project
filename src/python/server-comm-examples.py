#Setzen:
#http://192.168.0.79:8083/ZWaveAPI/Run/devices[2].instances[0].commandClasses[0x25].Set(0)

#Status Update:
#http://192.168.0.79:8083/ZWaveAPI/Run/devices[2].instances[0].commandClasses[0x25].Get()

#Status abfragen:
#http://192.168.0.79:8083/ZWaveAPI/Run/devices[2].instances[0].commandClasses[0x25].data.level


#PYTHON:
import httplib2
import json
h = httplib2.Http(".cache")
resp, content = h.request("http://192.168.0.79:8083/ZWaveAPI/Run/devices[2].instances[0].commandClasses[0x25].Set(0)", "GET")
resp, content = h.request("http://192.168.0.79:8083/ZWaveAPI/Run/devices[2].instances[0].commandClasses[0x25].Get()", "GET")

resp, content = h.request("http://192.168.0.79:8083/ZWaveAPI/Run/devices[2].instances[0].commandClasses[0x25].data.level", "GET")

print(content)

#print(content[1])
#for c in content: print(c)
mydict = json.loads(content.decode('ascii'))
print(mydict)


print(mydict['value'])

#conn = httplib2.Http("http://192.168.0.79:8083/")
# conn.request("GET", "/index.html")
#conn.request("GET", "/ZWaveAPI/Run/devices[2].instances[0].commandClasses[0x25].Set(0)")
