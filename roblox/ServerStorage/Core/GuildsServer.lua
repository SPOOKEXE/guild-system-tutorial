
local SystemsContainer = {}

type PermissionsDict = { }
type RankData = {}
type GuildInfo = { }
type GuildAuditLog = {}
type GuildChatMessage = {}
type GuildInvite = {}

-- // Internal API // --
local Internal = {}

function Internal.IsRankPermissionsValid( permissions : PermissionsDict ) : boolean
	error('NotImplementedError')
end

function Internal.IsGuildNameAvailable( name : string ) : boolean
	error('NotImplementedError')
end

function Internal.GetGuildInfoFromGuildId( guild_id : number ) : GuildInfo?
	error('NotImplementedError')
end

function Internal.GetGuildInfoFromUserId( user_id : number ) : GuildInfo?
	error('NotImplementedError')
end

function Internal.UpdateGuildDisplayInfo( guild_id : number, user_id : number, description : string, accessibility : number, emblem : number ) : boolean
	error('NotImplementedError')
end

function Internal.CreateGuild( user_id : number, name : string, description : string, emblem : number ) : GuildInfo?
	error('NotImplementedError')
end

function Internal.GetGuildInvites( user_id : number ) : { GuildInvite }
	error('NotImplementedError')
end

function Internal.InviteUserIdToGuild( user_id : number, target_id : number ) : boolean
	error('NotImplementedError')
end

function Internal.AcceptInviteToGuild( user_id : number, invite_id : number ) : boolean
	error('NotImplementedError')
end

function Internal.ChangeUserIdRankInGuild( guild_id : number, source_user_id : number, target_user_id : number, target_rank : number ) : boolean
	error('NotImplementedError')
end

function Internal.ChangeRankPermissionsInGuild( guild_id : number, user_id : number, rank_id : number, permissions : PermissionsDict ) : boolean
	error('NotImplementedError')
end

function Internal.CreateRankInGuild( guild_id : number, user_id : number, name : string ) : RankData?
	error('NotImplementedError')
end

function Internal.RemoveRankInGuild( guild_id : number, user_id : number, rank_id : number ) : boolean
	error('NotImplementedError')
end

function Internal.SetDefaultRankInGuild( guild_id : number, user_id : number, rank_id : number ) : boolean
	error('NotImplementedError')
end

function Internal.KickUserIdFromGuild( guild_id : number, user_id : number, target_id : number ) : boolean
	error('NotImplementedError')
end

function Internal.IgnoreInviteToGuild( user_id : number, invite_id : number ) : boolean
	error('NotImplementedError')
end

function Internal.DeleteGuild( guild_id : number, user_id : number ) : boolean
	error('NotImplementedError')
end

function Internal.TransferGuildOwnership( guild_id : number, user_id : number, target_user_id : number ) : boolean
	error('NotImplementedError')
end

function Internal.GetBannedUserIdsInGuild( guild_id : number, user_id : number ) : {number}
	error('NotImplementedError')
end

function Internal.BanUserIdFromGuild( guild_id : number, user_id : number, target_id : number ) : boolean
	error('NotImplementedError')
end

function Internal.UnbanUserIdFromGuild( guild_id : number, user_id : number, target_id : number ) : boolean
	error('NotImplementedError')
end

function Internal.CreateGuildChatMessage( guild_id : number, user_id : number, message : string ) : boolean
	error('NotImplementedError')
end

function Internal.RemoveGuildChatMessage( guild_id : number, user_id : number, message_id : number ) : boolean
	error('NotImplementedError')
end

function Internal.GetGuildChatMessages( guild_id : number, user_id : number, page_number : number, items_per_page : number ) : { GuildChatMessage }
	error('NotImplementedError')
end

--[[
	Move to python server - after every action create a audit log automatically?
	Otherwise have a server-only audit log and a roblox-only audit log and
	keep them in separate database tables
]]
function Internal.CreateGuildAuditLog( guild_id : number, user_id : number, action : number, args : {any} ) : boolean
	error('NotImplementedError')
end

function Internal.GetGuildAuditLogs( guild_id : number, user_id : number, page_number : number, items_per_page : number ) : { GuildAuditLog }
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
