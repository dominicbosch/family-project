local sunSetTime = "20:32"

device = {};

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

device["id"] = {15,5,11,19,54,35,66};												-- Device Id
device["name"] = {"TV Raum","Büro","Badzimmer","Treppe","Gang","Fitness","Keller"};	-- Device Name
device["probability_of_use"] = {100,50,100,100,100,5,80};							-- Probability of being used that day
device["min_duration"] = {120, 60, 15, 5, 5, 60, 5};								-- If used, how long will it minimaly stay on
device["max_duration"] = {240, 120, 30, 10, 10, 120, 10};							-- If used, how long will can it stay on
device["start_add"] = {60, 120, 150, 120, 120, 60, 10};								-- How long after sunset could it wait until getting started

math.randomseed(os.time());
execute = {};
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

for i in pairs(execute["id"]) do
	calc_startTime = os.date("*t", execute["StartTime"][i]);
	startHour = tostring(calc_startTime.hour);
	startMinute = tostring(calc_startTime.min);
	calc_endTime = os.date("*t", execute["TimeOff"][i]);
	endHour = tostring(calc_endTime.hour);
	endMinute = tostring(calc_endTime.min);
	dispStartTime = startHour .. ":" .. startMinute;
	dispEndTime = endHour .. ":" .. endMinute;
	print("Device Id : ", execute["id"][i], " Start Time : ", dispStartTime);
	print("Device Id : ", execute["id"][i], " End Time   : ", dispEndTime);
end
