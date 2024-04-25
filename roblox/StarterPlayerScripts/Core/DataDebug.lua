
local LocalPlayer = game:GetService('Players').LocalPlayer

local ReplicatedStorage = game:GetService("ReplicatedStorage")
local ReplicatedModules = require(ReplicatedStorage:WaitForChild("Modules"))

local ReplicatedData = ReplicatedModules.Services.ReplicatedData
local TableUtility = ReplicatedModules.Utility.Table

local SystemsContainer = {}

local DebugContainer = Instance.new('Folder')
DebugContainer.Name = 'DebugContainer'
DebugContainer.Parent = ReplicatedStorage

-- // Module // --
local Module = {}

function Module.OnDataUpdated( Category, Data )
	local DataContainer = DebugContainer:FindFirstChild( Category )
	if not DataContainer then
		DataContainer = Instance.new('Folder')
		DataContainer.Name = Category
		DataContainer.Parent = DebugContainer
	end

	DataContainer:ClearAllChildren()
	TableUtility.TableToObject(Data, DataContainer, {})
end

function Module.Start()
	for k, v in pairs( ReplicatedData.Replicated ) do
		task.spawn( Module.OnDataUpdated, k, v )
	end
	ReplicatedData.OnUpdated:Connect(function(Category, Data)
		Module.OnDataUpdated( Category, Data )
	end)
end

function Module.Init(otherSystems)
	SystemsContainer = otherSystems
end

return Module
