
local API_URL = 'http://127.0.0.1:5100'
local API_KEY = ''

type HttpMethods = 'POST' | 'GET'
type RequestAsyncResponse = {
	Success : boolean,
	StatusCode : number,
	StatusMessage : string,
	Headers : {}?,
	Body : {}?,
}

local HttpService = game:GetService("HttpService")

local function RequestAPIAsync( path : string, method : HttpMethods, body : {}? ) : RequestAsyncResponse
	if not HttpService.HttpEnabled then
		warn('HttpService.HttpEnabled must be enabled for the GuildsAPI to work.')
		return nil
	end

	local success, err = pcall(function()
		return HttpService:RequestAsync({
			Url = API_URL..path,
			Method = method,
			Headers = { ["Content-Type"] = "application/json", ["X-API-KEY"] = API_KEY },
			Body = body and HttpService:JSONEncode(body),
		})
	end)

	if success then
		return err
	end

	warn(err)
	return nil
end

-- // APIInternal API // --
local APIInternal = {}

function APIInternal.SetAPIUrl( api_url : string )
	API_URL = api_url
end

function APIInternal.SetAPIKey( api_key : string )
	API_KEY = api_key
end

function APIInternal.HealthCheck() : boolean
	return RequestAPIAsync('/health', 'GET', nil) ~= nil
end

function APIInternal.IsRankPermissionsValid( permissions : PermissionsDict ) : boolean
	--local response = RequestAPIAsync( '/guilds/add-user-to-guild', 'POST', { guild_id=guild_id, user_id=user_id } )
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

function APIInternal.UpdateGuildDisplayInfo( guild_id : number, description : string, accessibility : number, emblem : number ) : boolean
	error('NotImplementedError')
end

function APIInternal.CreateGuild( user_id : number, name : string, description : string, emblem : number ) : GuildInfo?
	error('NotImplementedError')
end

function APIInternal.ChangeUserIdRankInGuild( guild_id : number, target_user_id : number, target_rank : number ) : boolean
	error('NotImplementedError')
end

function APIInternal.ChangeRankPermissionsInGuild( guild_id : number, rank_id : number, permissions : PermissionsDict ) : boolean
	error('NotImplementedError')
end

function APIInternal.CreateRankInGuild( guild_id : number, name : string ) : RankData?
	error('NotImplementedError')
end

function APIInternal.RemoveRankInGuild( guild_id : number, rank_id : number ) : boolean
	error('NotImplementedError')
end

function APIInternal.SetDefaultRankInGuild( guild_id : number, rank_id : number ) : boolean
	error('NotImplementedError')
end

function APIInternal.KickUserIdFromGuild( guild_id : number, target_id : number ) : boolean
	error('NotImplementedError')
end

function APIInternal.DeleteGuild( guild_id : number ) : boolean
	error('NotImplementedError')
end

function APIInternal.TransferGuildOwnership( guild_id : number, user_id : number ) : boolean
	error('NotImplementedError')
end

function APIInternal.GetBannedUserIdsInGuild( guild_id : number ) : {number}
	error('NotImplementedError')
end

function APIInternal.BanUserIdFromGuild( guild_id : number, user_id : number ) : boolean
	error('NotImplementedError')
end

function APIInternal.UnbanUserIdFromGuild( guild_id : number, user_id : number ) : boolean
	error('NotImplementedError')
end

function APIInternal.CreateGuildChatMessage( guild_id : number, user_id : number, message : string ) : boolean
	error('NotImplementedError')
end

function APIInternal.RemoveGuildChatMessage( guild_id : number, message_id : number ) : boolean
	error('NotImplementedError')
end

function APIInternal.GetGuildChatMessages( guild_id : number, page_number : number, items_per_page : number ) : { GuildChatMessage }
	error('NotImplementedError')
end

function APIInternal.CreateGuildAuditLog( guild_id : number, user_id : number, action : number, args : {any} ) : boolean
	error('NotImplementedError')
end

function APIInternal.GetGuildAuditLogs( guild_id : number, page_number : number, items_per_page : number ) : { GuildAuditLog }
	error('NotImplementedError')
end

return APIInternal
