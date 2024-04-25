local ReplicatedStorage = game:GetService('ReplicatedStorage')
require(ReplicatedStorage:WaitForChild('Modules'))
local ServerStorage = game:GetService('ServerStorage')
require(ServerStorage:WaitForChild('Modules'))
require(ServerStorage:WaitForChild('Core'))

local Data = require(ReplicatedStorage:WaitForChild('Framework'))
Data.Init()
Data.Start()
