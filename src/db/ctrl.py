from typing import Type

from tortoise.models import Model

from src.db.base import BaseDB
from src.db.table import UserDBModel
from models import User


class DataBaseController(BaseDB):
    db: Type[Model] = UserDBModel

    def __init__(self):
        super().__init__()
        self.db = UserDBModel

    @BaseDB.db_connect
    async def create(self, first_name, last_name, email, password):
        if not await self.db.filter(email=email).exists():
            await self.db.create(
                first_name=first_name,
                last_name=last_name,
                email=email,
                password=password
            )
            return await self.db.filter(email=email).first().values()
        return None

    @BaseDB.db_connect
    async def read(self, email, password):
        if result := await self.db.filter(email=email, password=password).first().values():
            return result
        return None


db: DataBaseController = DataBaseController()