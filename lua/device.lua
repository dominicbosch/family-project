
device = {};

device.id = {};
device.name = {};
device.use = {};
device.duration = {};

device.id = {5,10,15,20,25,30,35};
device.name = {"Entrance","Office","First floor","Bathroom","Hobby","Fitness","Kitchen};
device.use = {100,50,100,100,100,5,80};
device.duration = {240, 120, 30, 10, 10, 120, 10};


for i in pairs(device.id) do
	print(device.id[i]);
	print(device.name[i]);
	print(device.use[i]);
	print(device.duration[i]);
end
