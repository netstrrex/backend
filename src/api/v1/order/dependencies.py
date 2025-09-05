from typing import cast

from fastapi.params import Depends

from api.v1.dependencies import get_database
from domain.order.repositories.repository import OrderRepository
from domain.order.service import OrderService
from infrastructure.database.postgres import PostgresDatabase

order_service: OrderService | None = None


def get_order_service(
    database: PostgresDatabase = Depends(get_database),
) -> OrderService:
    global order_service
    if order_service is None:
        order_repository = OrderRepository(database)
        order_service = OrderService(order_repository)
    return cast(OrderService, order_service)
