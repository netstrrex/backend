from logging import getLogger
from typing import Any

import asyncpg

from core.database import AbstractDatabase

from .schema import SCHEMA

logger = getLogger(__name__)


class PostgresDatabase(AbstractDatabase):
    _pool: asyncpg.Pool

    def __init__(self, dsn: str) -> None:
        self._dsn = dsn

    async def create_pool(self) -> None:
        self._pool = await asyncpg.create_pool(dsn=self._dsn)

    async def close_pool(self) -> None:
        await self._pool.close()

    async def execute(self, sql: str, *args: Any) -> None:
        async with self._pool.acquire() as connection, connection.transaction():
            try:
                await connection.execute(sql, *args)
            except Exception as e:
                logger.exception(e)

    async def executemany(self, sql: str, *args: Any) -> None:
        async with self._pool.acquire() as connection, connection.transaction():
            try:
                await connection.executemany(sql, *args)
            except Exception as e:
                logger.exception(e)

    async def fetch(
        self, sql: str, *args: Any
    ) -> tuple[
        dict[Any, Any] | dict[str, Any] | dict[str, str] | dict[bytes, bytes], ...
    ]:
        async with self._pool.acquire() as connection:
            rows = await connection.fetch(sql, *args)
        return tuple(dict(row) for row in rows)

    async def create_schema_if_not_exist(self) -> None:
        await self.execute(SCHEMA)
