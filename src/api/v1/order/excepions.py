from core.exception import AppException


class OutOfStockException(AppException):
    status_code: int = 409
    message: str = "The product out of stock"


class NotFoundException(AppException):
    status_code: int = 404
    message: str = "Not found"

    def __init__(self, message: str | None) -> None:
        if message:
            self.message = message
