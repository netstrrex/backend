import uuid
from logging import getLogger

from domain.order.repositories.ABC import AbstractOrderRepository
from domain.order.repositories.exceptions import ProductOutOfStockException

logger = getLogger(__name__)


class OrderService:
    def __init__(self, repo: AbstractOrderRepository):
        self._repo = repo

    async def add_product_to_order(
        self, order_id: uuid.UUID, product_id: uuid.UUID, quantity: int
    ) -> None:
        try:
            await self._repo.add_product_to_order(order_id, product_id, quantity)
        except ProductOutOfStockException as e:
            logger.info("Product %s out of stock", str(product_id))
            raise e
