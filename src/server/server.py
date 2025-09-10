import uvicorn
from fastapi import FastAPI

from config import cfg
from db.ctrl import DataBaseController
from src.server.api.http import register_router

class Server:
    app: FastAPI
    db: DataBaseController

    def __init__(self):
        self.app = FastAPI()
        self.db = DataBaseController()

    def run(self):
        register_router(self)

        uvicorn.run(
            self.app,
            host=cfg.host,
            port=cfg.port,
            log_level="info",
        )