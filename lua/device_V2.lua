
device = {};

device["id"] = {};
device["name"] = {};
device["probability_of_use"] = {};
device["min_duration"] = {};
device["max_duration"] = {};

device["id"] = {15,5,11,19,54,35,66};
device["name"] = {"TV Raum","Büro","Badzimmer","Treppe","Gang","Fitness","Keller"};
device["probability_of_use"] = {100,50,100,100,100,5,80};
device["min_duration"] = {120, 60, 15, 5, 5, 60, 5};
device["max_duration"] = {240, 120, 30, 10, 10, 120, 10};

for i in pairs(device["id"]) do
	print(device["id"][i]);
	print(device["name"][i]);
	print(device["probability_of_use"][i]);
	print(device["min_duration"][i]);
	print(device["max_duration"][i]);
	print("----------")
end

testVar = "id";

print("TestVar");
print(device[testVar][1]);
