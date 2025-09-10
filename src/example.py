import asyncio

from src.server.client import Client


NAME = "Iwan"
LAST_NAME = "Ragamafia"
EMAIL = "iwan.ragamafia@gmail.com"
PASSWORD = "123456"


async def register_user():
    client = Client()
    await client._create(
        name=NAME,
        last_name=LAST_NAME,
        email=EMAIL,
        password=PASSWORD
    )

async def login_user():
    client = Client()
    return await client._login(email=EMAIL, password=PASSWORD)

async def get_user(data):
    client = Client()
    return await client._get_user(data)
#
# async def login_admin():
#     pass  # login as admin and return admin session


# def promote_user_to_moderator(admin_session, user_id):
#     pass  # give moderator rights
#
#
# def delete_user(admin_session, user_id):
#     pass  # remove user
#
#
# def try_login_deleted_user():
#     pass  # attempt login, expect failure
#
#
# def make_request(session, endpoint, payload=None):
#     pass  # generic request function

async def main():
    await register_user()
    user_data = await login_user()
    print(await get_user(user_data))

    # # step 4: login as admin
    # admin_session = login_admin()
    #
    # # step 5: promote user
    # promote_user_to_moderator(admin_session, user_id=1)
    #
    # # step 6: get updated user data
    # get_user_data(user_session)
    #
    # # step 7: admin deletes user
    # delete_user(admin_session, user_id=1)
    #
    # # step 8: check deleted user cannot login
    # try_login_deleted_user()


asyncio.run(main())