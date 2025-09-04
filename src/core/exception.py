class AppException(Exception):
    status_code: int = 500
    message: str = "Internal Server Error"

    def __init__(self, message: str | None = None):
        if message:
            self.message = message
