
from __future__ import annotations
from typing import Any, Union
from fastapi import FastAPI, Body, Header
from databases import Database
from pydantic import BaseModel

import traceback
import uvicorn
import asyncio

guilds_api = FastAPI(title="Guilds API", description="Tutorial Series Guilds API", version="0.0.1")

async def host_fastapp( app : FastAPI, host : str, port : int ) -> None:
	print(f"Hosting App: {app.title}")
	await uvicorn.Server(uvicorn.Config(app, host=host, port=port, log_level='debug')).serve()

async def main( host : str = '0.0.0.0', port : int = 5100 ) -> None:
	await host_fastapp(guilds_api, host, port)

if __name__ == '__main__':
	asyncio.run(main(host='127.0.0.1', port=5100))
