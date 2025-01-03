import datetime
import os
from typing import Optional

import uvicorn
from fastapi import FastAPI, Query, Header
from fastapi.staticfiles import StaticFiles

from DbWorker import DbWorker
from error import AuthenticationError
from logging_config import setup_logger

app = FastAPI()

# Выдача изображений на предметы
app.mount("/item_image", StaticFiles(directory="item_image"), name="item_image")

# Выдача изображений на аватарки пользователей
app.mount("/user_image", StaticFiles(directory="user_image"),
          name="user_image")

# Выдача изображений на посты
app.mount("/post_image", StaticFiles(directory="post_image"), name="post_image")

# Выдача изображений компаний
app.mount("/business_image", StaticFiles(directory="business_image"),
          name="business_image")

logger = setup_logger('api_main')
db = DbWorker()


@app.get("/items")
async def get_items():
    """
    Получить список предметов. Лимит в 10 за запрос.
    :return:
    """
    return db.fetch_items()


@app.get("/items/")
async def get_item(item_id: int):
    """
    Получение предметов по его ID
    :param item_id:
    :return:
    """
    res = db.fetch_item_by_id(int(item_id))
    return res


@app.get("/item/reviews")
async def get_item_reviews(item_id: int = Header(..., alias="item_id")):
    """
    Получить отзывы на конкретный предмет по ID
    :param item_id:
    :return:
    """
    try:
        answer = db.get_reviews_by_item(item_id)
        return answer
    except Exception as ex:
        logger.error(ex)
        raise ex

@app.post("/registration")
async def registration_new_user(login: str = Header(...), password: str = Header(...),
                                phone_number: str = Header(..., alias="phone_number"),
                                name: str = Header(...), surname: str = Header(...)):
    """
    Регистрация нового пользователя
    :param login:
    :param password:
    :param phone_number:
    :param name:
    :param surname:
    :return:
    """
    # TODO реализовать проверку на формат данных

    print(login, password, phone_number)
    answer = db.register_user(login, password, phone_number, name, surname)
    return answer


@app.post("/like")
async def reg_new_like_item(login: str = Header(...), password: str = Header(...),
                            item_id: int = Header(..., alias="item_id")):
    """
    Поставить или снять лайк `предмету`. Требуется авторизация
    :param login:
    :param password:
    :param item_id:
    :return:
    """
    # TODO реализовать проверку на формат данных

    print(login, password, int(item_id))
    answer = db.add_favourites(login, password, int(item_id))
    return answer


@app.post("/like_post")
async def reg_new_like_post(login: str = Header(...), password: str = Header(...),
                            post_id: int = Header(..., alias="post_id")):
    """
    Поставить или снять лайк `посту`. Требуется авторизация
    :param login:
    :param password:
    :param post_id:
    :return:
    """
    # TODO реализовать проверку на формат данных

    try:
        print(login, password, int(post_id))
        answer = db.add_post_like(login, password, int(post_id))
        return answer
    except Exception as ex:
        print(ex)

    return {"error": "Invalid headers", "time": datetime.datetime.now()}


@app.delete("/user")
async def delete_user(login: str = Header(...), password: str = Header(...)):
    """
    Удаление юзера. Требуется авторизация.
    :param login:
    :param password:
    :return:
    """
    # todo сделать это админ фичёй

    return db.delete_user(login, password)


@app.get("/auth")
async def get_user_auth_info(login: str = Header(...), password: str = Header(...)):
    """
    Функция проверят валидность данных пользователя для авторизации

    TODO: должен выдавать токен авторизации
    :param login:
    :param password:
    :return:
    """
    try:
        return db.check_auth_user(login, password)
    except AuthenticationError as ex:
        return ex.as_dict()


@app.get("/like")
async def get_list_of_favorites(login: str = Header(...), password: str = Header(...)):
    """
    Получить список избранных `предметов` от юзера. Требуется авторизация.
    :param login:
    :param password:
    :return:
    """
    # TODO реализовать проверку на формат данных

    print(login, password)
    answer = db.get_list_of_favorites(login, password)
    return answer


