import datetime
import sqlite3


class DbWorker:
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
        """
        Регистрирует пользователя
        :param login:
        :param password:
        :param phone_number:
        :return:
        """

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

    def add_favourites(self, login: str, password: str, item_id: int):
        """
        Добавляет или удаляет предмет из избранного
        :param login:
        :param password:
        :param item_id:
        :return:
        """

        self.cursor.execute("""
                            SELECT id FROM users WHERE (login == ? AND password == ?)
                            """, (login, password))
        user_row = self.cursor.fetchone()
        if not user_row:
            return {"error": "The user is not logged in", "time": datetime.datetime.now()}
        user_id = user_row[0]

        self.cursor.execute("""
                    SELECT item_id FROM favorites
                    where user_id == ? AND item_id == ?;
                    """, (user_id, item_id))
        favorite_row = self.cursor.fetchone()

        if favorite_row:  # существует такая строка
            self.cursor.execute("""DELETE FROM favorites WHERE user_id == ? AND item_id == ?""",
                                (user_id, item_id))
            print("Предмет был удалён из избранного")  # todo Логгирование
        else:
            self.cursor.execute(
                """
                INSERT INTO favorites (user_id, item_id)
                VALUES (?, ?)
                """, (user_id, item_id))
            print("Предмет был добавлен в избранное")

        print(user_row)
        try:
            self.connection.commit()
            return {'success': True, 'time': datetime.datetime.now()}
        except Exception as e:
            print(f"Произошла ошибка: {e}")
            return {"error_code": 0, "error": "Undetected error",
                    "time": datetime.datetime.now()}  # todo Вынести в метод ошибок

    def get_list_of_favorites(self, login: str, password: str):
        """
        Получить список с полным набором характеристик предмета, который был добавлен в избранное пользователем
        :param login:
        :param password:
        :return:
        """

        self.cursor.execute("""
        SELECT id FROM users WHERE  (login == ? AND password == ?)""", (login, password))
        row = self.cursor.fetchone()
        if not row:
            return {"error": "The user is not logged in", "time": datetime.datetime.now()}

        user_id = row[0]
        print(user_id, type(user_id))
        self.cursor.execute("""
        SELECT * from items item_t 
        JOIN favorites favor_t WHERE (item_t.id == favor_t.item_id AND favor_t.user_id == ?) """, (user_id,))

        rows = self.cursor.fetchall()
        columns = [column[0] for column in self.cursor.description]

        return [dict(zip(columns, row)) for row in rows]

    def close(self):
        """
        Закрывает соединение с базой данных.
        """
        self.connection.close()
