import datetime
import os

import uvicorn
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles

from DbWorker import DbWorker

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

db = DbWorker()


# Получение списка всех элементов
@app.get("/items")
async def get_items():
    return db.fetch_items()


# Получение элемента по ID
@app.get("/items/")
async def get_item(item_id: int):
    try:
        res = db.fetch_item_by_id(int(item_id))
    except ValueError as ex:
        print("Exception in get_item", ex)
        return {"error": "Invalid index", "time": datetime.datetime.now()}

    return res


@app.get("/item/reviews")
async def get_item_reviews(request: Request):
    headers = request.headers
    item_id = headers.get("item_id")
    try:
        if item_id:
            answer = db.get_reviews_by_item(int(item_id))
            return answer
    except ValueError as ex:
        return {"error": "Item_id must be integer.", "time": datetime.datetime.now()}
    return {"error": "Invalid headers", "time": datetime.datetime.now()}


# Добавление нового элемента
@app.post("/registration")
async def registration_new_user(request: Request):
    headers = request.headers
    login = headers.get("login")
    password = headers.get("password")
    phone_number = headers.get("phone_number")
    name = headers.get("name")
    surname = headers.get("surname")

    # TODO реализовать проверку на формат данных

    if login and password and phone_number and name and surname:
        print(login, password, phone_number)
        answer = db.register_user(login, password, phone_number, name, surname)
        return answer
    else:
        return {"error": "Invalid headers", "time": datetime.datetime.now()}


# Добавление в избранное
@app.post("/like")
async def reg_new_like_item(request: Request):
    headers = request.headers
    login = headers.get("login")
    password = headers.get("password")
    item_id = headers.get("item_id")
    # TODO реализовать проверку на формат данных

    if login and password and item_id:
        print(login, password, int(item_id))
        answer = db.add_favourites(login, password, int(item_id))
        return answer
    else:
        return {"error": "Invalid headers", "time": datetime.datetime.now()}


# Поставить или снять лайк с поста
@app.post("/like_post")
async def reg_new_like_post(request: Request):
    headers = request.headers
    login = headers.get("login")
    password = headers.get("password")
    post_id = headers.get("post_id")
    # TODO реализовать проверку на формат данных

    try:
        if login and password and post_id:
            print(login, password, int(post_id))
            answer = db.add_post_like(login, password, int(post_id))
            return answer
    except Exception as ex:
        print(ex)

    return {"error": "Invalid headers", "time": datetime.datetime.now()}


# Получить список всех избранных предметов
@app.get("/like")
async def get_list_of_favorites(request: Request):
    headers = request.headers
    login = headers.get("login")
    password = headers.get("password")  # TODO реализовать проверку на формат данных

    if login and password:
        print(login, password)
        answer = db.get_list_of_favorites(login, password)
        return answer
    else:
        return {"error": "Invalid headers", "time": datetime.datetime.now()}  # TODO вынести в метод


# выдаёт список всех комментариев (лимит 10 за запрос)
@app.get("/post/get_comments")
async def get_comments_from_post(request: Request):
    headers = request.headers
    post_id = headers.get("post_id")  # TODO реализовать проверку на формат данных

    try:
        if post_id:
            print(post_id)
            answer = db.get_comments_from_post(int(post_id))
            return answer
    except Exception as ex:
        print(ex)

    return {"error": "Invalid headers", "time": datetime.datetime.now()}  # TODO вынести в метод


# выдаёт список всех постов (лимит 10 за запрос)
@app.get("/posts")
async def get_list_of_posts():
    answer = db.get_list_of_posts()
    return answer


@app.get("/user/friends")
async def get_list_of_friends(request: Request):
    headers = request.headers
    login = headers.get("login")  # TODO реализовать проверку на формат данных
    password = headers.get("password")  # TODO реализовать проверку на формат данных

    if login and password:
        answer = db.get_user_friend_list(login, password)
        return answer

    return {"error": "Invalid headers", "time": datetime.datetime.now()}  # TODO вынести в метод


@app.get("/user/friend_info")
async def get_friend_info(request: Request):
    headers = request.headers
    login = headers.get("login")  # TODO реализовать проверку на формат данных
    password = headers.get("password")  # TODO реализовать проверку на формат данных
    friend_id = headers.get("friend_id")

    try:
        if login and password and friend_id:
            answer = db.get_user_friend_info(login, password, int(friend_id))
            return answer
    except ValueError as ex:
        return {"error": "Friend_id is int value.", "time": datetime.datetime.now()}  # TODO вынести в метод
    return {"error": "Invalid headers", "time": datetime.datetime.now()}  # TODO вынести в метод


@app.get("/user/friend_info/favorites")
async def get_list_of_favorites_by_friend(request: Request):
    headers = request.headers
    login = headers.get("login")  # TODO реализовать проверку на формат данных
    password = headers.get("password")  # TODO реализовать проверку на формат данных
    friend_id = headers.get("friend_id")

    try:
        if login and password and friend_id:
            answer = db.get_favorites_by_friend(login, password, int(friend_id))
            return answer
    except ValueError as ex:
        return {"error": "Friend_id is int value.", "time": datetime.datetime.now()}  # TODO вынести в метод
    return {"error": "Invalid headers", "time": datetime.datetime.now()}  # TODO вынести в метод


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()

    parser.add_argument("--test", action="store_true", help="Need test ip (only local hosting")

    args = parser.parse_args()
    startup_ip = "0.0.0.0"
    if args.test:
        startup_ip = "127.0.0.1"
    elif os.name == 'nt':
        print("=================================")  # TODO переделать на логгирование
        print("Code was stared by Win System. You're crazy, or forget --test flag.")
        print("=================================")
        exit(2)

    uvicorn.run("main:app", host=startup_ip, port=8000, reload=True)
