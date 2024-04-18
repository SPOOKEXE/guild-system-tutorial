
import uvicorn
import asyncio

from typing import Union
from fastapi import FastAPI, Body
from guilds import InternalGuildsAPI, DEFAULT_GUILD_AUDIT_LOG_LIMIT, DEFAULT_GUILD_CHAT_MESSAGE_LIMIT

async def host_fastapp( app : FastAPI, host : str, port : int ) -> None:
	print(f"Hosting App: {app.title}")
	await uvicorn.Server(uvicorn.Config(app, host=host, port=port, log_level='debug')).serve()

guilds_api = FastAPI(title="Guilds API", description="Tutorial Series Guilds API", version="0.0.2")

@guilds_api.post('/is-rank-permissions-valid', summary='IsRankPermissionsValid', tags=['guild-core'])
async def IsRankPermissionsValid(
	permissions : dict = Body(None, embed=True)
) -> bool:
	return await InternalGuildsAPI.IsRankPermissionsValid(permissions)

@guilds_api.post('/is-guild-name-available', summary='IsGuildNameAvailable', tags=['guild-core'])
async def IsGuildNameAvailable(
	name : str = Body(None, embed=True)
) -> bool:
	return await InternalGuildsAPI.IsGuildNameAvailable(name)

@guilds_api.post('/get-guild-info-from-guild-id', summary='GetGuildInfoFromGuildId', tags=['guild-core'])
async def GetGuildInfoFromGuildId(
	guild_id : int = Body(None, embed=True)
) -> Union[dict, None]:
	return await InternalGuildsAPI.GetGuildInfoFromGuildId(guild_id)

@guilds_api.post('/get-guild-info-from-user-id', summary='GetGuildInfoFromGuildId', tags=['guild-core'])
async def GetGuildInfoFromUserId(
	user_id : int = Body(None, embed=True)
) -> Union[dict, None]:
	return await InternalGuildsAPI.GetGuildInfoFromUserId(user_id)

@guilds_api.post('/update-guild-display-info', summary='UpdateGuildDisplayInfo', tags=['guild-core'])
async def UpdateGuildDisplayInfo(
	guild_id : int = Body(None, embed=True),
	description : str = Body(None, embed=True),
	accessibility : int = Body(None, embed=True),
	emblem : int = Body(None, embed=True)
) -> Union[dict, None]:
	return await InternalGuildsAPI.UpdateGuildDisplayInfo(guild_id, description, accessibility, emblem)

@guilds_api.post('/create-guild', summary='CreateGuild', tags=['guild-core'])
async def CreateGuild(
	user_id : int = Body(None, embed=True),
	name : str = Body(None, embed=True),
	description : str = Body(None, embed=True),
	emblem : int = Body(None, embed=True)
) -> Union[dict, None]:
	return await InternalGuildsAPI.CreateGuild(user_id, name, description, emblem)

@guilds_api.post('/change-user-id-rank-in-guild', summary='ChangeUserIdRankInGuild', tags=['guild-core'])
async def ChangeUserIdRankInGuild(
	guild_id : int = Body(None, embed=True),
	target_id : int = Body(None, embed=True),
	rank_id : int = Body(None, embed=True)
) -> None:
	return await InternalGuildsAPI.ChangeUserIdRankInGuild(guild_id, target_id, rank_id)

@guilds_api.post('/change-guild-rank-permissions', summary='ChangeGuildRankPermissions', tags=['guild-core'])
async def ChangeRankPermissionsInGuild(
	guild_id : int = Body(None, embed=True),
	rank_id : int = Body(None, embed=True),
	permissions : dict = Body(None, embed=True)
) -> None:
	return await InternalGuildsAPI.ChangeRankPermissionsInGuild(guild_id, rank_id, permissions)

@guilds_api.post('/create-rank-in-guild', summary='CreateRankInGuild', tags=['guild-core'])
async def CreateRankInGuild(
	guild_id : int = Body(None, embed=True),
	name : str = Body(None, embed=True),
	protected : bool = Body(False, embed=True)
) -> None:
	return await InternalGuildsAPI.CreateRankInGuild(guild_id, name, protected=protected)

@guilds_api.post('/remove-rank-in-guild', summary='RemoveRankInGuild', tags=['guild-core'])
async def RemoveRankInGuild(
	guild_id : int = Body(None, embed=True),
	rank_id : int = Body(None, embed=True)
) -> None:
	return await InternalGuildsAPI.RemoveRankInGuild(guild_id, rank_id)

@guilds_api.post('/set-default-rank-in-guild', summary='SetDefaultRankInGuild', tags=['guild-core'])
async def SetDefaultRankInGuild(
	guild_id : int = Body(None, embed=True),
	rank_id : int = Body(None, embed=True)
) -> None:
	return await InternalGuildsAPI.SetDefaultRankInGuild(guild_id, rank_id)

@guilds_api.post('/kick-user-id-from-guild', summary='KickUserIdFromGuild', tags=['guild-core'])
async def KickUserIdFromGuild(
	guild_id : int = Body(None, embed=True),
	target_id : int = Body(None, embed=True),
) -> None:
	return await InternalGuildsAPI.KickUserIdFromGuild(guild_id, target_id)

@guilds_api.post('/delete-guild', summary='DeleteGuild', tags=['guild-core'])
async def DeleteGuild(
	guild_id : int = Body(None, embed=True),
) -> None:
	return await InternalGuildsAPI.DeleteGuild(guild_id)

@guilds_api.post('/transfer-guild-ownership', summary='TransferGuildOwnership', tags=['guild-core'])
async def TransferGuildOwnership(
	guild_id : int = Body(None, embed=True),
	target_id : int = Body(None, embed=True)
) -> None:
	return await InternalGuildsAPI.TransferGuildOwnership(guild_id, target_id)

