
local ReplicatedStorage = game:GetService("ReplicatedStorage")
local ReplicatedModules = require(ReplicatedStorage:WaitForChild("Modules"))

local GuildsConfigModule = ReplicatedModules.Data.Guilds

local RNetModule = ReplicatedModules.Libraries.RNet
local GuildsBridge = RNetModule.Create('GuildsBridge')

local SystemsContainer = {}

-- // Module // --
local Module = {}

Module.GuildsInternal = require(script.GuildsInternal)

function Module.HandleRemoteEvent( LocalPlayer, ... )
	local args = {...}
	print(args)
end

function Module.Start()

	Module.GuildsInternal.SetAPIUrl('http://127.0.0.1:5100')
	Module.GuildsInternal.SetAPIKey('guilds-api-key-10001010101')
	if not Module.GuildsInternal.HealthCheck() then
		warn('Failed to connect to the Guilds API. Guilds is unavailable.')
		return
	end

	GuildsBridge.OnServerEvent(Module.HandleRemoteEvent)

end

function Module.Init(otherSystems)
	SystemsContainer = otherSystems
end

return Module
