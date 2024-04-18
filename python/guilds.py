
from __future__ import annotations
from typing import Any, Union
from fastapi import Body
from pydantic import BaseModel
from database import DatabaseAPI

import asyncio
import time

DEFAULT_GUILD_CHAT_MESSAGE_LIMIT : int = 50
DEFAULT_GUILD_AUDIT_LOG_LIMIT : int = 50

def get_time() -> int:
	return int(round(time.time()))

class InternalGuildsAPI:

	DATABASE_NAME : str = 'guilds'

	async def initialize( ) -> None:
		constructors = [
			"CREATE TABLE IF NOT EXISTS master (guild_id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT NOT NULL, description TEXT NOT NULL, accessibility INTEGER DEFAULT 0, emblem INTEGER NOT NULL, owner_id INTEGER NOT NULL, default_rank_id INTEGER DEFAULT -1, total_members INTEGER DEFAULT 1, total_online INTEGER DEFAULT 0, creation INTEGER NOT NULL);",
			"CREATE TABLE IF NOT EXISTS members (user_id INTEGER PRIMARY KEY UNIQUE, guild_id INTEGER NOT NULL, rank_id INTEGER DEFAULT -1, timestamp INTEGER NOT NULL);",
			"CREATE TABLE IF NOT EXISTS ranks (rank_id INTEGER PRIMARY KEY AUTOINCREMENT, guild_id INTEGER NOT NULL, name TEXT NOT NULL, permissions TEXT NOT NULL);",
			"CREATE TABLE IF NOT EXISTS banned (id INTEGER PRIMARY KEY AUTOINCREMENT, guild_id INTEGER, banned_json TEXT)",
			"CREATE TABLE IF NOT EXISTS guild_chat (id INTEGER PRIMARY KEY AUTOINCREMENT, guild_id INTEGER, user_id INTEGER, message TEXT, timestamp INTEGER, deleted INTEGER)",
			"CREATE TABLE IF NOT EXISTS audit_logs (id INTEGER PRIMARY KEY AUTOINCREMENT, guild_id INTEGER, user_id INTEGER, rank_id INTEGER, timestamp INTEGER, action INTEGER, args TEXT)"
		]
		await DatabaseAPI.register_database(InternalGuildsAPI.DATABASE_NAME, constructors)

	async def IsRankPermissionsValid(
			permissions : dict
		) -> bool:
		raise NotImplementedError

	async def IsGuildNameAvailable(
			name : str
		) -> bool:
		raise NotImplementedError

	async def GetGuildInfoFromGuildId(
			guild_id : int
		) -> Union[dict, None]:
		raise NotImplementedError

	async def GetGuildInfoFromUserId(
			user_id : int
		) -> Union[dict, None]:
		raise NotImplementedError

	async def GetGuildMembers(
			guild_id : int
		) -> Union[list[dict], None]:
		raise NotImplementedError

	async def GetFullGuildInfoFromGuildId(
			guild_id : int
		) -> Union[dict, None]:
		raise NotImplementedError

	async def GetFullGuildInfoFromUserId(
			user_id : int
		) -> Union[dict, None]:
		raise NotImplementedError

	async def UpdateGuildDisplayInfo(
		guild_id : int,
		description : str,
		accessibility : int,
		emblem : int
	) -> Union[dict, None]:
		raise NotImplementedError

	async def CreateGuild(
		user_id : int,
		name : str,
		description : str,
		emblem : int
	) -> Union[dict, None]:
		raise NotImplementedError

	async def ChangeUserIdRankInGuild(
		guild_id : int,
		target_id : int,
		rank_id : int
	) -> None:
		raise NotImplementedError

	async def ChangeRankPermissionsInGuild(
		guild_id : int,
		rank_id : int,
		permissions : dict
	) -> None:
		raise NotImplementedError

	async def CreateRankInGuild(
		guild_id : int,
		name : str,
		protected : bool = Body(False, embed=True)
	) -> None:
		raise NotImplementedError

	async def RemoveRankInGuild(
			guild_id : int,
			rank_id : int
		) -> None:
		raise NotImplementedError

	async def SetDefaultRankInGuild(
			guild_id : int,
			rank_id : int
		) -> None:
		raise NotImplementedError

	async def KickUserIdFromGuild(
			guild_id : int,
			target_id : int
		) -> None:
		raise NotImplementedError

	async def DeleteGuild(
			guild_id : int
		) -> None:
		raise NotImplementedError

	async def TransferGuildOwnership(
			guild_id : int,
			target_id : int
		) -> None:
		raise NotImplementedError

	async def GetGuildBannedUserIds(
			guild_id : int
		) -> None:
		raise NotImplementedError

	async def BanUserIdFromGuild(
			guild_id : int,
			target_id : int
		) -> None:
		raise NotImplementedError

	async def UnbanUserIdFromGuild(
			guild_id : int,
			target_id : int
		) -> None:
		raise NotImplementedError

	async def CreateGuildChatMessage(
			guild_id : int,
			user_id : int,
			message : str
		) -> None:
		raise NotImplementedError

	async def RemoveGuildChatMessage(
			guild_id : int,
			message_id : int
		) -> None:
		raise NotImplementedError

	async def GetGuildChatMessages(
		guild_id : int,
		offset : int = Body(0, embed=True),
		limit : int = Body(DEFAULT_GUILD_CHAT_MESSAGE_LIMIT, embed=True)
	) -> None:
		raise NotImplementedError

	async def CreateGuildAuditLog(
		guild_id : int,
		user_id : int,
		action : str,
		args : list = Body(list, embed=True),
	) -> None:
		raise NotImplementedError

	async def GetGuildAuditLogs(
		guild_id : int,
		offset : int = Body(0, embed=True),
		limit : int = Body(DEFAULT_GUILD_AUDIT_LOG_LIMIT, embed=True)
	) -> None:
		raise NotImplementedError

async def test() -> None:

	await InternalGuildsAPI.initialize()

	data = await InternalGuildsAPI.GetGuildInfoFromUserId(123123123)
	print(data)

	data = await InternalGuildsAPI.CreateGuild(123123123, 'test guild', 'hello world!', 1)
	print(data)

	data = await InternalGuildsAPI.GetFullGuildInfoFromUserId(123123123)
	print(data)

if __name__ == '__main__':
	asyncio.run(test())
