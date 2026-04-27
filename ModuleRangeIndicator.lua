-- This module takes aruments form the game's GON files (as prvided in the RangeIndicator Template) and intpret them to work with the GridShape module --
local GridShape = require('Module:GridShape')
local p = {}

-- Generate GridShape string argument for the standard shape. see: "Manhattan Distance" for math explenation
local function standard_aoe(is_aoe, target_mode, min_range, max_range)
    local result = ""
    local color = 0
    local distance = 999
    local offset = 0
   	if is_aoe then
    	offset = 10
    end
    -- hanle abilities that cover the entire screen
    if max_range > 14 then
    	return "1 1 1 1 1 1 1 1 1 1;1 1 1 1 1 1 1 1 1 1;1 1 1 1 1 1 1 1 1 1;1 1 1 1 1 1 1 1 1 1;1 1 1 1 1 1 1 1 1 1;1 1 1 1 1 1 1 1 1 1;1 1 1 1 1 1 1 1 1 1;1 1 1 1 1 1 1 1 1 1;1 1 1 1 1 1 1 1 1 1;1 1 1 1 1 1 1 1 1 1;"
    end
    for i=0, (max_range*2) do
    	for j=0, (max_range*2) do
    		
    		distance = math.abs(max_range - i) + math.abs(max_range - j)

    		if distance >= min_range and distance <= max_range then
    			color = (1 + offset)
    		else
    			color = 0
    		end
    		if (distance == 0) and (not is_aoe) then
    			color = color+3
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
    local offset = 0
   	if is_aoe then
    	offset = 10
    end
    for i = -max_range+2, max_range do
    	for j = 0, max_range do
    		if  j+i > min_range and i-j < min_range then
    			color = (1 + offset)
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
    local offset = 0
   	if is_aoe then
    	offset = 10
    end
    for i = -1, 1 do
    	for j = 0, max_range do
    		if  j >= min_range and i==0 then
    			color = (1 + offset)
    		else
    			color = 0
    		end
    		if j > 0 then
    			result = result.." "
    		end
    		if (j == 0) and (i==0) and (not is_aoe) then
    			color = color + 3
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
    local offset = 0
   	if is_aoe then
    	offset = 10
    end
    -- account for the default
    if max_range == 0 then
    	max_range = 1
    	is_aoe = false
    end
    for i = -max_range, max_range do
    	for j = -max_range, max_range do
    		if  (j == 0 and math.abs(i) >= min_range) or (i == 0 and math.abs(j) >= min_range) then
    			color = (1 + offset)
    		else
    			color = 0
    		end
    		if (j == 0) and (i==0) and (not is_aoe) then
    			color = color + 3
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

local function  diagcross_aoe(is_aoe, target_mode, min_range, max_range)
    local result = ""
    local color = 0
    local offset = 0
   	if is_aoe then
    	offset = 10
    end
    -- account for the default
    if max_range == 0 then
    	max_range = 1
    	is_aoe = false
    end
    for i = -max_range, max_range do
    	for j = -max_range, max_range do
    		if  math.abs(i) == math.abs(j) and math.abs(i) >= min_range then
    			color = (1 + offset)
    		else
    			color = 0
    		end
    		if (j == 0) and (i==0) and (not is_aoe) then
    			color = color + 3
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
    local offset = 0
   	if is_aoe then
    	offset = 10
    end
    for i = -max_range/2, max_range/2 do
    	for j = 0, 4 do
    		if  (j == 3 and i >= min_range and i < max_range) then
    			color = (1 + offset)
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
-- TODO: add aoe_symmetry
local function custom_aoe_f(is_aoe, target_mode, min_range, max_range,  
	custom_aoe, aoe_symmetry)
	
	local points = {}
    local min_x, max_x, min_y, max_y = 0,0,0,0
    local offset = 0
   	if is_aoe then
    	offset = 10
    end

    -- Parse the string with regex to find [x, y] pairs 
    -- (also account for the cacses where the , is missing)
    for y_str, x_str in custom_aoe:gmatch("%[(-?%d+),?%s*(-?%d+)%]") do
        local x, y = tonumber(x_str), tonumber(y_str)
        
        
        points[x] = points[x] or {}
        points[x][y] = true
		
        min_x = min_x and math.min(min_x, x) or x
        max_x = max_x and math.max(max_x, x) or x
        min_y = min_y and math.min(min_y, y) or y
        max_y = max_y and math.max(max_y, y) or y
        
        if aoe_symmetry == "four_way" or aoe_symmetry == "eight_way"  then
        	points[y] = points[y] or {}
			points[y][-x] = true
			points[-x] = points[-x] or {}
			points[-x][-y] = true
			points[-y] = points[-y] or {}
			points[-y][x] = true
			
			min_x = math.min(min_x, -x)
			max_x = math.max(max_x, -x)
        	min_y = math.min(min_y, -y)
        	max_y = math.max(max_y, -y)
        	
        	
        	if aoe_symmetry == "eight_way"  then
        		points[y][x] = true
        		points[x][-y] = true
        		points[-y][-x] = true
        		points[-x][y] = true
        	end
        end
        
    end
    
    if not min_x then return "" end
    
    -- if no targeting, duplicate to the edge
    if target_mode == "none" then
        local draw_distance = 5
        for i = 1, draw_distance do
        	for x = min_x, max_x do
        		for y = min_y, max_y do
        			if points[x] and points[x][y] then
        				points[x*i] = points[x*i] or {}
        				points[x*i][y*i] = true
            		end
            	end
        	end
		end
	    min_x = min_x*draw_distance
        max_x = max_x*draw_distance
        min_y = min_y*draw_distance
        max_y = max_y*draw_distance
    end


    local output = {}
    
    for x = min_x, max_x do
        local row_values = {}
        for y = min_y, max_y do
        	if x == 0 and y == 0 and not is_aoe then
                table.insert(row_values, 3)
            elseif points[x] and points[x][y] then
                table.insert(row_values, 1+offset)
            else
                table.insert(row_values, 0)
            end
        end
        
        table.insert(output, table.concat(row_values, " ") .. ";")
    end

    return table.concat(output, "")
