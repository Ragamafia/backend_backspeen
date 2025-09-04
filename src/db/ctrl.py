from typing import Type

from tortoise.models import Model

from src.db.base import BaseDB
from src.db.table import UserDBModel


class DataBaseController(BaseDB):
    db: Type[Model] = UserDBModel

    def __init__(self):
        super().__init__()
        self.db = UserDBModel

    @BaseDB.db_connect
    async def get_user(self, email):
        return await self.db.filter(email=email).first()

    @BaseDB.db_connect
    async def create(self, name, last_name, email, password):
        if not await self.db.filter(email=email).exists():
            await self.db.create(
                name=name,
                last_name=last_name,
                email=email,
                password=password
            )

    @BaseDB.db_connect
    async def read(self, email, password):
        return await self.db.filter(email=email, password=password).first()


db: DataBaseController = DataBaseController()