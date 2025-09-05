from fastapi import APIRouter

from api.v1.order.routers import router as order_router

router = APIRouter(prefix="/v1")
router.include_router(order_router)

__all__ = ["router"]
