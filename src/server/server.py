import uvicorn
from fastapi import FastAPI

from config import cfg
from db.ctrl import DataBaseController
from src.server.api.users import register_users_router
from src.server.api.admin import register_admin_router


class Server:
    app: FastAPI
    db: DataBaseController

    def __init__(self):
        self.app = FastAPI()
        self.db = DataBaseController()
        self.app.state.db = self.db

    def run(self):
        register_users_router(self)
        register_admin_router(self)

        @self.app.on_event("startup")
        async def startup():
            await self.db.setup_db()

        uvicorn.run(
            self.app,
            host=cfg.host,
            port=cfg.port,
            log_level="info",
        )
