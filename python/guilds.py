
from __future__ import annotations
import time
from typing import Any, Union
from fastapi import Body
from pydantic import BaseModel
from database import DatabaseAPI

import asyncio

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

	async def IsRankPermissionsValid( permissions : dict ) -> bool:
		raise NotImplementedError

	async def IsGuildNameAvailable( name : str ) -> bool:
		query = 'SELECT guild_id FROM master WHERE name=:name COLLATE NOCASE'
		value : Union[dict, None] = await DatabaseAPI.fetch_one(InternalGuildsAPI.DATABASE_NAME, query, {'name' : name})
		return value is None

	async def GetGuildInfoFromGuildId( guild_id : int ) -> Union[dict, None]:
		query = 'SELECT * FROM master WHERE guild_id=:guild_id'
		return await DatabaseAPI.fetch_one(InternalGuildsAPI.DATABASE_NAME, query, {'guild_id' : guild_id})

	async def GetGuildInfoFromUserId( user_id : int ) -> Union[dict, None]:
		query = 'SELECT guild_id FROM members WHERE user_id=:user_id'
		value : Union[dict, None] = await DatabaseAPI.fetch_one(InternalGuildsAPI.DATABASE_NAME, query, {'user_id' : user_id})
		if value is None: return None
		return await InternalGuildsAPI.GetGuildInfoFromGuildId( value['guild_id'] )

	async def GetGuildMembers( guild_id : int ) -> Union[list[dict], None]:
		query = 'SELECT * FROM members WHERE guild_id=:guild_id'
		return await DatabaseAPI.fetch_all(InternalGuildsAPI.DATABASE_NAME, query, {'guild_id' : guild_id})

	async def GetFullGuildInfoFromGuildId( guild_id : int ) -> Union[dict, None]:
		data = await InternalGuildsAPI.GetGuildInfoFromGuildId(guild_id)
		if data is None: return None
		data['members'] = await InternalGuildsAPI.GetGuildMembers( guild_id )
		# data['banned'] = await InternalGuildsAPI.GetGuildBannedUserIds( guild_id, user_id )
		return data

	async def GetFullGuildInfoFromUserId( user_id : int ) -> Union[dict, None]:
		query = 'SELECT guild_id FROM members WHERE user_id=:user_id'
		value : Union[dict, None] = await DatabaseAPI.fetch_one(InternalGuildsAPI.DATABASE_NAME, query, {'user_id' : user_id})
		if value is None: return None
		return await InternalGuildsAPI.GetFullGuildInfoFromGuildId( value['guild_id'] )

	async def UpdateGuildDisplayInfo(
		guild_id : int,
		user_id : int,
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

		info = await InternalGuildsAPI.GetGuildInfoFromUserId(user_id)
		if info is not None: return None

		is_name_available : bool = await InternalGuildsAPI.IsGuildNameAvailable(name)
		if is_name_available is False: return None

		# insert to master and get the data
		query : str = 'INSERT INTO master (name, description, emblem, owner_id, creation) VALUES (:name, :description, :emblem, :owner_id, :creation);'
		await DatabaseAPI.execute_one(InternalGuildsAPI.DATABASE_NAME, query, {
			'name' : name, 'description' : description, 'emblem' : emblem, 'owner_id' : user_id, 'creation' : get_time()
		})

		query : str = 'SELECT * FROM master DESC LIMIT 1'
		guild_data : Union[dict, None] = await DatabaseAPI.fetch_one(InternalGuildsAPI.DATABASE_NAME, query, None)
		if guild_data is None: return None

		# insert default ranks and get their ids
		query : str = 'INSERT INTO ranks (guild_id, name, permissions) VALUES (:guild_id, :name, :permissions);'
		await DatabaseAPI.execute_one(InternalGuildsAPI.DATABASE_NAME, query, {'guild_id' : guild_data['guild_id'], 'name' : 'Owner', 'permissions' : '{}'})
		await DatabaseAPI.execute_one(InternalGuildsAPI.DATABASE_NAME, query, {'guild_id' : guild_data['guild_id'], 'name' : 'Member', 'permissions' : '{}'})

		query : str = 'SELECT rank_id FROM ranks WHERE guild_id=:guild_id '
		rank_ids : Union[list[dict], None] = await DatabaseAPI.fetch_all(InternalGuildsAPI.DATABASE_NAME, query, {'guild_id' : guild_data['guild_id']})
		rank_ids : list[int] = [ item['rank_id'] for item in rank_ids ]
		owner_rank_id : int = rank_ids[0]
		member_rank_id : int = rank_ids[1]

		# insert to members
		query : str = 'INSERT INTO members (guild_id, user_id, rank_id, timestamp) VALUES (:guild_id, :user_id, :rank_id, :timestamp);'
		await DatabaseAPI.execute_one(InternalGuildsAPI.DATABASE_NAME, query, {
			'guild_id' : guild_data['guild_id'], 'user_id' : user_id, 'rank_id' : owner_rank_id, 'timestamp' : get_time()
		})

		# update guild info
		query : str = 'UPDATE master SET default_rank_id=:default_rank_id WHERE guild_id=:guild_id'
		await DatabaseAPI.execute_one(InternalGuildsAPI.DATABASE_NAME, query, { 'guild_id' : guild_data['guild_id'], 'default_rank_id' : member_rank_id })

		# return all information
		return await InternalGuildsAPI.GetFullGuildInfoFromGuildId( guild_data['guild_id'] )

	async def ChangeUserIdRankInGuild(
		guild_id : int,
		user_id : int,
		target_id : int,
		rank_id : int
	) -> None:
		raise NotImplementedError

	async def ChangeRankPermissionsInGuild(
		guild_id : int,
		user_id : int,
		rank_id : int,
		permissions : dict
	) -> None:
		raise NotImplementedError

	async def CreateRankInGuild(
		guild_id : int,
		user_id : int,
		name : str,
		protected : bool = Body(False, embed=True)
	) -> None:
		# TODO: add 'protected' ranks that cannot be deleted (DefaultRank & Owner Rank)
		raise NotImplementedError

	async def RemoveRankInGuild( guild_id : int, user_id : int, rank_id : int ) -> None:
		raise NotImplementedError

	async def SetDefaultRankInGuild( guild_id : int, user_id : int, rank_id : int ) -> None:
		raise NotImplementedError

	async def KickUserIdFromGuild( guild_id : int, user_id : int, target_id : int ) -> None:
		raise NotImplementedError

	async def DeleteGuild( guild_id : int, user_id : int ) -> None:
		raise NotImplementedError

	async def TransferGuildOwnership( guild_id : int, user_id : int, target_id : int ) -> None:
		raise NotImplementedError

	async def GetGuildBannedUserIds( guild_id : int, user_id : int ) -> None:
		raise NotImplementedError

	async def BanUserIdFromGuild( guild_id : int, user_id : int, target_id : int ) -> None:
		raise NotImplementedError

	async def UnbanUserIdFromGuild( guild_id : int, user_id : int, target_id : int ) -> None:
		raise NotImplementedError

	async def CreateGuildChatMessage( guild_id : int, user_id : int, message : str ) -> None:
		raise NotImplementedError

	async def RemoveGuildChatMessage( guild_id : int, user_id : int, message_id : int ) -> None:
		raise NotImplementedError

	async def GetGuildChatMessages(
		guild_id : int,
		user_id : int,
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
		user_id : int,
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
