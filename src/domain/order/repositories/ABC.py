import uuid
from abc import ABC, abstractmethod

from core.database import AbstractDatabase


class AbstractOrderRepository(ABC):
    def __init__(self, database: AbstractDatabase):
        self._database = database

    @abstractmethod
    async def add_product_to_order(
        self, order_id: uuid.UUID, product_id: uuid.UUID, quantity: int
    ) -> None:
        """
        Asynchronous method for adding a product to an order.

        Args:
            order_id (uuid.UUID): Order uuid
            product_id (uuid.UUID): Product uuid
            quantity(int): quantity of goods

        Raises:
            NotImplementedError: If the method is not implemented in a subclass.
            ProductOutOfStockException: If the product is out of stock
        """
        raise NotImplementedError
