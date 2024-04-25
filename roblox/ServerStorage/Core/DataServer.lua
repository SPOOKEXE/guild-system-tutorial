local Players = game:GetService('Players')
local RunService = game:GetService('RunService')

local ServerStorage = game:GetService("ServerStorage")
local ServerModules = require(ServerStorage:WaitForChild("Modules"))

local ProfileService = ServerModules.Libraries.ProfileService

local SystemsContainer = {}

local Loading = {}
local ProfileCache = {}
local GameProfileStore = false

local TemplateData = {
	Level = 1,
	Experience = 0,

	GuildUUID = false,
}

-- // Module // --
local Module = { TemplateData = TemplateData }

-- Get the player's profile (optional yield until present)
function Module.GetProfileFromPlayer( LocalPlayer, yield )
	if yield then
		while (not ProfileCache[LocalPlayer.UserId]) and LocalPlayer:IsDescendantOf(Players) do
			RunService.Heartbeat:Wait()
		end
	end
	return ProfileCache[LocalPlayer.UserId]
end

-- Load the user id's data profile
function Module.LoadUserId( UserId )
	if Loading[ UserId ] then
		while Loading[ UserId ] do
			RunService.Heartbeat:Wait()
		end
		return ProfileCache[ UserId ], true
	end

	if ProfileCache[UserId] then
		return ProfileCache[UserId], true
	end

	Loading[ UserId ] = true

	local LoadedProfile = GameProfileStore:LoadProfileAsync( tostring(UserId), "ForceLoad" )
	if LoadedProfile then
		LoadedProfile:Reconcile()
		LoadedProfile:AddUserId(UserId)
		LoadedProfile:ListenToRelease(function()
			ProfileCache[UserId] = nil
		end)
		ProfileCache[UserId] = LoadedProfile
	else
		ProfileCache[UserId] = nil
	end

	Loading[ UserId ] = nil
	return LoadedProfile, false
end

-- Load the given player's data profile
function Module.LoadPlayerInstance( LocalPlayer )
	local UserId = LocalPlayer.UserId

	local Profile, wasCached = Module.LoadUserId( UserId )
	if not Profile then
		LocalPlayer:Kick('Failed to load your profile data.')
		return false
	end

	Profile:ListenToRelease(function()
		ProfileCache[UserId] = nil
	end)

	if LocalPlayer:IsDescendantOf(Players) then
		ProfileCache[LocalPlayer.UserId] = Profile
	else
		Profile:Release()
		ProfileCache[LocalPlayer.UserId] = nil
	end

	return Profile, wasCached
end

-- Release the data profile for this given userId
function Module.ReleaseUserId( UserId )
	if ProfileCache[UserId] then
		ProfileCache[UserId]:Release()
	end
	ProfileCache[UserId] = nil
	Loading[UserId] = nil
end

-- Release the given player's data profile
function Module.ReleasePlayerInstance( LocalPlayer )
	return Module.ReleaseUserId( LocalPlayer.UserId )
end

-- Delete a player's data
function Module.DeleteUserId( UserId )
	if GameProfileStore then
		GameProfileStore:RemoveAsync( tostring(UserId) )
	end
end

function Module.Start()

end

function Module.Init(otherSystems)
	SystemsContainer = otherSystems

	-- NOTE: .Mock means data DOES NOT save.
	GameProfileStore = ProfileService.GetProfileStore('PlayerData1', TemplateData).Mock
end

return Module
