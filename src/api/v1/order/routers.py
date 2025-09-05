import uuid

from fastapi import APIRouter, Depends

from api.v1.order.dependencies import get_order_service
from api.v1.order.excepions import NotFoundException, OutOfStockException
from api.v1.schemas import OkResponse
from domain.order.repositories.exceptions import (
    OrderNotFound,
    ProductNotFound,
    ProductOutOfStockException,
)
from domain.order.service import OrderService

router = APIRouter(prefix="/order", tags=["Task Management"])


@router.post(
    "/",
    response_model=OkResponse,
    responses={
        429: {"description": "The product out of stock"},
        404: {"description": "Not found"},
    },
)
async def add_product_to_order(
    order_id: uuid.UUID,
    product_id: uuid.UUID,
    quantity: int,
    order_service: OrderService = Depends(get_order_service),
) -> OkResponse:
    try:
        await order_service.add_product_to_order(order_id, product_id, quantity)
    except ProductOutOfStockException as e:
        raise OutOfStockException() from e
    except (OrderNotFound, ProductNotFound) as e:
        raise NotFoundException(e.message) from e
    return OkResponse(ok=True)
