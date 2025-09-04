from client.client import Client


NAME = "Iwan"
LAST_NAME = "Ragamafia"
EMAIL = "iwan.ragamafia@gmail.com"
PASSWORD = "123456"


async def register_user():
    client = Client()
    await client.create(
        name=NAME,
        last_name=LAST_NAME,
        email=EMAIL,
        password=PASSWORD
    )

async def login_user():
    client = Client()
    await client.login(email=EMAIL, password=PASSWORD)

async def session():
    client = Client()
    await client.session()