from functools import wraps

from tortoise import Tortoise

from config import cfg


def db_connect(func):
    @wraps(func)
    async def wrapper(self, *args, **kwargs):
        if not self.inited:
            await self.setup_db()
        return await func(self,*args, **kwargs)
    return wrapper


class BaseDB:
    name: str = ""
    inited: bool = False
    db_connect: callable = db_connect

    def __init__(self, prefix: str = None):
        if prefix:
            self.name = prefix

    async def setup_db(self):
        if self.name:
            filename = cfg.sql_lite_db_path.with_suffix(f".{self.name}.db")
        else:
            filename = cfg.sql_lite_db_path

        await Tortoise.init(
            db_url=f"sqlite://{filename}",
            modules={'models': ['src.db.table']}
        )
        await Tortoise.generate_schemas()
        BaseDB.inited = True