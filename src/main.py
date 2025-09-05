from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from api import router
from config import settings
from core.exception import AppException
from infrastructure.database.postgres import PostgresDatabase
from infrastructure.logger.root import configure_root_logging
from infrastructure.server.gunicorn import GunicornApplication


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator:
    database = PostgresDatabase(settings.postgres.dsn)
    await database.create_pool()
    await database.create_schema_if_not_exist()
    app.state.database = database
    yield
    await database.close_pool()


configure_root_logging()
fastapi_app = FastAPI(lifespan=lifespan)
fastapi_app.include_router(router)


@fastapi_app.exception_handler(AppException)
async def app_exception_handler(request: Request, exc: AppException) -> JSONResponse:
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.message, "code": exc.status_code},
    )


if __name__ == "__main__":
    GunicornApplication(fastapi_app).run()
