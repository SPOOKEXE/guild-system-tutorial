local HttpService = game:GetService("HttpService")
local HttpService = game:GetService("HttpService")
local Players = game:GetService("Players")

local ReplicatedStorage = game:GetService("ReplicatedStorage")
local ReplicatedModules = require(ReplicatedStorage:WaitForChild("Modules"))

local ReplicatedData = ReplicatedModules.Services.ReplicatedData

local SystemsContainer = {}

-- // Module // --
local Module = {}

function Module.OnPlayerAdded( LocalPlayer : Player )
	local profile = SystemsContainer.DataServer.LoadPlayerInstance(LocalPlayer)
	if not profile then
		return
	end

	local guildInfo = SystemsContainer.GuildsServer.GetGuildInfoFromUserId( LocalPlayer.UserId )
	print(HttpService:JSONEncode(guildInfo))
	if guildInfo then
		profile.Data.GuildUUID = guildInfo['guild_id']
		ReplicatedData.SetData('GuildData', guildInfo, {LocalPlayer})
	end
	ReplicatedData.SetData('PlayerData', profile.Data, {LocalPlayer})
end

function Module.OnPlayerRemoving(LocalPlayer)
	ReplicatedData.RemoveDataForPlayer('PlayerData', LocalPlayer)
	SystemsContainer.DataServer.ReleasePlayerInstance(LocalPlayer)
end

function Module.Start()
	SystemsContainer.GuildsServer.PerformHealthCheck()
	SystemsContainer.GuildsServer.SetupAutoHealthCheck()

	for _, LocalPlayer in Players:GetPlayers() do
		task.spawn(Module.OnPlayerAdded, LocalPlayer)
	end
	Players.PlayerAdded:Connect(Module.OnPlayerAdded)
	Players.PlayerRemoving:Connect(Module.OnPlayerRemoving)
end

function Module.Init(otherSystems)
	SystemsContainer = otherSystems
end

return Module
