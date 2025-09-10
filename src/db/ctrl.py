from typing import Type

from tortoise.models import Model

from src.db.base import BaseDB
from src.db.table import UserDBModel


class DataBaseController(BaseDB):
    db: Type[Model] = UserDBModel

    @BaseDB.db_connect
    async def get_user(self, email):
        return await self.db.filter(email=email).first()

    async def get_user_by_id(self, user_id):
        return await self.db.filter(id=user_id).first()


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

    @BaseDB.db_connect
    async def update(self, user_id, name, last_name, email, password):
        if user := await self.db.filter(id=user_id).first():
            user.name = name
            user.last_name = last_name
            user.email = email
            user.password = password
            await user.save()

    @BaseDB.db_connect
    async def delete(self, user_id):
        if user := await self.db.filter(id=user_id).first():
            await user.delete()


db: DataBaseController = DataBaseController()