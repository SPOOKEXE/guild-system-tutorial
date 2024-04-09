
from __future__ import annotations
from typing import Any, Union, Dict
from databases import Database
from pydantic import BaseModel

import traceback
import asyncio

class BaseDatabase(Database):

	async def start( self : BaseDatabase ) -> None:
		print(f'Connecting to SQLite Database: {self.filename}')
		await self.connect()

	def __init__( self, filename : str, *args, **kwargs ) -> BaseDatabase:
		super().__init__( "sqlite+aiosqlite:///" + filename, *args, **kwargs)

class DatabaseAPI:

	async def get_databases() -> list:
		raise NotImplementedError

	async def register_database( name : str, constructors : list ) -> None:
		raise NotImplementedError

	async def does_database_exist( name : str ) -> bool:
		raise NotImplementedError

	async def execute_one( name : str, query : str, data : Union[dict, None] ) -> None:
		raise NotImplementedError

	async def execute_many( name : str, query : str, data : Union[dict, None] ) -> None:
		raise NotImplementedError

	async def fetch_one( name : str, query : str, data : Union[dict, None] ) -> None:
		raise NotImplementedError

	async def fetch_all( name : str, query : str, data : Union[dict, None] ) -> None:
		raise NotImplementedError
