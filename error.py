import datetime


class AuthenticationError(Exception):
    """Класс исключения для ошибок аутентификации."""

    def __init__(self, message):
        super().__init__(message)
        self.details = {
            "error": message,
            "time": datetime.datetime.now()
        }

    def as_dict(self):
        """Метод для получения словаря с деталями ошибки."""
        return self.details
