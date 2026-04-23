-- This module takes aruments form the game's GON files (as prvided in the RangeIndicator Template) and intpret them to work with the FurnitureShape module --
local FurnitureShape = require('Module:FurnitureShape')
local p = {}

-- Generate FuntitureShape string argument for the standard shape. see: "Manhattan Distance" for math explenation
local function standard_aoe(is_aoe, target_mode, min_range, max_range)
    local result = ""
    local color = 0
    local distance = 999
    for i = 0, max_range*2-1 do
    	for j = 0, max_range*2-1 do
    		distance = math.abs(max_range - i) + math.abs(max_range - j)
    		if (distance == 0) and (not is_aoe) then
    			color = 3
    		elseif distance >= min_range and distance < max_range then
    			color = 1
    		else
    			color = 0
    		end
    		if j > 0 then
    			result = result.." "
    		end
    		result = result..color
    	end
    	if i < max_range*2 then
    		result = result..";"
    	end
    end
    return result
end

local function cone_aoe(is_aoe, target_mode, min_range, max_range)
    local result = ""
    local color = 0
    for i = -max_range+2, max_range do
    	for j = 0, max_range do
    		if  j+i > min_range and i-j < min_range then
    			color = 1
    		else
    			color = 0
    		end
    		if j > 0 then
    			result = result.." "
    		end
    		if (j == 0) and (i==1) then
    			color = 3
    		end
    		result = result..color
    	end
    	if i < max_range*2 then
    		result = result..";"
    	end
    end
    return result
end

local function line_aoe(is_aoe, target_mode, min_range, max_range)
    local result = ""
    local color = 0
    for i = -1, 2 do
    	for j = 0, max_range do
    		if  j >= min_range and i==0 then
    			color = 1
    		else
    			color = 0
    		end
    		if j > 0 then
    			result = result.." "
    		end
    		if (j == 0) and (i==0) then
    			color = 3
    		end
    		result = result..color
    	end
    	if i < max_range*2 then
    		result = result..";"
    	end
    end
    return result
end

local function cross_aoe(is_aoe, target_mode, min_range, max_range)
    local result = ""
    local color = 0
    -- account for the default
    if max_range == 0 then
    	max_range = 1
    	is_aoe = false
    end
    for i = -max_range, max_range do
    	for j = -max_range, max_range do
    		if  (j == 0 and math.abs(i) >= min_range) or (i == 0 and math.abs(j) >= min_range) then
    			color = 1
    		else
    			color = 0
    		end
    		if (j == 0) and (i==0) and (not is_aoe) then
    			color = 3
    		end
    		-- don't add space at the start
    		if j > -max_range then
    			result = result.." "
    		end
    		result = result..color
    	end
    	if i < max_range then
    		result = result..";"
    	end
    end
    return result
end

-- perpendicular to the selection 
local function perpline_aoe(is_aoe, target_mode, min_range, max_range)
    local result = ""
    local color = 0
    for i = -max_range/2, max_range/2 do
    	for j = 0, 4 do
    		if  (j == 3 and i >= min_range and i < max_range) then
    			color = 1
    		else
    			color = 0
    		end
    		if (j == 0) and (i == 0) then
    			color = 3
    		end
    		-- don't add space at the start
    		if j > -max_range then
    			result = result.." "
    		end
    		result = result..color
    	end
    	if i < max_range then
    		result = result..";"
    	end
    end
    return result
end

-- Custom targeting - This is Tylers punishmet for me
local function custom_aoe(is_aoe, target_mode, min_range, max_range)
    local result = ""
    local color = 0
    local range = 10
    if max_range > 0 then
    	max_range = max_range/2
    end
    for i = -range, range do
    	for j = -range, range do
    		if  (j == 3 and i >= min_range and i < max_range) then
    			color = 1
    		else
    			color = 0
    		end
    		if (j == 0) and (i == 0) then
    			color = 3
    		end
    		-- don't add space at the start
    		if j > -max_range then
    			result = result.." "
    		end
    		result = result..color
    	end
    	if i < max_range then
    		result = result..";"
    	end
    end
    return result
end


-- Main function
function p.render(frame)
	local is_aoe = frame.args.is_aoe -- for range or aoe indicator  Default: False (Range) 
	local target_mode =  frame.args.target_mode -- who this targets  Default: None 
	local aoe_mode = frame.args.aoe_mode -- one of several preprogrammed shapes or custom Default: standard
	local min_range = frame.args.min_range -- default: 0 
	local max_range = frame.args.max_range -- default: 0 
	local aoe_excludes_self = frame.args.aoe_excludes_self -- true/false default: true
	local custom_aoe = frame.args.custom_aoe -- an array storing custom aoe shape
	
	local furniture_string = ""
	
	is_aoe = mw.text.trim(is_aoe) == "true"
	target_mode = mw.text.trim(target_mode)
	aoe_mode = mw.text.trim(aoe_mode)
	min_range = tonumber(mw.text.trim(min_range))
	max_range = tonumber(mw.text.trim(max_range))
	aoe_excludes_self =  mw.text.trim(aoe_excludes_self) == "true"
	custom_aoe = mw.text.trim(custom_aoe)
	
	if aoe_excludes_self then
		if min_range < 1 then
		 	min_range = 1 
		end
	end
	
	-- select the correct shape
    if aoe_mode == "standard" then
    	furniture_string = standard_aoe(is_aoe, target_mode, min_range, max_range)
    elseif aoe_mode == "cone" then
    	furniture_string = cone_aoe(is_aoe, target_mode, min_range, max_range)
    elseif aoe_mode == "line" then
    	furniture_string = line_aoe(is_aoe, target_mode, min_range, max_range)
    elseif aoe_mode == "cross" then
    	furniture_string = cross_aoe(is_aoe, target_mode, min_range, max_range)
    elseif aoe_mode == "8cross" then
    	furniture_string = e_cross_aoe(is_aoe, target_mode, min_range, max_range)
    elseif aoe_mode == "square" then
    	furniture_string = square_aoe(is_aoe, target_mode, min_range, max_range)
    elseif aoe_mode == "circle" then
    	furniture_string = circle_aoe(is_aoe, target_mode, min_range, max_range)
    elseif aoe_mode == "perpline" then
    	furniture_string = perpline_aoe(is_aoe, target_mode, min_range, max_range)
    elseif aoe_mode == "diagcross" then
    	furniture_string = diagcross_aoe(is_aoe, target_mode, min_range, max_range)
    elseif aoe_mode == "custom" then
    	furniture_string = custom_aoe(is_aoe, target_mode, min_range, max_range, custom_aoe)
    else
    	furniture_string = "" -- will print error
    end
	
	-- return furniture_string -- test
	
	return FurnitureShape.render({ args = { furniture_string } }) -- will this work?
    
end

return p