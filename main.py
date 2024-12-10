import uvicorn
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from DB_worker import DB_worker

app = FastAPI()

app.mount("/item_image", StaticFiles(directory="item_image"), name="item_image") # Выдача изображений на предметы
app.mount("/user_image", StaticFiles(directory="user_image"), name="user_image") # Выдача изображений на предметы

db = DB_worker()

# Получение списка всех элементов
@app.get("/items/")
def get_items():
    return db.fetch_items()

# Получение элемента по ID
@app.get("/items/{item_id}")
def get_item(item_id: str):
    res = db.fetch_item_by_id(int(item_id))
    return res

# Добавление нового элемента
# @app.post("/items/")
# def add_item(item_id: str, name: str, price: float):
#     if item_id in items:
#         return {"error": "Item already exists"}
#     items[item_id] = {"name": name, "price": price}
#     return {"message": "Item added", "item": items[item_id]}

# Удаление элемента
# @app.delete("/items/{item_id}")
# def delete_item(item_id: str):
#     if item_id in items:
#         deleted_item = items.pop(item_id)
#         return {"message": "Item deleted", "item": deleted_item}
#     return {"error": "Item not found"}


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)