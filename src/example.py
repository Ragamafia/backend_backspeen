import asyncio

from src.server.client import Client
from logger import logger


ADMIN_EMAIL = "admin@admin.com"
ADMIN_PASSWORD = "654321"

FIRST_NAME = "Iwan"
LAST_NAME = "Ragamafia"
EMAIL = "user@user.com"
PASSWORD = "123456"


async def main():
    user_client = Client()
    admin_client = Client()

    # step 1: create user
    resp = await user_client.create_user(
        name=FIRST_NAME,
        last_name=LAST_NAME,
        email=EMAIL,
        password=PASSWORD,
    )
    if resp:
        logger.info(f"User created: {resp}")
    else:
        raise AssertionError("Can not create user")

    # step 2: login user
    user_resp = await user_client.login(email=EMAIL, password=PASSWORD)
    if user_resp["success"] == True and user_resp["data"]["access_token"]:
        logger.success(f"Authenticated successfully (USER)")
    else:
        raise AssertionError("Can not auth user")

    # step 3: get user from database
    if user := await user_client.get_user(user_resp):
        logger.info(f"User recived: {user['name']} {user['last_name']}")
    else:
        raise AssertionError("Can not get user")

    # step 4: login admin
    admin_resp = await admin_client.login(email=ADMIN_EMAIL, password=ADMIN_PASSWORD)
    if admin_resp["success"] == True and admin_resp["data"]["access_token"]:
        logger.success(f"Authenticated successfully (ADMIN)")
    else:
        raise AssertionError("Can not auth admin")

    # step 5: update user role
    new_role = "moderator"
    if updated_user := await admin_client.update_role(user, new_role):  # change (moderator/user)
        logger.debug(f"User update to {new_role}: {updated_user['name']} {updated_user['last_name']}")
    else:
        raise AssertionError("Can not update user")

    # step 6: logout user
    user_logout = await user_client.logout(user_resp)
    if user_logout["success"] == False:
        logger.debug(f"User logout (USER)")
    else:
        raise AssertionError("Can not logout user")

    # step 7: soft remove user
    if removed_user := await user_client.soft_remove(user.get("id")):
        logger.debug(f"User {user['name']} {user['last_name']} soft removed")
    else:
        raise AssertionError("Can not soft remove user")

    # step 8: try to login banned user
    banned_user = await user_client.login(email=EMAIL, password=PASSWORD)
    if banned_user["success"] == True and banned_user["data"]["access_token"]:
        logger.success(f"Successfully again!")
    else:
        logger.error(f"Can not login user")

    # step 9: unlock user
    if unblock_user := await admin_client.unblock(user.get("id")):
        logger.success(f"User unblock: {unblock_user['name']} {unblock_user['last_name']}")
    else:
        raise AssertionError("Can not unban user")

    # step 10: delete user
    if deleted_user := await admin_client.delete_user(user.get("id")):
        logger.debug(f"User deleted: {deleted_user}")
    else:
        raise AssertionError("Can not delete user")


    await user_client.close()
    await admin_client.close()


asyncio.run(main())