
local SystemsContainer = {}

type PermissionsDict = { }
type RankData = {}
type GuildInfo = { }
type GuildAuditLog = {}
type GuildChatMessage = {}
type GuildInvite = {}

-- // APIInternal API // --
local APIInternal = {}

function APIInternal.IsRankPermissionsValid( permissions : PermissionsDict ) : boolean
	error('NotImplementedError')
end

function APIInternal.IsGuildNameAvailable( name : string ) : boolean
	error('NotImplementedError')
end

function APIInternal.GetGuildInfoFromGuildId( guild_id : number ) : GuildInfo?
	error('NotImplementedError')
end

function APIInternal.GetGuildInfoFromUserId( user_id : number ) : GuildInfo?
	error('NotImplementedError')
end

function APIInternal.UpdateGuildDisplayInfo( guild_id : number, user_id : number, description : string, accessibility : number, emblem : number ) : boolean
	error('NotImplementedError')
end

function APIInternal.CreateGuild( user_id : number, name : string, description : string, emblem : number ) : GuildInfo?
	error('NotImplementedError')
end

function APIInternal.ChangeUserIdRankInGuild( guild_id : number, source_user_id : number, target_user_id : number, target_rank : number ) : boolean
	error('NotImplementedError')
end

function APIInternal.ChangeRankPermissionsInGuild( guild_id : number, user_id : number, rank_id : number, permissions : PermissionsDict ) : boolean
	error('NotImplementedError')
end

function APIInternal.CreateRankInGuild( guild_id : number, user_id : number, name : string ) : RankData?
	error('NotImplementedError')
end

function APIInternal.RemoveRankInGuild( guild_id : number, user_id : number, rank_id : number ) : boolean
	error('NotImplementedError')
end

function APIInternal.SetDefaultRankInGuild( guild_id : number, user_id : number, rank_id : number ) : boolean
	error('NotImplementedError')
end

function APIInternal.KickUserIdFromGuild( guild_id : number, user_id : number, target_id : number ) : boolean
	error('NotImplementedError')
end

function APIInternal.DeleteGuild( guild_id : number, user_id : number ) : boolean
	error('NotImplementedError')
end

function APIInternal.TransferGuildOwnership( guild_id : number, user_id : number, target_user_id : number ) : boolean
	error('NotImplementedError')
end

function APIInternal.GetBannedUserIdsInGuild( guild_id : number, user_id : number ) : {number}
	error('NotImplementedError')
end

function APIInternal.BanUserIdFromGuild( guild_id : number, user_id : number, target_id : number ) : boolean
	error('NotImplementedError')
end

function APIInternal.UnbanUserIdFromGuild( guild_id : number, user_id : number, target_id : number ) : boolean
	error('NotImplementedError')
end

function APIInternal.CreateGuildChatMessage( guild_id : number, user_id : number, message : string ) : boolean
	error('NotImplementedError')
end

function APIInternal.RemoveGuildChatMessage( guild_id : number, user_id : number, message_id : number ) : boolean
	error('NotImplementedError')
end

function APIInternal.GetGuildChatMessages( guild_id : number, user_id : number, page_number : number, items_per_page : number ) : { GuildChatMessage }
	error('NotImplementedError')
end

--[[
	Move to python server - after every action create a audit log automatically?
	Otherwise have a server-only audit log and a roblox-only audit log and
	keep them in separate database tables
]]
function APIInternal.CreateGuildAuditLog( guild_id : number, user_id : number, action : number, args : {any} ) : boolean
	error('NotImplementedError')
end

function APIInternal.GetGuildAuditLogs( guild_id : number, user_id : number, page_number : number, items_per_page : number ) : { GuildAuditLog }
	error('NotImplementedError')
end

-- // Roblox APIInternal // --
local RobloxInternal = {}

function RobloxInternal.IgnoreInviteToGuild( user_id : number, invite_id : number ) : boolean
	error('NotImplementedError')
end

function RobloxInternal.GetGuildInvites( user_id : number ) : { GuildInvite }
	error('NotImplementedError')
end

function RobloxInternal.InviteUserIdToGuild( user_id : number, target_id : number ) : boolean
	error('NotImplementedError')
end

function RobloxInternal.AcceptInviteToGuild( user_id : number, invite_id : number ) : boolean
	error('NotImplementedError')
end

-- // Module // --
local Module = {}

function Module.Start()

end

function Module.Init(otherSystems)
	SystemsContainer = otherSystems
end

return Module
