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


    if user_resp := await user_client.login(email=EMAIL, password=PASSWORD):
        if user_resp["success"] == True and user_resp["data"]["access_token"]:
            logger.success(f"Authenticate USER successfully")
    else:
        raise AssertionError("Can not auth user")

    print(user_resp)
    if user := await user_client.get_user(user_resp):
        print(f"User recived: {user}")
    else:
        raise AssertionError("Can not get user")

    print(user_resp)
    if admin_resp := await admin_client.login(email=ADMIN_EMAIL, password=ADMIN_PASSWORD):
        if admin_resp["success"] == True and admin_resp["data"]["access_token"]:
            logger.success(f"Authenticate ADMIN successfully")
    else:
        raise AssertionError("Can not auth admin")


    if updated_user := await admin_client.update_role(user, "user"):
        print(f"User updated: {updated_user}")
    else:
        raise AssertionError("Can not update user")
    print(user_resp)
    new_data = await user_client.get_user(user_resp)
    print(f"User new data: {new_data}")




    await user_client.close()
    await admin_client.close()


asyncio.run(main())

#     async def delete_user(self, admin_session, user_id):
#         pass  # remove user
#
#     async def try_login_deleted_user(self):
#         pass  # attempt login, expect failure
#
#     async def make_request(self, session, endpoint, payload=None):
#         pass  # generic request function


#     # # step 6: get updated user data
#     # get_user_data(user_session)
#     #
#     # # step 7: admin deletes user
#     # delete_user(admin_session, user_id=1)
#     #
#     # # step 8: check deleted user cannot login
#     # try_login_deleted_user()
#