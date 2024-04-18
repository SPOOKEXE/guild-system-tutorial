
from __future__ import annotations
from typing import Any, Union
from pydantic import BaseModel
from database import DatabaseAPI

import asyncio
import time
import json

DEFAULT_GUILD_CHAT_MESSAGE_LIMIT : int = 50
DEFAULT_GUILD_AUDIT_LOG_LIMIT : int = 50
DEFAULT_GUILD_GET_ALL_LIMIT : int = 25

def get_time() -> int:
	return int(round(time.time()))

class InternalGuildsAPI:

	DATABASE_NAME : str = 'guilds'
	OUTPUT_DELETED_TO_FILE : bool = False

	async def initialize( ) -> None:
		constructors = [
			"CREATE TABLE IF NOT EXISTS master (guild_id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT NOT NULL, description TEXT NOT NULL, accessibility INTEGER DEFAULT 0, emblem INTEGER NOT NULL, owner_id INTEGER NOT NULL, owner_rank_id INTEGER DEFAULT -1, default_rank_id INTEGER DEFAULT -1, total_members INTEGER DEFAULT 1, total_online INTEGER DEFAULT 0, creation INTEGER NOT NULL);",
			"CREATE TABLE IF NOT EXISTS members (user_id INTEGER PRIMARY KEY UNIQUE, guild_id INTEGER NOT NULL, rank_id INTEGER DEFAULT -1, timestamp INTEGER NOT NULL);",
			"CREATE TABLE IF NOT EXISTS ranks (rank_id INTEGER PRIMARY KEY AUTOINCREMENT, guild_id INTEGER NOT NULL, name TEXT NOT NULL, protected INTEGER NOT NULL, permissions TEXT NOT NULL);",
			"CREATE TABLE IF NOT EXISTS banned (id INTEGER PRIMARY KEY AUTOINCREMENT, guild_id INTEGER, banned_json TEXT)",
			"CREATE TABLE IF NOT EXISTS guild_chat (id INTEGER PRIMARY KEY AUTOINCREMENT, guild_id INTEGER, user_id INTEGER, message TEXT, timestamp INTEGER, deleted INTEGER)",
			"CREATE TABLE IF NOT EXISTS audit_logs (id INTEGER PRIMARY KEY AUTOINCREMENT, guild_id INTEGER, user_id INTEGER, rank_id INTEGER, timestamp INTEGER, action INTEGER, args TEXT)"
		]
		await DatabaseAPI.register_database(InternalGuildsAPI.DATABASE_NAME, constructors)

	async def IsRankPermissionsValid(
		permissions : dict
	) -> bool:
		if isinstance(permissions, dict) is False: return False
		return True # TODO

	async def IsGuildNameAvailable(
		name : str
	) -> bool:
		query = 'SELECT guild_id FROM master WHERE name=:name COLLATE NOCASE'
		data = {'name' : name}
		value = await DatabaseAPI.fetch_one(InternalGuildsAPI.DATABASE_NAME, query, data)
		return value is None

	async def GetGuildInfoFromGuildId(
		guild_id : int
	) -> Union[dict, None]:
		query = 'SELECT * FROM master WHERE guild_id=:guild_id'
		data = {'guild_id' : guild_id}
		return await DatabaseAPI.fetch_one(InternalGuildsAPI.DATABASE_NAME, query, data)

	async def GetGuildInfoFromUserId(
		user_id : int
	) -> Union[dict, None]:
		query = 'SELECT guild_id FROM members WHERE user_id=:user_id'
		data = {'user_id' : user_id}
		value = await DatabaseAPI.fetch_one(InternalGuildsAPI.DATABASE_NAME, query, data)
		if value is None: return None
		gid : int = value['guild_id']
		return await InternalGuildsAPI.GetGuildInfoFromGuildId(gid)

	async def GetGuildMembers(
		guild_id : int
	) -> Union[list[dict], None]:
		query = 'SELECT * FROM members WHERE guild_id=:guild_id'
		data = {'guild_id' : guild_id}
		return await DatabaseAPI.fetch_all(InternalGuildsAPI.DATABASE_NAME, query, data)

	async def GetGuildRanks(
		guild_id : int
	) -> Union[list[dict], None]:
		query = 'SELECT rank_id, name, permissions FROM ranks WHERE guild_id=:guild_id'
		data = {'guild_id' : guild_id}
		return await DatabaseAPI.fetch_all(InternalGuildsAPI.DATABASE_NAME, query, data)

	async def GetFullGuildInfoFromGuildId(
		guild_id : int
	) -> Union[dict, None]:
		data = await InternalGuildsAPI.GetGuildInfoFromGuildId(guild_id)
		if data is None: return None
		data['ranks'] = await InternalGuildsAPI.GetGuildRanks( guild_id )
		data['members'] = await InternalGuildsAPI.GetGuildMembers( guild_id )
		data['banned'] = await InternalGuildsAPI.GetGuildBannedUserIds( guild_id )
		return data

	async def GetFullGuildInfoFromUserId(
		user_id : int
	) -> Union[dict, None]:
		query = 'SELECT guild_id FROM members WHERE user_id=:user_id'
		data = {'user_id' : user_id}
		value = await DatabaseAPI.fetch_one(InternalGuildsAPI.DATABASE_NAME, query, data)
		if value is None: return None
		return await InternalGuildsAPI.GetFullGuildInfoFromGuildId( value['guild_id'] )

	async def UpdateGuildDisplayInfo(
		guild_id : int,
		description : str,
		accessibility : int,
		emblem : int
	) -> Union[dict, None]:
		raise NotImplementedError

	async def ChangeUserIdRankInGuild(
		guild_id : int,
		target_id : int,
		rank_id : int
	) -> bool:
		raise NotImplementedError

	async def ChangeRankPermissionsInGuild(
		guild_id : int,
		rank_id : int,
		permissions : dict
	) -> bool:
		raise NotImplementedError

	async def CreateRankInGuild(
		guild_id : int,
		name : str,
		protected : bool = False
	) -> Union[dict, None]:
		query : str = 'INSERT INTO ranks (guild_id, name, protected, permissions) VALUES (:guild_id, :name, :protected, :permissions) RETURNING *;'
		data = {'guild_id' : guild_id, 'name' : name, 'permissions' : "{}", 'protected' : int(protected)}
		return await DatabaseAPI.execute_and_return(InternalGuildsAPI.DATABASE_NAME, query, data)

	async def RemoveRankInGuild(
		guild_id : int,
		rank_id : int
	) -> bool:
		raise NotImplementedError

	async def SetDefaultRankInGuild(
		guild_id : int,
		rank_id : int
	) -> bool:
		raise NotImplementedError

	async def KickUserIdFromGuild(
		guild_id : int,
		target_id : int
	) -> bool:
		raise NotImplementedError

	async def DeleteGuild(
		guild_id : int
	) -> bool:

		if InternalGuildsAPI.OUTPUT_DELETED_TO_FILE is True:
			backup = await InternalGuildsAPI.GetFullGuildInfoFromGuildId(guild_id)
			if backup is None:
				return True
			with open(f'{guild_id}_backup.json', 'w') as file:
				file.write(json.dumps(backup, indent=4))

		queries = [
			'DELETE FROM master WHERE guild_id=:guild_id',
			'DELETE FROM members WHERE guild_id=:guild_id',
			'DELETE FROM ranks WHERE guild_id=:guild_id',
			'DELETE FROM banned WHERE guild_id=:guild_id',
			'DELETE FROM guild_chat WHERE guild_id=:guild_id',
			'DELETE FROM audit_logs WHERE guild_id=:guild_id',
		]
		data = {'guild_id' : guild_id}
		for query in queries:
			await DatabaseAPI.execute_one( InternalGuildsAPI.DATABASE_NAME, query, data )
		return True

	async def TransferGuildOwnership(
		guild_id : int,
		target_id : int
	) -> bool:
		raise NotImplementedError

	async def GetGuildBannedUserIds(
		guild_id : int
	) -> Union[list, None]:
		query = 'SELECT banned_json FROM banned WHERE guild_id=:guild_id'
		data = {'guild_id' : guild_id}
		value = await DatabaseAPI.fetch_one( InternalGuildsAPI.DATABASE_NAME, query, data )
		try:
			return json.dumps(value) if value is not None else []
		except:
			return []

	async def BanUserIdFromGuild(
		guild_id : int,
		target_id : int
	) -> bool:
		query = 'SELECT banned_json FROM banned WHERE guild_id=:guild_id'
		data = {'guild_id' : guild_id}
		value = await DatabaseAPI.fetch_one( InternalGuildsAPI.DATABASE_NAME, query, data )
		if value is not None:
			try:
				values = json.loads(value)
			except:
				values = []
			if target_id in values:
				return True # already banned
			values.append(target_id)
		else:
			values = [target_id]
		query : str = 'UPDATE banned SET banned_json=:banned_json WHERE guild_id=:guild_id'
		data = {'guild_id' : guild_id, 'banned_json' : json.dumps(values)}
		await DatabaseAPI.execute_one( InternalGuildsAPI.DATABASE_NAME, query, data )
		return True

	async def UnbanUserIdFromGuild(
		guild_id : int,
		target_id : int
	) -> bool:
		raise NotImplementedError

	async def CreateGuildChatMessage(
		guild_id : int,
		user_id : int,
		message : str
	) -> bool:
		raise NotImplementedError

	async def RemoveGuildChatMessage(
		guild_id : int,
		message_id : int
	) -> bool:
		raise NotImplementedError

	async def GetGuildChatMessages(
		guild_id : int,
		offset : int = 0,
		limit : int = DEFAULT_GUILD_CHAT_MESSAGE_LIMIT
	) -> Union[list[dict], None]:
		raise NotImplementedError

	async def CreateGuildAuditLog(
		guild_id : int,
		user_id : int,
		action : str,
		args : list = list(),
	) -> bool:
		raise NotImplementedError

	async def GetGuildAuditLogs(
		guild_id : int,
		offset : int = 0,
		limit : int = DEFAULT_GUILD_AUDIT_LOG_LIMIT
	) -> Union[list[dict], None]:
		raise NotImplementedError

	async def GetCreatedGuilds(offset : int = 0, limit : int = DEFAULT_GUILD_GET_ALL_LIMIT) -> list[dict]:
		query = f'SELECT * FROM master LIMIT {limit} OFFSET {offset}'
		return await DatabaseAPI.fetch_all(InternalGuildsAPI.DATABASE_NAME, query, None)

	async def GetCreatedGuildsFull(offset : int = 0, limit : int = DEFAULT_GUILD_GET_ALL_LIMIT) -> list[dict]:
		query = f'SELECT guild_id FROM master LIMIT {limit} OFFSET {offset} '
		values = await DatabaseAPI.fetch_all(InternalGuildsAPI.DATABASE_NAME, query, None)
		if values is None: return []
		return [ await InternalGuildsAPI.GetFullGuildInfoFromGuildId( value['guild_id'] ) for value in values if value is not None ]

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
		query = 'INSERT INTO master (name, description, emblem, owner_id, creation) VALUES (:name, :description, :emblem, :owner_id, :creation) RETURNING *;'
		guild_data = await DatabaseAPI.execute_and_return(InternalGuildsAPI.DATABASE_NAME, query, {
			'name' : name,
			'description' : description,
			'emblem' : emblem,
			'owner_id' : user_id,
			'creation' : get_time()
		})

		if guild_data is None: return None

		# insert default ranks and get their ids
		owner_rank : dict = await InternalGuildsAPI.CreateRankInGuild( guild_data['guild_id'], 'Owner', protected=True )
		member_rank : dict = await InternalGuildsAPI.CreateRankInGuild( guild_data['guild_id'], 'Member', protected=True )

		# insert to members
		query : str = 'INSERT INTO members (guild_id, user_id, rank_id, timestamp) VALUES (:guild_id, :user_id, :rank_id, :timestamp) RETURNING *;'
		await DatabaseAPI.execute_one(InternalGuildsAPI.DATABASE_NAME, query, {
			'guild_id' : guild_data['guild_id'],
			'user_id' : user_id,
			'rank_id' : owner_rank['rank_id'],
			'timestamp' : get_time()
		})

		# update guild info
		query : str = 'UPDATE master SET default_rank_id=:default_rank_id, owner_rank_id=:owner_rank_id WHERE guild_id=:guild_id'
		await DatabaseAPI.execute_one(InternalGuildsAPI.DATABASE_NAME, query, { 'guild_id' : guild_data['guild_id'], 'default_rank_id' : member_rank['rank_id'], 'owner_rank_id' : owner_rank['rank_id'] })

		# return all information
		return await InternalGuildsAPI.GetFullGuildInfoFromGuildId( guild_data['guild_id'] )

async def test() -> None:

	await InternalGuildsAPI.initialize()

	# data = await InternalGuildsAPI.GetFullGuildInfoFromUserId(123123123)
	# print(data)

	# data = await InternalGuildsAPI.CreateGuild(123123123, 'test guild', 'hello world!', 1)
	# print(data)

	# data = await InternalGuildsAPI.GetFullGuildInfoFromUserId(123123123)
	# print(data)

	# get all guilds and output
	print( await InternalGuildsAPI.GetCreatedGuildsFull(offset=0, limit=9999) )

	# get all guilds and delete them all
	# items = await InternalGuildsAPI.GetCreatedGuildsFull(offset=0, limit=9999)
	# for guild in items:
	# 	await InternalGuildsAPI.DeleteGuild( guild['guild_id'] )

	pass

if __name__ == '__main__':
	asyncio.run(test())
