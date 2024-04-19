
local ReplicatedStorage = game:GetService("ReplicatedStorage")
local ReplicatedModules = require(ReplicatedStorage:WaitForChild("Modules"))

local GuildsConfigModule = ReplicatedModules.Data.Guilds

local RNetModule = ReplicatedModules.Libraries.RNet
local GuildsBridge = RNetModule.Create('GuildsBridge')

local GuildsInternal = require(script.GuildsInternal)

local SystemsContainer = {}

-- // Module // --
local Module = {}

Module.GuildsInternal = GuildsInternal

--[[

TODO:
- remote cooldown
- caching of guild data
- guild invite with MessagingService/MemoryStoreService

]]

function Module.HandleRemoteEvent( LocalPlayer, ... )
	print( LocalPlayer.Name, ... )

	--[[
		local args = {...}
		local job = table.remove(args, 1)
		if job == GuildsConfigModule.RemoteEnums.IsPermissionsValid then

		elseif job == GuildsConfigModule.RemoteEnums.IsGuildNameAvailable then

		elseif job == GuildsConfigModule.RemoteEnums.GetMyGuildInfo then

		elseif job == GuildsConfigModule.RemoteEnums.GetOtherGuildInfo then

		elseif job == GuildsConfigModule.RemoteEnums.GetGuildChatMessages then

		elseif job == GuildsConfigModule.RemoteEnums.GetGuildAuditLogs then

		elseif job == GuildsConfigModule.RemoteEnums.UpdateGuildDisplayInfo then

		elseif job == GuildsConfigModule.RemoteEnums.SetUserRankInGuild then

		elseif job == GuildsConfigModule.RemoteEnums.CreateRankInGuild then

		elseif job == GuildsConfigModule.RemoteEnums.RemoveRankInGuild then

		elseif job == GuildsConfigModule.RemoteEnums.ChangeGuildRankName then

		elseif job == GuildsConfigModule.RemoteEnums.BanUserIdFromGuild then

		elseif job == GuildsConfigModule.RemoteEnums.UnbanUserIdFromGuild then

		elseif job == GuildsConfigModule.RemoteEnums.GetGuildBannedUserIds then

		elseif job == GuildsConfigModule.RemoteEnums.SetDefaultRankInGuild then

		elseif job == GuildsConfigModule.RemoteEnums.ChangeGuildRankPermissions then

		elseif job == GuildsConfigModule.RemoteEnums.InviteToGuild then

		elseif job == GuildsConfigModule.RemoteEnums.CancelGuildInvite then

		elseif job == GuildsConfigModule.RemoteEnums.AcceptGuildInvite then

		elseif job == GuildsConfigModule.RemoteEnums.KickUserIdFromGuild then

		elseif job == GuildsConfigModule.RemoteEnums.CreateGuild then

		elseif job == GuildsConfigModule.RemoteEnums.LeaveGuild then

		elseif job == GuildsConfigModule.RemoteEnums.DeleteGuild then

		elseif job == GuildsConfigModule.RemoteEnums.TransferGuildOwnership then

		end
	]]
end

function Module.Start()

	GuildsInternal.SetAPIUrl('http://127.0.0.1:5100')
	GuildsInternal.SetAPIKey('guilds-api-key-10001010101')
	if not GuildsInternal.HealthCheck() then
		warn('Failed to connect to the Guilds API. Guilds is unavailable.')
		return
	end

	GuildsBridge.OnServerEvent(Module.HandleRemoteEvent)

end

function Module.Init(otherSystems)
	SystemsContainer = otherSystems
end

return Module
