import asyncio

import uvicorn

from client.client import Client


async def run_server():
    config = uvicorn.Config("src.server.app:app", host="127.0.0.1", port=8000, reload=True)
    server = uvicorn.Server(config)
    await server.serve()

async def register_user():
    client = Client()
    first_name = input("Enter first name: ")
    last_name = input("Enter last name: ")
    email = input("Enter email: ")
    password = input("Enter password: ")
    await client.create(first_name, last_name, email, password)

async def login_user():
    client = Client()
    email = input("Enter email: ")
    password = input("Enter password: ")
    await client.auth(email, password)

async def main():
    await asyncio.gather(run_server(), login_user())


if __name__ == "__main__":
    asyncio.run(main())