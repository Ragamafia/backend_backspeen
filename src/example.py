import asyncio

from src.server.client import Client

from logger import logger
from config import cfg


user = {
    "name": "Iwan",
    "last_name": "Ragamafia",
    "email": "user@user.com",
    "password": "123456"
}


async def main(user_data: dict):
    user_client = Client()
    admin_client = Client()

    # step 1: create user
    resp = await user_client.create_user(user_data)
    if resp:
        logger.info(f"User created: {resp}")
    else:
        raise AssertionError("Can not create user")

    # step 2: login user
    user_resp = await user_client.login(email=user_data["email"], password=user_data["password"])
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
    admin_resp = await admin_client.login(email=cfg.admin_email, password=cfg.admin_password)

    if admin_resp["success"] == True and admin_resp["data"]["access_token"]:
        logger.success(f"Authenticated successfully (ADMIN)")
    else:
        raise AssertionError("Can not auth admin")

    # step 5: update user role
    new_role = "moderator"
    if updated_user := await admin_client.change_role(user, new_role):  # change (moderator/user)
        logger.debug(f"User update to {new_role}: {updated_user['name']} {updated_user['last_name']}")
    else:
        raise AssertionError("Can not update user")

    # step 6: logout user
    user_logout = await user_client.logout()
    if user_logout["success"] == False:
        #user_client.headers.pop("Authorization")
        logger.debug(f"User logout (USER)")
    else:
        raise AssertionError("Can not logout user")

    # step 7: soft remove user
    if removed_user := await user_client.soft_remove():
        logger.debug(f"User {user['name']} {user['last_name']} - {removed_user}")
    else:
        raise AssertionError("Can not soft remove user")

    # step 8: try deleted user login
    banned_user = await user_client.login(email=user.get("email"), password=user.get("password"))
    if banned_user["success"] == True and banned_user["data"]["access_token"]:
        logger.success(f"Successfully again!")
    else:
        logger.error(f"Can not login user")

    # step 9: unlock user
    if unblock_user := await admin_client.unblock_user(user.get("id")):
        logger.success(f"User unblock: {unblock_user['name']} {unblock_user['last_name']}")
    else:
        raise AssertionError("Can not unban user")


    await user_client.close()
    await admin_client.close()


asyncio.run(main(user))