import uuid
from typing import cast

from core.database import AbstractDatabase
from domain.order.repositories.ABC import AbstractOrderRepository
from domain.order.repositories.exceptions import (
    OrderNotFound,
    ProductNotFound,
    ProductOutOfStockException,
)


class OrderRepository(AbstractOrderRepository):
    def __init__(self, database: AbstractDatabase):
        super().__init__(database)

    async def add_product_to_order(
        self, order_id: uuid.UUID, product_id: uuid.UUID, quantity: int
    ) -> None:
        res = cast(
            tuple[dict[str, int], ...],
            await self._database.fetch(
                "SELECT add_product_to_order($1, $2, $3)",
                order_id,
                product_id,
                quantity,
            ),
        )
        status = res[0]["add_product_to_order"]
        match status:
            case 0:
                raise ProductOutOfStockException
            case 3:
                raise OrderNotFound
            case 4:
                raise ProductNotFound
