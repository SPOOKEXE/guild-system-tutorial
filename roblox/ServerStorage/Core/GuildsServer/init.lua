
--[[
	TODO:
	- remote cooldown
	- caching of guild data
	- guild invite with MessagingService/MemoryStoreService
]]

local HttpService = game:GetService("HttpService")
local MemoryStoreService = game:GetService("MemoryStoreService")

local Players = game:GetService("Players")
local ServerStorage = game:GetService("ServerStorage")
local ServerModules = require(ServerStorage:WaitForChild("Modules"))

local MessagingWrapper = ServerModules.Libraries.MessagingWrapper

local ReplicatedStorage = game:GetService("ReplicatedStorage")
local ReplicatedModules = require(ReplicatedStorage:WaitForChild("Modules"))

local GuildsConfigModule = ReplicatedModules.Data.Guilds

local RNetModule = ReplicatedModules.Libraries.RNet
local GuildsBridge = RNetModule.Create('GuildsBridge')

local GuildsInternal = require(script.GuildsInternal)

local SystemsContainer = {}


-- // Module // --
local Module = {}

Module.GuildsAvailable = false
Module.GuildsInternal = GuildsInternal

Module.GuildCache = {}
Module.UserIdToGuildId = {}

function Module.SetCachedGuildData( guild_data : {} )
	local guild_id = Module.GuildCache['guild_id']
	if not guild_id then
		return
	end
	for _, member in guild_data['members'] do
		Module.SetUserIdGuildId( member['user_id'], guild_id )
	end
	Module.GuildCache[guild_id] = guild_data
end

function Module.GetCachedGuildData( guild_id : number )
	return Module.GuildCache[guild_id]
end

function Module.SetUserIdGuildId( userId : number, guildId : number )
	Module.UserIdToGuildId[userId] = guildId
end

function Module.GetUserIdGuildInfo( userId : number ) : {}?
	local guild_id = Module.UserIdToGuildId[ userId ]
	if guild_id then
		return Module.GetCachedGuildData( guild_id )
	end
	return nil
end

function Module.GetGuildInfoFromUserId( userId : number )
	local info = Module.GetUserIdGuildInfo( userId )
	if info then
		return info
	end
	local data = Module.GuildsAvailable and GuildsInternal.GetFullGuildInfoFromUserId( userId )
	if data then
		Module.SetCachedGuildData( data )
	end
	return data
end

function Module.HandleRemoteInvoke( LocalPlayer : Player, ... )

	local args = {...}
	local job = table.remove(args, 1)
	if job == GuildsConfigModule.RemoteEnums.CreateGuild then

		local name, description, emblem = unpack(args)
		if typeof(name) ~= 'string' or #name < 3 or #name > 12 then
			return false, 'Invalid name.'
		end
		if typeof(description) ~= 'string' or #name > 100 then
			return false, 'Invalid description.'
		end
		if typeof(emblem) ~= 'number' or emblem < 0 or emblem > #GuildsConfigModule.Emblems then
			return false, 'Invalid emblem.'
		end

		local profile = SystemsContainer.DataServer.GetProfileFromPlayer( LocalPlayer, false )
		if not profile then
			return false, 'No Player Profile.'
		end

		if profile.Data.GuildUUID then
			return false, 'You are already in a guild.'
		end

		local Data = GuildsInternal.CreateGuild( LocalPlayer.UserId, name, description, emblem )
		print(Data)
		if Data then
			profile.Data.GuildUUID = Data['guild_id']
			--task.spawn(Module.CacheGuildData, Data)
			return true, 'Guild was created.'
		else
			return false, 'Could not create the guild.'
		end
	end

	return false, 'Invalid Job.'

end

function Module.HandleRemoteEvent( LocalPlayer, ... )
	print( LocalPlayer.Name, ... )
	--[[
		if job == GuildsConfigModule.RemoteEnums.QueryGuildInfo then

		elseif job == GuildsConfigModule.RemoteEnums.IsPermissionsValid then

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

		elseif job == GuildsConfigModule.RemoteEnums.GetGuildInvites then

		elseif job == GuildsConfigModule.RemoteEnums.InviteToGuild then

		elseif job == GuildsConfigModule.RemoteEnums.CancelGuildInvite then

		elseif job == GuildsConfigModule.RemoteEnums.AcceptGuildInvite then

		elseif job == GuildsConfigModule.RemoteEnums.KickUserIdFromGuild then

		elseif job == GuildsConfigModule.RemoteEnums.LeaveGuild then

		elseif job == GuildsConfigModule.RemoteEnums.DeleteGuild then

		elseif job == GuildsConfigModule.RemoteEnums.TransferGuildOwnership then

		end
	]]

end

function Module.SetupMessagingHandlers()

	MessagingWrapper.Subscribe('GuildMessaging', function(data)
		print(data and HttpService:GenerateGUID(data) or 'no data')
	end)

	task.spawn(function()
		MessagingWrapper.Publish('GuildMessaging', 'Hello from the other siiiideeeee.')
	end)

end

function Module.PerformHealthCheck()
	if not HttpService.HttpEnabled then
		warn('HttpService.HttpEnabled must be true for guild system to be functional.')
		return
	end
	local Available = GuildsInternal.HealthCheck() and true or false
	Module.GuildsAvailable = Available
	workspace:SetAttribute('GuildsAvailable', Available)
end

function Module.SetupAutoHealthCheck()
	task.spawn(function()
		while true do
			Module.PerformHealthCheck()
			task.wait(10)
		end
	end)
end

function Module.Start()

	workspace:SetAttribute('GuildsAvailable', false)
	GuildsInternal.SetAPIUrl('http://127.0.0.1:5100')
	GuildsInternal.SetAPIKey('guilds-api-key-10001010101')

	task.spawn(Module.SetupMessagingHandlers)
	GuildsBridge:OnServerEvent(Module.HandleRemoteEvent)
	GuildsBridge:OnServerInvoke(Module.HandleRemoteInvoke)

end

function Module.Init(otherSystems)
	SystemsContainer = otherSystems
end

return Module
