import asyncio
from typing import Callable

from pydantic import BaseModel

from src.server.client import Client
from logger import logger
from config import cfg


ADMIN_CREDS = {
    "email": cfg.admin_email,
    "password": cfg.admin_password,
}
USER_CREDS = {
    "email": "user@user.com",
    "password": "123456",
}
USER = {
    "name": "Iwan",
    "last_name": "Ragamafia",
    **USER_CREDS,
}


class Response(BaseModel):
    success: bool
    data: dict | None
    error: str | None


async def handle_request(coro: Callable, failed: str, *args, **kwargs):
    try:
        resp: Response = await coro(*args, **kwargs)
        if resp.success:
            return resp.data
        else:
            raise AssertionError(f"{failed} failed: {resp.error}")
    except Exception as e:
        raise AssertionError(f"{failed} failed: Can not handle request '{e}'")

async def handle_unauthorized(coro: Callable, failed: str, *args, **kwargs):
    try:
        resp: Response = await coro(*args, **kwargs)
        if not resp.success:
            return resp.error
        else:
            raise AssertionError(f"{failed} failed: {resp.error}")
    except Exception as e:
        raise AssertionError(f"{failed} failed: Can not handle request '{e}'")


async def main():
    async with Client() as user, Client() as admin:
        # step 1: create user
        new_user = await handle_request(user.create_user, "Create user", USER)
        logger.success(f"User created: {new_user}")

        # step 2: login user
        await handle_request(user.login, "User login", **USER_CREDS)
        logger.success(f"New user authenticated successfully")

        # step 3: get user from database
        current = await handle_request(user.current_user, "Get current user")
        logger.success(f"Current user: {current}")

        # step 4: login admin
        await handle_request(admin.login, "Admin login", **ADMIN_CREDS)
        logger.success(f"Admin authenticated successfully")

        # step 5: update user role
        role = "moderator"
        await handle_request(admin.change_role, "Change role", current, role=role)
        logger.success(f"User {current['name']} {current['last_name']} updated. New role: {role}")

        # step 6: logout user
        await handle_request(user.logout, "Logout user")
        logger.success(f"User {current['name']} {current['last_name']} logged out")

        # step 7: try getting info as a logged out user
        await handle_unauthorized(user.current_user, "Get current user")
        logger.success(f"Unauthorized")

        # step 8: login user again
        await handle_request(user.login, "User login", **USER_CREDS)
        logger.success(f"User authenticated successfully")

        # step 9: remove user
        await handle_request(user.remove_user, "Remove user")
        logger.success(f"User deleted")

        # step 10: try deleted user login
        await handle_unauthorized(user.login, "User login", **USER_CREDS)
        logger.success(f"Unauthorized")

        # step 10: unblock user
        await handle_request(admin.unblock_user, "Unblock user", current["user_id"])
        logger.success(f"User unblocked")

        # step 11: unblocked user login
        await handle_request(user.login, "User login", **USER_CREDS)
        logger.success(f"Successfully again!")

        # step 12: edit user
        new_name = await handle_request(user.edit_user, "Edit user", new_name="Jack", new_last_name="Sparrow")
        logger.success(f"User {current['name']} {current['last_name']} updated. New name: {new_name['name']} {new_name['last_name']}")


asyncio.run(main())
