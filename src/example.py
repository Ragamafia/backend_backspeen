import asyncio
from typing import Callable

from src.server.client import Client
from src.server.api.models import Response

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
        logger.success("Unauthorized")

        # step 8: login user again
        await handle_request(user.login, "User login", **USER_CREDS)
        logger.success(f"Authenticated successfully (USER)")

        # step 9: remove user
        await handle_request(admin.remove_user, "Remove user")
        logger.success(f"User deleted")

        # step 10: try deleted user login
        if unauthorized2 := await handle_unauthorized(user.login, "User login", **USER_CREDS):
            print(unauthorized2)
            logger.error(f"Response: {unauthorized2}")


asyncio.run(main())
#     # step 9: remove user
#     if removed_user := await user_client.remove_user():
#         logger.debug(f"User deleted: {removed_user}")
#     else:
#         raise AssertionError("Can not soft remove user")
#
#     # step 10: try deleted user login
#     deleted_user_resp = await user_client.login(email=USER["email"], password=USER["password"])
#     if deleted_user_resp.success:
#         logger.success(f"Successfully again!")
#     else:
#         logger.error(f"Can not login user")
#
#     # step 11: unlock user
#     if unblock_user := await admin_client.unblock_user(current_user["user_id"]):
#         logger.success(f"User unblock: {unblock_user.data['name']} {unblock_user.data['last_name']}")
#     else:
#         raise AssertionError("Can not unban user")
#
#     # step 12: unblocked user login
#     user_resp = await user_client.login(email=USER["email"], password=USER["password"])
#     if user_resp.success:
#         logger.success(f"Successfully again!")
#     else:
#         logger.error(f"Can not login user")
#
#     # step 13: edit user
#     if updated_user := await user_client.edit_user(new_name="Jack", new_last_name="Sparrow"):
#         logger.info(f"User {current_user.data['name']} {current_user.data['last_name']} updated. New name: {updated_user.data['name']} {updated_user.data['last_name']}")
#     else:
#         raise AssertionError("Can not update user")
