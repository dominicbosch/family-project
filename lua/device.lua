
device = {};

device.id = {};
device.name = {};
device.use = {};
device.duration = {};

device.id = {15,5,11,19,54,35,66};
device.name = {"TV Raum","Büro","Badzimmer","Treppe","Gang","Fitness","Keller"};
device.use = {100,50,100,100,100,5,80};
device.duration = {240, 120, 30, 10, 10, 120, 10};


for i in pairs(device.id) do
	print(device.id[i]);
	print(device.name[i]);
	print(device.use[i]);
	print(device.duration[i]);
end
