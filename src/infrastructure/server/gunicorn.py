from fastapi import FastAPI
from gunicorn.app.base import BaseApplication

from config import settings
from infrastructure.logger.gunicorn import GunicornLogger


class GunicornApplication(BaseApplication):
    def __init__(self, app: FastAPI) -> None:
        self.app = app
        super().__init__()

    def load_config(self) -> None:
        self.cfg.set("logger_class", GunicornLogger)
        self.cfg.set("bind", settings.gunicorn.bind)
        self.cfg.set("workers", settings.gunicorn.workers)
        self.cfg.set("worker_class", "uvicorn.workers.UvicornWorker")

    def load(self) -> FastAPI:
        return self.app