@guilds_api.post('/get-guild-banned-user-ids', summary='GetGuildBannedUserIds', tags=['guild-core'])
async def GetGuildBannedUserIds(
	guild_id : int = Body(None, embed=True),
) -> None:
	return await InternalGuildsAPI.GetGuildBannedUserIds(guild_id)

@guilds_api.post('/ban-user-id-from-guild', summary='BanUserIdFromGuild', tags=['guild-core'])
async def BanUserIdFromGuild(
	guild_id : int = Body(None, embed=True),
	target_id : int = Body(None, embed=True)
) -> None:
	return await InternalGuildsAPI.BanUserIdFromGuild(guild_id, target_id)

@guilds_api.post('/unban-user-id-from-guild', summary='UnbanUserIdFromGuild', tags=['guild-core'])
async def UnbanUserIdFromGuild(
	guild_id : int = Body(None, embed=True),
	target_id : int = Body(None, embed=True)
) -> None:
	return await InternalGuildsAPI.UnbanUserIdFromGuild(guild_id, target_id)

@guilds_api.post('/create-guild-chat-message', summary='CreateGuildChatMessage', tags=['guild-chat'])
async def CreateGuildChatMessage(
	guild_id : int = Body(None, embed=True),
	user_id : int = Body(None, embed=True),
	message : str = Body(None, embed=True)
) -> None:
	return await InternalGuildsAPI.CreateGuildChatMessage(guild_id, user_id, message)

@guilds_api.post('/remove-guild-chat-message', summary='RemoveGuildChatMessage', tags=['guild-chat'])
async def RemoveGuildChatMessage(
	guild_id : int = Body(None, embed=True),
	message_id : int = Body(None, embed=True)
) -> None:
	return await InternalGuildsAPI.RemoveGuildChatMessage(guild_id, message_id)

@guilds_api.post('/get-guild-chat-messages', summary='GetGuildChatMessages', tags=['guild-chat'])
async def GetGuildChatMessages(
	guild_id : int = Body(None, embed=True),
	offset : int = Body(0, embed=True),
	limit : int = Body(DEFAULT_GUILD_CHAT_MESSAGE_LIMIT, embed=True)
) -> None:
	return await InternalGuildsAPI.GetGuildChatMessages(guild_id, offset, limit)

@guilds_api.post('/create-guild-audit-log', summary='CreateGuildAuditLog', tags=['guild-audit-log'])
async def CreateGuildAuditLog(
	guild_id : int = Body(None, embed=True),
	user_id : int = Body(None, embed=True),
	action : str = Body(None, embed=True),
	args : list = Body(list, embed=True),
) -> None:
	return await InternalGuildsAPI.CreateGuildAuditLog(guild_id, user_id, action, args)

@guilds_api.post('/get-guild-audit-logs', summary='GetGuildAuditLogs', tags=['guild-audit-log'])
async def GetGuildAuditLogs(
	guild_id : int = Body(None, embed=True),
	offset : int = Body(0, embed=True),
	limit : int = Body(DEFAULT_GUILD_AUDIT_LOG_LIMIT, embed=True)
) -> None:
	return await InternalGuildsAPI.GetGuildAuditLogs(guild_id, offset, limit)

@guilds_api.post('/get-full-guild-info-from-guild-id', summary='GetFullGuildInfoFromGuildId', tags=['guild-core'])
async def GetFullGuildInfoFromGuildId( guild_id : int, user_id : int ) -> Union[dict, None]:
	return await InternalGuildsAPI.GetFullGuildInfoFromGuildId(guild_id, user_id)

@guilds_api.post('/get-full-guild-info-from-user-id', summary='GetFullGuildInfoFromUserId', tags=['guild-core'])
async def GetFullGuildInfoFromUserId( guild_id : int, user_id : int ) -> Union[dict, None]:
	return await InternalGuildsAPI.GetFullGuildInfoFromUserId(guild_id, user_id)

@guilds_api.post('/get-guild-ranks', summary='GetGuildRanks', tags=['guild-core'])
async def GetGuildRanks( guild_id : int ) -> Union[list[dict], None]:
	return await InternalGuildsAPI.GetGuildRanks(guild_id)

@guilds_api.post('/get-guild-members', summary='GetGuildMembers', tags=['guild-core'])
async def GetGuildMembers( guild_id : int ) -> Union[list[dict], None]:
	return await InternalGuildsAPI.GetGuildMembers(guild_id)

@guilds_api.post('/get-created-guilds', summary='GetCreatedGuilds', tags=['guild-core'])
async def GetCreatedGuilds(
	offset : int = Body(0, embed=True),
	limit : int = Body(DEFAULT_GUILD_CHAT_MESSAGE_LIMIT, embed=True)
) -> list[dict]:
	return await InternalGuildsAPI.GetCreatedGuilds(offset=offset, limit=limit)

@guilds_api.post('/get-created-guilds-full', summary='GetCreatedGuildsFull', tags=['guild-core'])
async def GetCreatedGuildsFull(
	offset : int = Body(0, embed=True),
	limit : int = Body(DEFAULT_GUILD_CHAT_MESSAGE_LIMIT, embed=True)
) -> list[dict]:
	return await InternalGuildsAPI.GetCreatedGuildsFull(offset=offset, limit=limit)

async def main( host : str = '0.0.0.0', port : int = 5100 ) -> None:
	await host_fastapp(guilds_api, host, port)

if __name__ == '__main__':
	asyncio.run(main(host='127.0.0.1', port=5100))
