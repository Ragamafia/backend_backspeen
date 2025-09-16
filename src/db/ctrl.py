from typing import Type

from tortoise.models import Model
from tortoise.exceptions import IntegrityError

from src.db.base import BaseDB
from src.db.table import UserDBModel
from loguru import logger


class DataBaseController(BaseDB):
    db: Type[Model] = UserDBModel

    @BaseDB.db_connect
    async def ensure_user(self, user: dict):
        try:
            return await self.db.create(**user)
        except IntegrityError:
            logger.warning(f"User already exists")
            return await self.get_by_email(user["email"])
        except Exception as e:
            logger.error(f"Error while getting user {e}")

    @BaseDB.db_connect
    async def get_user(self, email, password):
        return await self.db.filter(email=email, password=password).first()

    @BaseDB.db_connect
    async def get_user_by_id(self, user_id):
        return await self.db.filter(id=user_id).first()

    @BaseDB.db_connect
    async def get_by_email(self, email):
        return await self.db.filter(email=email).first()

    @BaseDB.db_connect
    async def update(self, user_id: str, **kwargs):
        await self.db.filter(id=user_id).update(**kwargs)
        return await self.db.filter(id=user_id).first()


db = DataBaseController()
