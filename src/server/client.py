import aiohttp

from json import JSONDecodeError

from src.server.models import Response, Ok, Error
from logger import logger
from config import cfg


class Client:
    headers: dict
    session: aiohttp.ClientSession | None

    def __init__(self):
        self.session = None
        self.headers = cfg.headers.copy()

    async def __aenter__(self):
        self.session = aiohttp.ClientSession()
        return self

    async def __aexit__(self, exc_type, exc, tb):
        if self.session:
            await self.session.close()


    async def create_user(self, user: dict):
        return await self.post("api/users/register", json=user)

    async def login(self, email, password):
        data = {
            "email": email,
            "password": password
        }
        resp = await self.post("api/users/login", json=data)
        if resp.success:
            self.headers["Authorization"] = f"Bearer {resp.data["access_token"]}"
            return resp
        else:
            return resp.data

    async def logout(self):
        return await self.get(f"api/users/logout")

    async def current_user(self):
        return await self.get("api/users/me")

    async def change_role(self, user, role):
        data = {
            "user_id": user["user_id"],
            "role": role
        }
        return await self.post("api/admin/change-role", json=data)

    async def remove_user(self):
        return await self.delete(f"api/users/")

    async def unblock_user(self, user_id):
        return await self.update(f"api/admin/unblock/{user_id}")

    async def edit_user(self, new_name, new_last_name):
        data = {
            "name": new_name,
            "last_name": new_last_name
        }
        return await self.post(f"api/users/edit", json=data)


    async def get(self, path: str, **kwargs):
        return await self._request("GET", path, **kwargs)

    async def post(self, path: str, **kwargs):
        return await self._request("POST", path, **kwargs)

    async def delete(self, path: str, **kwargs):
        return await self._request("DELETE", path, **kwargs)

    async def update(self, path: str, **kwargs):
        return await self._request("PUT", path, **kwargs)

    async def _request(self, method: str, path: str, **kwargs):
        kwargs = dict(
            method=method,
            url=f"{cfg.base_url}/{path}",
            headers=self.headers,
            **kwargs
        )
        try:
            async with self.session.request(**kwargs) as response:
                try:
                    data = await response.json()
                    try:
                        resp = Response(**data)
                        return resp
                    except ValueError:
                        if response.status < 300:
                            return Ok(data=data)
                        else:
                            return Error(error=data)

                except JSONDecodeError:
                    error = await response.text()
                    logger.error(f"Can not parse response: {error}")
                    return Error(error=error)

        except Exception as e:
            return {"success": False, "error": f"[{method}] {path} -> {e}"}
