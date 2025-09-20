from typing import Type

from tortoise.models import Model
from tortoise.exceptions import IntegrityError

from db.base import BaseDB
from db.table import UserDBModel, SessionDBModel
from loguru import logger


class DataBaseController(BaseDB):
    db: Type[Model] = UserDBModel
    session_db: Type[Model] = SessionDBModel

    async def ensure_user(self, user: dict):
        real_dict = user
        real_dict['password'] = user["password"].get_secret_value()
        try:
            return await self.db.create(**real_dict)
        except IntegrityError:
            logger.warning(f"User already exists")
            return await self.get_by_email(user["email"])
        except Exception as e:
            logger.error(f"Error while getting user {e}")


    async def get_user(self, email, password):
        return await self.db.filter(email=email, password=password).first()

    async def get_user_by_id(self, user_id):
        return await self.db.filter(user_id=user_id).first()

    async def get_by_email(self, email):
        return await self.db.filter(email=email).first()

    async def update(self, user_id: str, **kwargs):
        await self.db.filter(user_id=user_id).update(**kwargs)
        return await self.db.filter(user_id=user_id).first()


    async def create_session(self, user_id, session_id):
        return await self.session_db.create(user_id=user_id, session_id=session_id)

    async def validate_session(self, user_id, session_id):
        return await self.session_db.filter(user_id=user_id, session_id=session_id).exists()

    async def kill_session(self, user_id):
        return await self.session_db.filter(user_id=user_id).delete()
