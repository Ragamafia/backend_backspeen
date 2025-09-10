import aiohttp

from json import JSONDecodeError

from config import cfg


class Client:
    headers: dict

    def __init__(self):
        self.session = aiohttp.ClientSession()
        self.headers = cfg.headers

    async def create(self, name, last_name, email, password):
        data = {
            "name": name,
            "last_name": last_name,
            "email": email,
            "password": password
        }
        await self.post("api/users/register", json=data)

    async def login(self, email, password):
        data = {
            "email": email,
            "password": password
        }
        resp = await self.post("api/users/login", json=data)
        if token := resp["access_token"]:
            self.access_token = token
            self.headers["Authorization"] = f"Bearer {token}"
            return resp

    async def get_user(self, data):
        return await self.post("api/users/me", json=data)


    async def get(self, path: str, **kwargs):
        return await self._request("GET", path, **kwargs)

    async def post(self, path: str, **kwargs):
        return await self._request("POST", path, **kwargs)

    async def _request(self, method: str, path: str, **kwargs):
        kwargs = dict(
            method=method,
            url=f"{cfg.BASE_URL}/{path}",
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
