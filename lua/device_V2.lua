local sunSetTime = "20:32"

local device = {};
device["id"] = {};
device["name"] = {};
device["probability_of_use"] = {};
device["min_duration"] = {};
device["max_duration"] = {};

function convert_sunset(setTime)
	local convDate = os.date("*t", os.time());
	local convHour = string.sub(setTime,1,2);
	local convMinute = string.sub(setTime, -2, -1);
	convDate.hour = tonumber(convHour);
	convDate.min = tonumber(convMinute);
	return os.time(convDate);
end

function convert_lastminute()
	local convDate = os.date("*t", os.time());
	convDate.hour = 23;
	convDate.min = 59;
	return os.time(convDate);
end

function bubble_sort(sort_array)
	local tempArr = {};
	tempArr["id"] = {};
	tempArr["do"] = {};
	tempArr["doTime"] = {};
	tempArr["executed"] = {};

	local hasChanged;

	hasChanged = true;

	while hasChanged == true do
		hasChanged = false;
		for i = 1, #sort_array["id"]-1 do
			if sort_array["doTime"][i] > sort_array["doTime"][i+1] then
				print("Sorting", i)
				tempArr["id"][1] = sort_array["id"][i];
				tempArr["do"][1] = sort_array["do"][i];
				tempArr["doTime"][1] = sort_array["doTime"][i];
				tempArr["executed"][1] = sort_array["executed"][i];
				sort_array["id"][i] = sort_array["id"][i+1];
				sort_array["do"][i] = sort_array["do"][i+1];
				sort_array["doTime"][i] = sort_array["doTime"][i+1];
				sort_array["executed"][i] = sort_array["executed"][i+1];
				sort_array["id"][i+1] = tempArr["id"][1];
				sort_array["do"][i+1] = tempArr["do"][1];
				sort_array["doTime"][i+1] = tempArr["doTime"][1];
				sort_array["executed"][i+1] = tempArr["executed"][1];
				hasChanged = true;
			end
		end
	end

	return sort_array;

end

device["id"] = {15,5,11,19,54,35,66};												-- Device Id
device["name"] = {"TV Raum","Büro","Badzimmer","Treppe","Gang","Fitness","Keller"};	-- Device Name
device["probability_of_use"] = {100,50,100,100,100,5,80};							-- Probability of being used that day
device["min_duration"] = {120, 60, 15, 5, 5, 60, 5};								-- If used, how long will it minimaly stay on
device["max_duration"] = {240, 120, 30, 10, 10, 120, 10};							-- If used, how long will can it stay on
device["start_add"] = {60, 120, 150, 120, 120, 60, 10};								-- How long after sunset could it wait until getting started

math.randomseed(os.time());
local execute = {};
execute["id"] = {};
execute["StartTime"] = {};
execute["TimeOff"] = {};

converted_sunset = convert_sunset(sunSetTime);

for i in pairs(device["id"]) do
	execute["id"][i] = device["id"][i];
	addMinute = math.random(device["start_add"][i]) * 60;
	execute["StartTime"][i] = converted_sunset + addMinute;
	if execute["StartTime"][i] > convert_lastminute() then
		execute["StartTime"][i] = convert_lastminute()-120;
	end
	addMinute = math.random(device["min_duration"][i], device["max_duration"][i]) * 60;
	execute["TimeOff"][i] = execute["StartTime"][i] + addMinute;
	if execute["TimeOff"][i] > convert_lastminute() then
		execute["TimeOff"][i] = convert_lastminute();
	end
end

local action = {};
action["id"] = {};
action["do"] = {};
action["doTime"] = {};
action["executed"] = {};

local arrptr = 0
for i in pairs(execute["id"]) do
	arrptr = arrptr +1;
	action["id"][arrptr] = execute["id"][i];
	action["do"][arrptr] = "on";
	action["doTime"][arrptr] = execute["StartTime"][i];
	action["executed"][arrptr] = false;
	arrptr = arrptr + 1;
	action["id"][arrptr] = execute["id"][i];
	action["do"][arrptr] = "off";
	action["doTime"][arrptr] = execute["TimeOff"][i];
	action["executed"][arrptr] = false;
end

action = bubble_sort(action);

for i in pairs(action["id"]) do
--	print("Device Id : ", action["id"][i], " do : ", action["do"][i], " doTime : ", action["doTime"][i], " executed : ", action["executed"][i]);
	dispTime = os.date("*t", action["doTime"][i])
	dispHour = "00" .. tostring(dispTime.hour);
	dispHour = string.sub(dispHour, -2, -1);
	dispMinute = "00" .. tostring(dispTime.min);
	dispMinute = string.sub(dispMinute, -2, -1);
	dispInfo = dispHour .. ":" .. dispMinute;
	print("Device Id : ", action["id"][i], " do : ", action["do"][i], " doTime : ", dispInfo, " executed : ", action["executed"][i]);
end
