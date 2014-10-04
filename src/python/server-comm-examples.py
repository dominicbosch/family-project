#!/usr/bin/env python3.2
#Setzen:
#http://192.168.0.79:8083/ZWaveAPI/Run/devices[2].instances[0].commandClasses[0x25].Set(1)

#Status Update:
#http://192.168.0.79:8083/ZWaveAPI/Run/devices[2].instances[0].commandClasses[0x25].Get()

#Status abfragen:
#http://192.168.0.79:8083/ZWaveAPI/Run/devices[2].instances[0].commandClasses[0x25].data.level


#PYTHON:
import httplib2
conn = httplib2.HTTPConnection("http://192.168.0.79:8083/")
# conn.request("GET", "/index.html")
conn.request("GET", "/ZWaveAPI/Run/devices[2].instances[0].commandClasses[0x25].Set(1)")
