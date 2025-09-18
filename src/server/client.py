import aiohttp

from json import JSONDecodeError

from config import cfg


class Client:
    headers: dict

    def __init__(self):
        self.session = aiohttp.ClientSession()
        self.headers = cfg.headers.copy()
        self.close = self.session.close

    async def create_user(self, user: dict):
        return await self.post("api/users/register", json=user)

    async def login(self, email, password):
        data = {
            "email": email,
            "password": password
        }
        resp = await self.post("api/users/login", json=data)
        if resp["success"]:
            self.headers["Authorization"] = f"Bearer {resp["data"]["access_token"]}"
            return resp
        else:
            return resp

    async def logout(self):
        return await self.get(f"api/users/logout")

    async def get_user(self, resp):
        data = {
            "access_token": resp["data"]["access_token"],
            "token_type": resp["data"]["token_type"]
        }
        return await self.post("api/users/me", json=data)

    async def change_role(self, user, role):
        data = {
            "user_id": user.get("id"),
            "role": role
        }
        return await self.post("api/admin/change-role", json=data)

    async def remove_user(self):
        return await self.delete(f"api/users/")

    async def unblock_user(self, user_id):
        return await self.update(f"api/admin/unblock/{user_id}")


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

        except Exception as e:
            print(f"[{method}] {path} -> {e}")
