
from __future__ import annotations
from typing import Any, Union
from fastapi import Body
from databases import Database
from pydantic import BaseModel

import asyncio

DEFAULT_GUILD_CHAT_MESSAGE_LIMIT : int = 50
DEFAULT_GUILD_AUDIT_LOG_LIMIT : int = 50

class InternalGuildsAPI:

	async def IsRankPermissionsValid( permissions : dict ) -> bool:
		raise NotImplementedError

	async def IsGuildNameAvailable( name : str ) -> bool:
		raise NotImplementedError

	async def GetGuildInfoFromGuildId( guild_id : int ) -> dict | None:
		raise NotImplementedError

	async def GetGuildInfoFromUserId( user_id : int ) -> dict | None:
		raise NotImplementedError

	async def UpdateGuildDisplayInfo(
		guild_id : int,
		user_id : int,
		description : str,
		accessibility : int,
		emblem : int
	) -> dict | None:
		raise NotImplementedError

	async def CreateGuild(
		user_id : int,
		name : str,
		description : str,
		emblem : int
	) -> None:
		raise NotImplementedError

	async def GetGuildInvites( user_id : int, ) -> None:
		raise NotImplementedError

	async def InviteUserIdToGuild( user_id : int, target_id : int, ) -> None:
		raise NotImplementedError

	async def AcceptGuildInvite( user_id : int, invite_id : int, ) -> None:
		raise NotImplementedError

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

	async def IgnoreGuildInvite( user_id : int, invite_id : str ) -> None:
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
	data = InternalGuildsAPI.CreateGuild()
	print(data['id'])

if __name__ == '__main__':
	asyncio.run(test())