end

--test mode for feeding a direct string. Tihs will need to be in final format
-- I.e: "1 2 3 4;5 6 7 8" and so on
local function test_aoe(custom_aoe)
	return custom_aoe
end

-- Main function
function p.render(frame)
	local is_aoe = frame.args.is_aoe or "false" -- for range or aoe indicator  Default: False (Range) 
	local target_mode =  frame.args.target_mode or "tile" -- who this targets  Default: None 
	local aoe_mode = frame.args.aoe_mode or "standard" -- one of several preprogrammed shapes or custom Default: standard
	local min_range = frame.args.min_range or "0" -- default: 0 
	local max_range = frame.args.max_range or "0" -- default: 0 
	local aoe_excludes_self = frame.args.aoe_excludes_self or "true" -- true/false default: true
	local custom_aoe = frame.args.custom_aoe or "" -- an array storing custom aoe shape
	local aoe_symmetry = frame.args.aoe_symmetry or "none"
	
	local grid_string = ""
	
	is_aoe = mw.text.trim(is_aoe) == "true"
	target_mode = mw.text.trim(target_mode)
	aoe_mode = mw.text.trim(aoe_mode)
	min_range = tonumber(mw.text.trim(min_range))
	max_range = tonumber(mw.text.trim(max_range))
	aoe_excludes_self =  mw.text.trim(aoe_excludes_self) == "true"
	custom_aoe = mw.text.trim(custom_aoe)
	aoe_symmetry = mw.text.trim(aoe_symmetry)
	
	if aoe_excludes_self then
		if min_range < 1 then
		 	min_range = 1 
		end
	end
	
	-- this is a failsafe to ensure we don't crash the page by making too big of a shape
	-- te diagonal of a 10x10 square is ~14.1 so 15 should always cover the entire board.
	if max_range > 10 then
		max_range = 15
	end
	
	-- select the correct shape
    if aoe_mode == "standard" then
    	grid_string = standard_aoe(is_aoe, target_mode, min_range, max_range)
    elseif aoe_mode == "cone" then
    	grid_string = cone_aoe(is_aoe, target_mode, min_range, max_range)
    elseif aoe_mode == "line" then
    	grid_string = line_aoe(is_aoe, target_mode, min_range, max_range)
    elseif aoe_mode == "cross" then
    	grid_string = cross_aoe(is_aoe, target_mode, min_range, max_range)
    elseif aoe_mode == "8cross" then
    	grid_string = e_cross_aoe(is_aoe, target_mode, min_range, max_range)
    elseif aoe_mode == "square" then
    	grid_string = square_aoe(is_aoe, target_mode, min_range, max_range)
    elseif aoe_mode == "circle" then
    	grid_string = circle_aoe(is_aoe, target_mode, min_range, max_range)
    elseif aoe_mode == "perpline" then
    	grid_string = perpline_aoe(is_aoe, target_mode, min_range, max_range)
    elseif aoe_mode == "diagcross" then
    	grid_string = diagcross_aoe(is_aoe, target_mode, min_range, max_range)
    elseif aoe_mode == "custom" then
    	grid_string = custom_aoe_f(is_aoe, target_mode, min_range, max_range,  
	custom_aoe, aoe_symmetry)
    elseif aoe_mode == "test" then
    	grid_string = test_aoe(custom_aoe)
    else
    	grid_string = "" -- will print error
    end
	
	--return grid_string -- test
	
	return GridShape.render({ args = { 
		grid_string,
		type = "range"
	} })
    
end

function p.test()
	local frame = mw.getCurrentFrame()
	frame.args = {
		is_aoe = "true",
		target_mode = "direction",
		aoe_mode = "cone",
		min_range = "1",
		max_range = "3",
		aoe_excludes_self = "true"
	}

	return p.render(frame)
end

return p
