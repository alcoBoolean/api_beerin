import datetime

from fastapi.responses import JSONResponse


class AuthenticationError(Exception):
    """Класс исключения для ошибок аутентификации."""

    def __init__(self, message):
        super().__init__(message)
        self.details = {
            "error": message,
            "time": datetime.datetime.now().isoformat()
        }

    def as_dict(self):
        """Метод для получения словаря с деталями ошибки."""
        return JSONResponse(
            status_code=401,
            content=self.details)
