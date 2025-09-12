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
    resp = await user_client.create(
        name=FIRST_NAME,
        last_name=LAST_NAME,
        email=EMAIL,
        password=PASSWORD,
    )
    if resp:
        print(f"User created: {resp}")
    else:
        raise AssertionError("Can not create user")

    # step 2: login user
    if user_resp := await user_client.login(email=EMAIL, password=PASSWORD):
        if user_resp["success"] == True and user_resp["data"]["access_token"]:
            logger.success(f"Authenticate USER successfully")
    else:
        raise AssertionError("Can not auth user")

    # step 3: get user from database
    if user := await user_client.get_user(user_resp):
        print(f"User recived: {user}")
    else:
        raise AssertionError("Can not get user")

    # step 4: login admin
    if admin_resp := await admin_client.login(email=ADMIN_EMAIL, password=ADMIN_PASSWORD):
        if admin_resp["success"] == True and admin_resp["data"]["access_token"]:
            logger.success(f"Authenticate ADMIN successfully")
    else:
        raise AssertionError("Can not auth admin")

    # step 5: update user role
    if updated_user := await admin_client.update_role(user, "user"):   # change role (moderator / user)
        print(f"User updated: {updated_user}")
    else:
        raise AssertionError("Can not update user")

    # step 6: logout user
    if user_logout := await user_client.logout(user_resp):
        if user_logout["success"] == False:
            print(f"User logout: {user_logout}")
        else:
            raise AssertionError("Can not logout user")


    await user_client.close()
    await admin_client.close()


asyncio.run(main())