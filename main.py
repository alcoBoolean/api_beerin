import datetime
import os

import uvicorn
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles

from DbWorker import DbWorker

app = FastAPI()

app.mount("/item_image", StaticFiles(directory="item_image"), name="item_image")  # Выдача изображений на предметы
app.mount("/user_image", StaticFiles(directory="user_image"), name="user_image")  # Выдача изображений на предметы

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


# Добавление нового элемента
@app.post("/registration")
async def registration_new_user(request: Request):
    headers = request.headers
    login = headers.get("login")
    password = headers.get("password")
    phone_number = headers.get("phone_number")
    # TODO реализовать проверку на формат данных

    if login and password and phone_number:
        print(login, password, phone_number)
        answer = db.register_user(login, password, phone_number)
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
