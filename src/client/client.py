import aiohttp

from json import JSONDecodeError

from config import cfg


class Client:
    headers: dict
    access_token: str | None = None

    def __init__(self):
        self.session = aiohttp.ClientSession()

    async def create(self, name, last_name, email, password):
        data = {
            "name": name,
            "last_name": last_name,
            "email": email,
            "password": password
        }
        await self.post("register", json=data)

    async def login(self, email, password):
        data = {
            "email": email,
            "password": password
        }
        await self.post("login", json=data)

    async def session(self):
        await self.get("protected")


    async def get(self, path: str, **kwargs):
        return await self.request("GET", path, **kwargs)

    async def post(self, path: str, **kwargs):
        return await self.request("POST", path, **kwargs)

    async def request(self, method: str, path: str, **kwargs):
        kwargs = dict(
            method=method,
            url=f"{cfg.BASE_URL}/{path}",
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