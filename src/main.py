import asyncio

import uvicorn

from client.client import Client
from config import cfg


async def run_server():
    config = uvicorn.Config("src.server.app:app", host="127.0.0.1", port=8000, reload=True)
    server = uvicorn.Server(config)
    await server.serve()

async def run_client():
    username = input("Enter username to create: ")
    client = Client()
    await client.create_user(cfg.BASE_URL, username)

async def main():
    await asyncio.gather(run_server(), run_client())


if __name__ == "__main__":
    asyncio.run(main())