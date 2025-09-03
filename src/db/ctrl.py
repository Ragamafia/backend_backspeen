from typing import Type

from tortoise.models import Model

from src.db.base import BaseDB
from src.db.table import UserModel


class DataBaseController(BaseDB):
    user: Type[Model] = UserModel

    def __init__(self):
        super().__init__()
        self.user = UserModel

    @BaseDB.db_connect
    async def create(self, username):
        if user := await self.user.filter(username=username).first():
            raise ValueError("User already exists")
        else:
            await self.user.create(username=username)

    @BaseDB.db_connect
    async def read(self):
        return await self.user.all()


db: DataBaseController = DataBaseController()