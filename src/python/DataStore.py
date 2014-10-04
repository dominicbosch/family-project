
fobj = open("tstData.txt","a")

stati = {"2": "On",
         "3": "Off"}

for outVal in stati:
    fobj.write("{} {}\n".format(outVal, stati[outVal]))
    print(outVal)

fobj.close
