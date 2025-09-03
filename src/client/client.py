import aiohttp
from json import JSONDecodeError


class Client:
    def __init__(self):
        self.session = aiohttp.ClientSession()
        self.headers = {
            "Content-Type": "application/json",
        }

    async def create_user(self, url, username: str):
        data = {
            "username": username
        }
        await self.request("POST", url, json=data)

    async def get(self, path: str, **kwargs):
        return await self.request("GET", path, **kwargs)

    async def post(self, path: str, **kwargs):
        return await self.request("POST", path, **kwargs)

    async def request(self, method: str, path: str, **kwargs):
        kwargs = dict(
            method=method,
            url=path,
            headers=self.headers,
            **kwargs
        )
        try:
            async with self.session.request(**kwargs) as response:
                if response.status < 300:
                    try:
                        data = await response.json()
                    except JSONDecodeError:
                        data = await response.text()
                    return data

                elif response.status == 401:
                    return "Unauthorized"

                elif response.status >= 400:
                    return "No access"
        finally:
            await self.session.close()