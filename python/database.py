
from __future__ import annotations
import time
from typing import Union
from databases import Database
from pydantic import BaseModel

import traceback
import os
import asyncio

FILE_DIRECTORY = os.path.dirname(os.path.realpath(__file__))

class BaseDatabase(Database):

	async def execute_constructors( self : BaseDatabase, constructors : list[str] ) -> None:
		for constructor in constructors:
			await self.execute(constructor)

	async def start( self : BaseDatabase ) -> None:
		print(f'Connecting to SQLite Database: {self.filename}')
		await self.connect()

	def __init__( self, filename : str, *args, **kwargs ) -> BaseDatabase:
		self.filename = filename
		super().__init__( "sqlite+aiosqlite:///" + filename, *args, **kwargs)

class DatabaseAPI:

	DATABASES_DIRECTORY = os.path.join(FILE_DIRECTORY, 'databases')

	_cache : dict[str, BaseDatabase] = {}
	async def get_database( name : str ) -> Union[BaseDatabase, None]:
		if DatabaseAPI._cache.get(name) is not None:
			return DatabaseAPI._cache[name]

		filepath : str = os.path.join( DatabaseAPI.DATABASES_DIRECTORY, name + '.db' )
		if os.path.exists(filepath) is False: return None

		db = BaseDatabase(filepath)
		DatabaseAPI._cache[name] = db
		return db

	async def get_databases() -> list[str]:
		os.makedirs(DatabaseAPI.DATABASES_DIRECTORY, exist_ok=True)
		return [ os.path.splitext(item)[0] for item in os.listdir(DatabaseAPI.DATABASES_DIRECTORY) ]

	async def register_database( name : str, constructors : Union[list[str], None] ) -> None:
		os.makedirs(DatabaseAPI.DATABASES_DIRECTORY, exist_ok=True)
		database : bool = await DatabaseAPI.get_database(name)
		if database is not None:
			return
		filepath : str = os.path.join( DatabaseAPI.DATABASES_DIRECTORY, name + '.db' )
		database = BaseDatabase(filepath)
		await database.start()
		if constructors is not None:
			await database.execute_constructors(constructors)

	async def execute_one( name : str, query : str, data : Union[dict, None] ) -> bool:
		database : BaseDatabase = await DatabaseAPI.get_database(name)
		if database is None: return False
		await database.execute(query, data)
		return True

	async def execute_many( name : str, query : str, values : Union[list[dict], None] ) -> bool:
		database : BaseDatabase = await DatabaseAPI.get_database(name)
		if database is None: return False
		await database.execute_many(query, values)
		return True

	async def fetch_one( name : str, query : str, data : Union[dict, None] ) -> Union[dict, None]:
		database : BaseDatabase = await DatabaseAPI.get_database(name)
		if database is None: return None
		record = await database.fetch_one(query, data)
		if record is None: return None
		return dict(record)

	async def fetch_all( name : str, query : str, values : Union[list[dict], None] ) -> Union[list, None]:
		database : BaseDatabase = await DatabaseAPI.get_database(name)
		if database is None: return None
		records = await database.fetch_all(query, values)
		records = [ dict(record) for record in records if record is not None ]
		return None if len(records) == 0 else records

async def test() -> None:
	pass

if __name__ == '__main__':
	asyncio.run(test())
