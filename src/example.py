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
        logger.info(f"User created: {resp.get('name')} {resp.get('last_name')}")
    else:
        raise AssertionError("Can not create user")

    # step 2: login user
    user_resp = await user_client.login(email=user_data["email"], password=user_data["password"])
    if user_resp["success"]:
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
    if admin_resp["success"]:
        logger.success(f"Authenticated successfully (ADMIN)")
    else:
        raise AssertionError("Can not auth admin")

    # step 5: update user role
    new_role = "moderator"
    if updated_user := await admin_client.change_role(user, new_role):  # change (moderator/user)
        logger.debug(f"Update to {new_role}: {updated_user['name']} {updated_user['last_name']}")
    else:
        raise AssertionError("Can not update user")

    # step 6: logout user
    user_logout = await user_client.logout()
    if not user_logout["success"]:
        logger.debug(f"User logout")
    else:
        raise AssertionError("Can not logout user")

    # step 7: try getting info as a logged out user
    logged_out_user = await user_client.get_user(user_resp)
    try:
        logger.info(f"User recived: {logged_out_user['name']} {logged_out_user['last_name']}")
    except:
        logger.error(f"Response: {logged_out_user}")

    # step 8: login user again
    user_resp = await user_client.login(email=user_data["email"], password=user_data["password"])
    if user_resp["success"]:
        logger.success(f"Authenticated successfully (USER)")
    else:
        raise AssertionError("Can not auth user")

    # step 9: soft remove user
    if removed_user := await user_client.remove_user():
        logger.debug(f"User deleted: {removed_user}")
    else:
        raise AssertionError("Can not soft remove user")

    # step 10: try deleted user login
    deleted_user_resp = await user_client.login(email=user_data.get("email"), password=user_data.get("password"))
    if deleted_user_resp["success"]:
        logger.success(f"Successfully again!")
    else:
        logger.error(f"Can not login user")

    # step 11: unlock user
    if unblock_user := await admin_client.unblock_user(user.get("user_id")):
        logger.success(f"User unblock: {unblock_user['name']} {unblock_user['last_name']}")
    else:
        raise AssertionError("Can not unban user")

    # step 12: try deleted user login again
    user_resp = await user_client.login(email=user_data.get("email"), password=user_data.get("password"))
    if user_resp["success"]:
        logger.success(f"Successfully again!")
    else:
        logger.error(f"Can not login user")

    # step 13: edit user
    if updated_user := await user_client.edit_user(new_name="Jack", new_last_name="Sparrow"):
        logger.info(f"User {user["name"]} {user["last_name"]} updated. New name: {updated_user['name']} {updated_user['last_name']}")
    else:
        raise AssertionError("Can not update user")

    await user_client.close()
    await admin_client.close()


asyncio.run(main(user))