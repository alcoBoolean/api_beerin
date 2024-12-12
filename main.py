import datetime
import os

import uvicorn
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles

from DB_worker import DB_worker

app = FastAPI()

app.mount("/item_image", StaticFiles(directory="item_image"), name="item_image")  # Выдача изображений на предметы
app.mount("/user_image", StaticFiles(directory="user_image"), name="user_image")  # Выдача изображений на предметы

db = DB_worker()


# Получение списка всех элементов
@app.get("/items")
async def get_items():
    return db.fetch_items()


# Получение элемента по ID
@app.get("/items/{item_id}")
async def get_item(item_id: str):
    res = db.fetch_item_by_id(int(item_id))
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


# Удаление элемента
# @app.delete("/items/{item_id}")
# def delete_item(item_id: str):
#     if item_id in items:
#         deleted_item = items.pop(item_id)
#         return {"message": "Item deleted", "item": deleted_item}
#     return {"error": "Item not found"}


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
