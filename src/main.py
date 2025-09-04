import asyncio

import uvicorn

from src.client import example


async def run_server():
    config = uvicorn.Config("src.server.app:app", host="127.0.0.1", port=8000, reload=True)
    server = uvicorn.Server(config)
    await server.serve()

async def main():
    await asyncio.gather(run_server(), example.login_user())


if __name__ == "__main__":
    asyncio.run(main())