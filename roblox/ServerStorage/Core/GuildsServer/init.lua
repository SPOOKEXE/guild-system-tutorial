
local GuildsInternal = require(script.GuildsInternal)

local SystemsContainer = {}

-- // Module // --
local Module = {}

function Module.Start()

	GuildsInternal.SetAPIUrl('http://127.0.0.1:5100')
	GuildsInternal.SetAPIKey('guilds-api-key-10001010101')
	if not GuildsInternal.HealthCheck() then
		warn('Failed to connect to the Guilds API. Guilds is unavailable.')
		return
	end

end

function Module.Init(otherSystems)
	SystemsContainer = otherSystems
end

return Module
