import datetime
import sqlite3


class DB_worker:
    def __init__(self, db_name="database.db"):
        """
        Инициализация подключения к базе данных.
        """
        self.db_name = db_name
        self.connection = sqlite3.connect(self.db_name, check_same_thread=False)
        self.cursor = self.connection.cursor()

    def fetch_items(self, limit=10):
        """
        Извлекает максимум `limit` предметов из таблицы `items`.
        """
        query = f"SELECT * FROM items LIMIT {limit}"
        self.cursor.execute(query)
        rows = self.cursor.fetchall()
        columns = [column[0] for column in self.cursor.description]
        # Преобразуем в JSON
        return [dict(zip(columns, row)) for row in rows]

    def fetch_item_by_id(self, item_id: int):
        """
        Извлекает предмет по ID из таблицы `items`.
        """
        query = "SELECT * FROM items WHERE id = ?"
        self.cursor.execute(query, (item_id,))
        row = self.cursor.fetchone()

        # Если предмет не найден
        if not row:
            return {"error": "Item not found"}

        # Получаем названия столбцов
        columns = [column[0] for column in self.cursor.description]

        # Преобразуем в словарь
        return dict(zip(columns, row))

    # Функция для регистрации пользователя
    def register_user(self, login: str, password: str, phone_number: str):
        try:
            # hashed_password = hash_password(password)  # TODO Хешируем пароль
            self.cursor.execute("""
            INSERT INTO users (login, password, phone_number)
            VALUES (?, ?, ?)
            """, (login, password, phone_number))

            self.connection.commit()
            print("Пользователь успешно зарегистрирован!")
            return {"success": True, "time": datetime.datetime.now()}
        except sqlite3.IntegrityError as e:
            print("Ошибка: Пользователь с таким именем или email уже существует.")
            return {"error_code": 1, "error": "The user has already been created.", "time": datetime.datetime.now()}
        except Exception as e:
            print(f"Произошла ошибка: {e}")
            return {"error_code": 0, "error": "Undetected error", "time": datetime.datetime.now()}

    def close(self):
        """
        Закрывает соединение с базой данных.
        """
        self.connection.close()
