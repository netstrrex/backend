from fastapi import Request

from infrastructure.database.postgres import PostgresDatabase


def get_database(request: Request) -> PostgresDatabase:
    return request.app.state.database
