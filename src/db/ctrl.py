from typing import Type

from tortoise.models import Model

from src.db.base import BaseDB
from src.db.table import UserDBModel
from src.server.api.models import User


class DataBaseController(BaseDB):
    db: Type[Model] = UserDBModel

    @BaseDB.db_connect
    async def get_user(self, user_id):
        return await self.db.filter(id=user_id).first()

    @BaseDB.db_connect
    async def create(self, name, last_name, email, password):
        if not await self.db.filter(email=email).exists():
            user = await self.db.create(
                name=name,
                last_name=last_name,
                email=email,
                password=password,
                role="user"
            )
            return User.model_validate(user)

    @BaseDB.db_connect
    async def read(self, email, password):
        return await self.db.filter(email=email, password=password).first()

    @BaseDB.db_connect
    async def update(self, user_id, role):
        if user := await self.db.filter(id=user_id).first():
            user.role = role
            await user.save()
            return user

    @BaseDB.db_connect
    async def delete(self, user_id):
        if user := await self.db.filter(id=user_id).first():
            return await user.delete()