@app.get("/post/get_comments")
async def get_comments_from_post(post_id: int = Header(..., alias="post_id")):
    """
    Получить список комментариев от поста. Лимит 10 за запрос
    :param post_id:
    :return:
    """
    # TODO реализовать проверку на формат данных
    # TODO сделать докрутку информации (после 0-10, выдавать 11-20, 21-30 и тд.

    try:
        print(post_id)
        answer = db.get_comments_from_post(int(post_id))
        return answer
    except Exception as ex:
        print(ex)


@app.get("/posts")
async def get_list_of_posts():
    """
    Получить список всех постов. Лимит 10 за запрос
    :return:
    """
    # TODO сделать докрутку информации (после 0-10, выдавать 11-20, 21-30 и тд.
    answer = db.get_list_of_posts()
    return answer


@app.get("/user/friends")
async def get_list_of_friends(login: str = Header(...), password: str = Header(...)):
    """
    Получить список всех друзей пользователя. Требуется авторизация.
    :param login:
    :param password:
    :return:
    """
    # TODO реализовать проверку на формат данных

    answer = db.get_user_friend_list(login, password)
    return answer


@app.get("/user/friend_info")
async def get_friend_info(login: str = Header(...), password: str = Header(...),
                          friend_id: int = Header(..., alias="friend_id")):
    """
    Получить информацию о конкретном друге. Требуется авторизация, требуется наличие "друга" в друзьях пользователя
    :param login:
    :param password:
    :param friend_id:
    :return:
    """
    # TODO реализовать проверку на формат данных
    try:
        answer = db.get_user_friend_info(login, password, friend_id)
        return answer
    except ValueError as ex:
        return {"error": "Friend_id is int value.", "time": datetime.datetime.now()}  # TODO вынести в метод


@app.get("/user/friend_info/favorites")
async def get_list_of_favorites_by_friend(login: str = Header(...), password: str = Header(...),
                                          friend_id: int = Header(..., alias="friend_id")):
    """
    Получить список избранного от своего друга. Требуется авторизация и наличие "друга" в списке друзей пользователя.
    :param login:
    :param password:
    :param friend_id:
    :return:
    """

    try:
        answer = db.get_favorites_by_friend(login, password, int(friend_id))
        return answer
    except ValueError as ex:
        return {"error": "Friend_id is int value.", "time": datetime.datetime.now()}  # TODO вынести в метод


@app.get("/filter_items")
async def filter_items(
        country: Optional[str] = Query(None),
        style: Optional[str] = Query(None),
        types: Optional[str] = Query(None),
        alcohol_range: Optional[str] = Query(None),  # Ожидаем диапазон в виде строки "2-4"
        density_range: Optional[str] = Query(None),  # То же для плотности
):
    """
    Получение списка "отфильрованных" предметов. Лимит на 10 за запрос.
    :param country:
    :param style:
    :param types:
    :param alcohol_range:
    :param density_range:
    :return:
    """

    # TODO сделать докрутку информации (после 0-10, выдавать 11-20, 21-30 и тд.
    def parse_range(range_str):
        """
        Парсим промежуток. Получаем мин-макс.
        :param range_str: Обязательно int"-"int
        :return:
        """
        if range_str:
            try:
                lower, upper = map(float, range_str.split("-"))
                return lower, upper
            except ValueError:
                return None
        return None

    # Собираем фильтры в словарь
    filters = {
        "country": country,
        "style": style,
        "color": types,
        "alcohol_percentage": parse_range(alcohol_range),
        "density": parse_range(density_range)
    }

    # Получаем данные
    items = db.get_items_by_filter(filters)
    return items


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()

    parser.add_argument("--test", action="store_true", help="Need test ip (only local hosting")

    args = parser.parse_args()
    startup_ip = "0.0.0.0"
    if args.test:
        startup_ip = "127.0.0.1"

        logger.info("========================")
        logger.info("Start API in local env")
    elif os.name == 'nt':
        logger.critical("=================================")
        logger.critical("Code was stared by Win System. You're crazy, or forget --test flag.")
        logger.critical("=================================")
        exit(2)
    else:
        logger.info("========================")
        logger.info("Start API in VPS")

    uvicorn.run("main:app", host=startup_ip, port=80, reload=True, log_config=f"logs/unicorn_config_log.ini")
