import datetime
import sqlite3

from error import AuthenticationError


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
    def register_user(self, login: str, password: str, phone_number: str, name: str, surname: str):
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
            INSERT INTO users (login, password, phone_number, name, surname)
            VALUES (?, ?, ?,?,?)
            """, (login, password, phone_number, name, surname))

            self.connection.commit()
            print("Пользователь успешно зарегистрирован!")
            return {"success": True, "time": datetime.datetime.now()}
        except sqlite3.IntegrityError as e:

            print("Ошибка: Пользователь с таким именем или email уже существует.")
            print(e)
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
        return self.__add_user_like(login, password, "favorites", "item_id", item_id)

    def add_post_like(self, login: str, password: str, post_id: int):
        """
        Добавляет или удаляет лайк для записи со стены
        :param login: 
        :param password: 
        :param post_id: 
        :return: 
        """
        return self.__add_user_like(login, password, "post_likes", "post_id", post_id)

    def __add_user_like(self, login: str, password: str, table_name: str, liked_category: str, liked_id: int):
        """
        Абстрактный класс для лайка чего-то. Подходит для лайка предмета и записи со стены

        :param login:
        :param password:
        :param table_name: `favorites` для лайков предметов, `post_likes` для лайка записей
        :param liked_category: `item_id` для [favorites] и `post_id` для [post_likes]
        :param liked_id: id предмета который лайкаем
        :return:
        """
        try:
            user_id = self.__check_user(login, password)
        except AuthenticationError as ex:
            return ex.as_dict()

        # if user_id is dict:
        #     return user_id

        self.cursor.execute(f"""
                    SELECT * FROM {table_name}
                    where user_id == ? AND {liked_category} == ?;
                    """, (user_id, liked_id))
        favorite_row = self.cursor.fetchone()

        if favorite_row:  # существует такая строка
            self.cursor.execute(f"""DELETE FROM {table_name} WHERE user_id == ? AND {liked_category} == ?""",
                                (user_id, liked_id))
            print(f"Лайк {liked_category} был снят")  # todo Логгирование
        else:
            self.cursor.execute(
                f"""
                INSERT INTO {table_name} (user_id, {liked_category})
                VALUES (?, ?)
                """, (user_id, liked_id))
            print(f"Лайк {liked_category} был поставлен")

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
        try:
            user_id = self.__check_user(login, password)
        except AuthenticationError as ex:
            return ex.as_dict()
        # if user_id is dict:
        #     return user_id

        print(user_id, type(user_id))
        self.cursor.execute("""
        SELECT * from items item_t 
        JOIN favorites favor_t WHERE (item_t.id == favor_t.item_id AND favor_t.user_id == ?) """, (user_id,))

        rows = self.cursor.fetchall()
        columns = [column[0] for column in self.cursor.description]

        return [dict(zip(columns, row)) for row in rows]

    def get_list_of_posts(self, limit: int = 10):
        """
        Выдаёт список постов с подробными характеристиками, количеством лайков и комментариев

        :param limit:  лимит постов на один запрос (по умолчанию 10)
        :return:
        """
        self.cursor.execute("""
        SELECT p.id,
        p.image,
        bus.name                  as 'company_name',
        bus.logo_image            as 'company_logo_image',
        bus.id                    as 'company_id',
        (SELECT COUNT(*)
        FROM post_likes pl
        WHERE pl.post_id = p.id) AS 'like_count',
        (SELECT COUNT(*)
        FROM post_comments pc
        WHERE pc.post_id = p.id) AS 'comment_count',
        p.created_at

        FROM posts p
        JOIN business bus WHERE P.owner_id = bus.id
        LIMIT ?
        """, (limit,))

        rows = self.cursor.fetchall()
        columns = [column[0] for column in self.cursor.description]

        return [dict(zip(columns, row)) for row in rows]

    def __check_user(self, login: str, password: str):
        """
        Проверяет на наличие авторизованного пользователя
        :param login:
        :param password:
        :return:
        """
        self.cursor.execute("""
                            SELECT id FROM users WHERE (login == ? AND password == ?)
                            """, (login, password))
        user_row = self.cursor.fetchone()
        if not user_row:
            raise AuthenticationError("The user is not logged in")
            # return {"error": "The user is not logged in", "time": datetime.datetime.now()}
        return user_row[0]

    def get_comments_from_post(self, post_id: int, limit: int = 10):
        """
        Получить все комментарии (лимит 10 на запрос) под конкретным постом
        :param post_id:
        :param limit:
        :return:
        """
        self.cursor.execute("""
            SELECT pc.post_id,
                pc.text,
                pc.created_at,
                user.login as 'user_login',
                user.image as 'user_avatar_image'
            FROM post_comments pc
                JOIN users user
                WHERE pc.post_id == ?
                    AND user.id = pc.user_id
            LIMIT ?
            """, (post_id, limit))

        rows = self.cursor.fetchall()
        columns = [column[0] for column in self.cursor.description]

        return [dict(zip(columns, row)) for row in rows]

    def get_user_friend_list(self, login: str, password: str):

        try:
            user_id = self.__check_user(login, password)
        except AuthenticationError as ex:
            return ex.as_dict()

        self.cursor.execute(
            """
            SELECT
                u.id as 'user_id',
                u.name,
                u.surname,
                u.status,
                u.phone_number,
                u.image
            FROM
                friends f
            JOIN
                users u
            ON
                u.id = CASE
                           WHEN f.user_id = ? THEN f.friend_id
                           ELSE f.user_id
                       END
            WHERE
                f.user_id = ? OR f.friend_id = ?""",
            (user_id, user_id, user_id)
        )

        rows = self.cursor.fetchall()
        columns = [column[0] for column in self.cursor.description]

        return [dict(zip(columns, row)) for row in rows]

    def get_user_friend_info(self, login: str, password: str, friend_id: int):
        try:
            user_id = self.__check_user(login, password)
        except AuthenticationError as ex:
            return ex.as_dict()

        self.cursor.execute(
            """
            SELECT 
                u.id AS friend_id,
                u.name,
                u.surname,
                u.status,
                u.phone_number,
                u.image
            FROM 
                friends f
            JOIN 
                users u
            ON 
                u.id = f.friend_id
            WHERE 
                f.user_id = ? AND f.friend_id = ?;""",
            (user_id, friend_id)
        )

        rows = self.cursor.fetchall()
        if not rows:
            return {"error": "The user is not your friend.", "time": datetime.datetime.now()}
        columns = [column[0] for column in self.cursor.description]

        return [dict(zip(columns, row)) for row in rows]

    def get_favorites_by_friend(self, login: str, password: str, friend_id: int):
        try:
            user_id = self.__check_user(login, password)
        except AuthenticationError as ex:
            return ex.as_dict()

        self.cursor.execute(
            """
            WITH verified_friend AS (
                SELECT 
                    CASE 
                        WHEN f.user_id = ? THEN f.friend_id
                        ELSE f.user_id
                    END AS friend_id
                FROM 
                    friends f
                WHERE 
                    (f.user_id = ? AND f.friend_id = ?) OR (f.user_id = ? AND f.friend_id = ?)
            ),
            friend_favorites AS (
                SELECT 
                    fav.item_id
                FROM 
                    favorites fav
                JOIN 
                    verified_friend vf
                ON 
                    fav.user_id = vf.friend_id
            ),
            item_details AS (
                SELECT 
                    i.id,
                    i.name,
                    i.description,
                    i.average_rating,
                    i.brand,
                    i.image
                FROM 
                    items i
                JOIN 
                    friend_favorites ff
                ON 
                    i.id = ff.item_id
            )
            SELECT * FROM item_details;
            """,
            (user_id, user_id, friend_id, friend_id, user_id)
        )

        rows = self.cursor.fetchall()
        columns = [column[0] for column in self.cursor.description]

        return [dict(zip(columns, row)) for row in rows]

    def get_reviews_by_item(self, item_id: int):
        self.cursor.execute("""
        SELECT
            r.*,
            u.image AS user_image,
            u.name AS user_name
        FROM
            reviews r
        JOIN
            users u
        ON
            r.user_id = u.id
        WHERE
            r.item_id = ?;
""", (item_id,))
        rows = self.cursor.fetchall()
        columns = [column[0] for column in self.cursor.description]

        return [dict(zip(columns, row)) for row in rows]

    def get_items_by_filter(self, filters: dict):
        query = "SELECT * FROM items WHERE 1=1"
        params = []

        # Генерация WHERE условий на основе фильтров
        for key, value in filters.items():
            if value:
                if isinstance(value, tuple):
                    # Если это диапазон, то используем BETWEEN
                    query += f" AND {key} BETWEEN ? AND ?"
                    params.extend(value)
                else:
                    query += f" AND {key} = ?"
                    params.append(value)

        # Выполняем запрос
        self.cursor.execute(query, params)
        rows = self.cursor.fetchall()
        columns = [column[0] for column in self.cursor.description]

        return [dict(zip(columns, row)) for row in rows]


    def close(self):
        """
        Закрывает соединение с базой данных.
        """
        self.connection.close()
