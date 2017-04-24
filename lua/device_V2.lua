local sunSetTime = "20:32"				-- to be deleted in fibaro

local device = {};
device["id"] = {};
device["name"] = {};
device["probability_of_use"] = {};
device["min_duration"] = {};
device["max_duration"] = {};

function sleep(n)
  os.execute("sleep " .. tonumber(n))
end

function convert_sunset(setTime)			-- On Fibaro Sunset is in the format "hh:mm"
	local convDate = os.date("*t", os.time());
	local convHour = string.sub(setTime,1,2);
	local convMinute = string.sub(setTime, -2, -1);
	convDate.hour = tonumber(convHour);
	convDate.min = tonumber(convMinute);
	return os.time(convDate);
end

function convert_lastminute()				-- Converting the last minute of the day to os.time format
	local convDate = os.date("*t", os.time());
	convDate.hour = 23;
	convDate.min = 59;
	return os.time(convDate);
end

function bubble_sort(sort_array)			-- Sorting the action array
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

function getDeviceName(srchId, nameArr)

	i = 1
	found = 0

	while i <= #nameArr and found == 0 do
		if nameArr["id"][i] == srchId then
			found = i;
		end
		i = i + 1
	end

	if found >= 1 then
		return nameArr["name"][found];
	else
		return "";
	end

end

device["id"] = {15,5,11,19,54,35,66};												-- Device Id
device["name"] = {"TV Raum","Büro","Badzimmer","Treppe","Gang","Fitness","Keller"};	-- Device Name
device["probability_of_use"] = {100,50,100,100,100,5,80};							-- Probability of being used that day
device["min_duration"] = {120, 60, 15, 5, 5, 60, 5};								-- If used, how long will it minimaly stay on
device["max_duration"] = {240, 120, 30, 10, 10, 120, 10};							-- If used, how long will can it stay on
device["start_add"] = {10, 60, 90, 60, 60, 30, 10};								-- How long after sunset could it wait until getting started

forever = true;

while forever == true do

	math.randomseed(os.time());
	local execute = {};
	execute["id"] = {};
	execute["StartTime"] = {};
	execute["TimeOff"] = {};

	converted_sunset = convert_sunset(sunSetTime);

	for i in pairs(device["id"]) do
		if math.random(100) < device["probability_of_use"][i] then
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

	executedAll = false;

	while executedAll == false do
		for i in pairs(action["id"]) do
			if (os.time() >= action["doTime"][i]) and (action["executed"][i] == false) then
				print(action["doTime"][i]);
				print(os.time());
				action["executed"][i] = true;
				if action["do"][i] == "on" then
					-- fibaro:switch("On");
				else
					-- fibaro:switch("Off")
				end
				dispStr = "Switch : " .. getDeviceName(action["id"][i], device) .. " set to " .. action["do"][i];
				print(dispStr); 
			end
			dispTime = os.date("*t", action["doTime"][i])
			dispHour = "00" .. tostring(dispTime.hour);
			dispHour = string.sub(dispHour, -2, -1);
			dispMinute = "00" .. tostring(dispTime.min);
			dispMinute = string.sub(dispMinute, -2, -1);
			dispInfo = dispHour .. ":" .. dispMinute;
			dispStr = "Device Id : " .. tostring(action["id"][i]) .. " do : " .. action["do"][i] .. " doTime : " .. dispInfo .. " executed : ";
			if action["executed"][i] == false then
				dispStr = dispStr .. "False";
			else
				dispStr = dispStr .. "True";
			end
			print(dispStr);
		end
		sleep(10);
		-- fibaro:wait(60);
		executedAll = true;
		for i in pairs(action["id"]) do
			if action["executed"][i] == false then
				executedAll = false;
			end
		end
		if executedAll == false then
			print "Not all commands executed. Rerun !";
		else
			print "All comands executed. Wait for a new day !";
		end
		print "****************************************";
	end

	newDay = false
	while newDay == false do
		sleep(10);
		-- fibaro:wait
		local checkDate = os.date("*t", os.time());
		if tonumber(checkDate.hour) == 0 then
			newDay = true;
		end
	end
end
