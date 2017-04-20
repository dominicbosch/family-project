
device = {};

device["id"] = {};
device["name"] = {};
device["probability_of_use"] = {};
device["min_duration"] = {};
device["max_duration"] = {};

device["id"] = {15,5,11,19,54,35,66};												-- Device Id
device["name"] = {"TV Raum","Büro","Badzimmer","Treppe","Gang","Fitness","Keller"};	-- Device Name
device["probability_of_use"] = {100,50,100,100,100,5,80};							-- Probability of being used that day
device["min_duration"] = {120, 60, 15, 5, 5, 60, 5};								-- If used, how long will it minimaly stay on
device["max_duration"] = {240, 120, 30, 10, 10, 120, 10};							-- If used, how long will can it stay on
device["start_add"] = {60, 120, 150, 120, 120, 60, 10};								-- How long after sunset could it wait until getting started

--[[
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
--]]

math.randomseed(os.time());
execute = {};
execute["id"] = {};
execute["StartTime"] = {};
execute["TimeOn"] = {};

for i in pairs(device["id"]) do
	execute["id"][i] = device["id"][i];
	execute["TimeOn"][i] = math.random(device["min_duration"][i], device["max_duration"][i]);
	print(execute["id"][i], "", execute["TimeOn"][i]);
end
