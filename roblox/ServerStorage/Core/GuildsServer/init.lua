
type PermissionsDict = { }
type RankData = {}
type GuildInfo = { }
type GuildAuditLog = {}
type GuildChatMessage = {}
type GuildInvite = {}

local GuildsInternal = require(script.GuildsInternal)

local SystemsContainer = {}

-- // Module // --
local Module = {}

function Module.Start()

end

function Module.Init(otherSystems)
	SystemsContainer = otherSystems

	GuildsInternal.SetAPIUrl('http://127.0.0.1:5100')
	GuildsInternal.SetAPIKey('guilds-api-key-10001010101')
end

return Module
