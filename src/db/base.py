from tortoise import Tortoise

from src.db.table import UserDBModel
from config import cfg


class BaseDB:

    async def setup_db(self):
        await Tortoise.init(
            db_url=f"sqlite://{cfg.sql_lite_db_path}",
            modules={'models': ['src.db.table']}
        )
        await Tortoise.generate_schemas()

        # Ensure super user
        await UserDBModel.get_or_create(
            name=cfg.admin_name,
            last_name=cfg.admin_last_name,
            email=cfg.admin_email,
            password=cfg.admin_password,
            role="admin",
        )
