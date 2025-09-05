class ProductOutOfStockException(Exception):
    message: str = "The product is out of stock"


class OrderNotFound(Exception):
    message: str = "Order not found"


class ProductNotFound(Exception):
    message: str = "Product not found"
