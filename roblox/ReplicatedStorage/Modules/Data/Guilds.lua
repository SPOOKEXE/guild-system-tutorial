
local Module = {}

Module.Emblems = {
	'rbxassetid://11200910338',
	'rbxassetid://12886344712',
	'rbxassetid://12711372482',
	'rbxassetid://12694655016',
	'rbxassetid://15067320350',
}

Module.RemoteEnums = {
	-- misc
	IsPermissionsValid = 1,
	IsGuildNameAvailable = 2,
	QueryGuildInfo = 3,
	-- your guild
	GetMyGuildInfo = 10,
	GetOtherGuildInfo = 11,
	-- guild operations
	GetGuildChatMessages = 20,
	GetGuildAuditLogs = 21,
	UpdateGuildDisplayInfo = 22,
	SetUserRankInGuild = 23,
	CreateRankInGuild = 24,
	RemoveRankInGuild = 25,
	ChangeGuildRankName = 26,
	BanUserIdFromGuild = 27,
	UnbanUserIdFromGuild = 28,
	GetGuildBannedUserIds = 29,
	SetDefaultRankInGuild = 30,
	ChangeGuildRankPermissions = 31,
	-- invites
	GetGuildInvites = 60,
	InviteToGuild = 61,
	CancelGuildInvite = 62,
	AcceptGuildInvite = 63,
	KickUserIdFromGuild = 64,
	-- misc
	CreateGuild = 91,
	LeaveGuild = 92,
	DeleteGuild = 93,
	TransferGuildOwnership = 94,
}

return Module
