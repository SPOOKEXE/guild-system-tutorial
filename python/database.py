
from __future__ import annotations
from typing import Any, Union, Dict
from fastapi import Body, FastAPI, Header
from databases import Database
from pydantic import BaseModel

import traceback
import uvicorn
import asyncio

class BaseDatabase(Database):

	async def start( self : Database ) -> None:
		print(f'Connecting to SQLITE Database: {self.filename}')
		await self.connect()

	def __init__( self, filename : str, *args, **kwargs ) -> BaseDatabase:
		super().__init__( "sqlite+aiosqlite:///" + filename, *args, **kwargs)
