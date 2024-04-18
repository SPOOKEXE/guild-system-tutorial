
local DEBUG_MODE = true

local Cache = {}

local function SetDebugModule(enabled : boolean)
	DEBUG_MODE = enabled
end

local function HasInitFunction(tbl : {}) : boolean
	return tbl.Init or ( getmetatable(tbl) and getmetatable(tbl).Init )
end

local function HasStartFunction(tbl : table) : boolean
	return tbl.Start or (getmetatable(tbl) and getmetatable(tbl).Start)
end

local function Register( Parent : Instance ) : {}
	if Cache[Parent] then
		return Cache[Parent]
	end
	if DEBUG_MODE then
		print("Caching Children of: ", Parent:GetFullName())
	end
	local Children = {}
	for _, ModuleScript in Parent:GetChildren() do
		if ModuleScript:IsA('ModuleScript') then
			if Children[ModuleScript.Name] then
				local message = 'Duplicate child under parent: %s %s'
				error(string.format(message, Children.Name, Parent:GetFullName()))
			end
			Children[ModuleScript.Name] = require(ModuleScript)
		end
	end
	Cache[Parent] = Children
	return Children
end

local function Init()
	for Parent, children in Cache do
		for initName, initModule in children do
			if typeof(initModule) ~= 'table' then
				continue
			end
			if initModule.Initialized or not HasInitFunction(initModule) then
				continue
			end
			local Container = { ParentSystems = Cache[Parent.Parent] }
			for otherInitName, otherInitModule in children do
				if otherInitName == initName then
					continue
				end
				Container[otherInitName] = otherInitModule
			end
			initModule.Initialized = true
			if DEBUG_MODE then
				print("Initializing Module:", Parent:GetFullName(), '->', initName)
			end
			initModule.Init(Container)
		end
	end
end

local function Start()
	for parent, children in Cache do
		for name, module in pairs(children) do
			if typeof(module) ~= 'table' then
				continue
			end
			if module.Started or not HasStartFunction(module) then
				continue
			end
			module.Started = true
			if DEBUG_MODE then
				print("Starting Module:", parent:GetFullName(), '->', name)
			end
			task.defer(module.Start)
		end
	end
end

return { SetDebugModule = SetDebugModule, Register = Register, Init = Init, Start = Start }
